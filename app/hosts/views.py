#!flask/bin/python
# encoding: utf-8

from .forms import *
from ..models import Activity, Schedule, User, Bookmark
from flask import flash, redirect, url_for, request, render_template, g, current_app
from flask_login import login_required, current_user
from .. import db
from . import hosts
import json
from ..register.views import send_email


@hosts.before_app_request
def before_request():
    g.activity_id = 0
    g.delete_activities_form = DeleteActivitiesForm()
    g.delete_schedules_form = DeleteSchedulesForm()


@hosts.route('/host/homepage')
@hosts.route('/host/homepage/<int:page>')
def index(page=1):
    activities = Activity.query.filter_by(host_id=current_user.id).order_by(Activity.start_date.desc())
    pagination = activities.paginate(page, 2, False)
    return render_template('host/homepage.html', page=page, pagination=pagination,
                           activities=activities, endpoint='hosts.index')


@hosts.route('/host/add_activity', methods=['GET', 'POST'])
@login_required
def add_activity():
    form = AddActivityForm()
    method = 'add'
    if form.validate_on_submit():
        name = form.name.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        location = form.location.data
        introduction = form.introduction.data
        activity = Activity(name=name, start_date=start_date, end_date=end_date, location=location,
                            introduction=introduction,
                            host_id=current_user.id)
        db.session.add(activity)
        db.session.commit()
        flash('success!')
        return redirect(url_for('hosts.index'))
    return render_template('host/add_activity.html', form=form, method=method)


@hosts.route('/host/edit_activity/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def edit_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    form = AddActivityForm()
    method = 'update'
    if form.validate_on_submit():
        activity.update(form.name.data, form.location.data, form.introduction.data,
                        form.start_date.data, form.end_date.data)
        db.session.add(activity)
        db.session.commit()
        flash(u'活动更新成功')
        return redirect(url_for('hosts.manage_activity', page=request.args.get('page', 1, type=int)))
    form.name.data = activity.name
    form.location.data = activity.location
    form.introduction.data = activity.introduction
    form.start_date.data = activity.start_date
    form.end_date.data = activity.end_date
    return render_template('host/add_activity.html', form=form, method=method)


@hosts.route('/host/manage_activity', methods=['GET', 'POST'])
@login_required
def manage_activity():
    page = request.args.get('page', 1, type=int)
    activities = Activity.query.filter_by(host_id=current_user.id).order_by(Activity.start_date.desc())
    pagination = activities.paginate(page, 3, False)
    form1 = DeleteActivityForm()
    form2 = DeleteActivitiesForm()
    return render_template('host/manage_activity.html', activities=activities, endpoint='hosts.manage_activity',
                           form1=form1, form2=form2, pagination=pagination, page=page)


@hosts.route('/host/delete_activity', methods=['GET', 'POST'])
@login_required
def delete_activity():
    form = DeleteActivityForm()
    if form.validate_on_submit():
        activity_id = int(form.activity_id.data)
        activity = Activity.query.get_or_404(activity_id)
        schedules = Schedule.query.filter_by(activity_id=activity_id)
        bookmarks = Bookmark.query.filter_by(activity_id=activity_id)
        for schedule in schedules:
            db.session.delete(schedule)
        for bookmark in bookmarks:
            participant = User.query.get(bookmark.owner_id)
            try:
                send_email(participant.email, 'Activity Canceled', 'host/email/cancled', user=participant,
                           activity=activity)
            except:
                flash('Email send failed')
            db.session.delete(bookmark)
        db.session.delete(activity)
        db.session.commit()
        flash('success')
        return redirect(url_for('hosts.manage_activity', page=request.args.get('page', 1, type=int)))
    return redirect(url_for('hosts.manage_activity', page=request.args.get('page', 1, type=int)))


@hosts.route('/host/delete_activities', methods=['GET', 'POST'])
@login_required
def delete_activities():
    form = DeleteActivitiesForm()
    if form.validate_on_submit():
        activity_ids = json.loads(form.activity_ids.data)
        for activity_id in activity_ids:
            activity = Activity.query.get_or_404(activity_id)
            schedules = Schedule.query.filter_by(activity_id=activity_id)
            bookmarks = Bookmark.query.filter_by(activity_id=activity_id)
            for schedule in schedules:
                db.session.delete(schedule)
            for bookmark in bookmarks:
                participant = User.query.get(bookmark.owner_id)
                try:
                    send_email(participant.email, 'Activity Canceled', 'host/email/cancled', user=participant,
                               activity=activity)
                except:
                    flash('email send failed')
                db.session.delete(bookmark)
            db.session.delete(activity)
        db.session.commit()
        flash('success')
        return redirect(url_for('hosts.index'))
    return redirect(url_for('hosts.manage_activity', page=request.args.get('page', 1, type=int)))


@hosts.route('/host/add_schedule/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def add_schedule(activity_id):
    form = AddScheduleForm()
    method = 'add'
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        start_time = form.start_time.data
        end_time = form.end_time.data
        location = form.location.data
        introduction = form.information.data
        activity = Activity.query.get_or_404(activity_id)
        if start_time.date() < activity.start_date or end_time.date() > activity.end_date:
            flash(u'日程的开始日期必须大于活动开始日期, 结束日期必须小于活动结束日期')
            form.start_time.data = None
            return render_template('host/add_schedule.html', form=form, method=method, page=page,
                                   activity_id=activity_id)
        schedule = Schedule(activity_id=activity_id,
                            start_time=start_time, end_time=end_time, location=location, information=introduction)
        db.session.add(schedule)
        db.session.commit()
        flash('success!')
        return redirect(url_for('hosts.manage_activity', page=page))
    return render_template('host/add_schedule.html', form=form, method=method, page=page, activity_id=activity_id)


@hosts.route('/host/edit_schedule/<int:schedule_id>', methods=['GET', 'POST'])
@login_required
def edit_schedule(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    method = 'update'
    page = request.args.get('page', 1, type=int)
    form = AddScheduleForm()
    activity_id = request.args.get('activity_id', 1, type=int)
    activity = Activity.query.get_or_404(activity_id)
    if form.validate_on_submit():
        if form.start_time.data.date() < activity.start_date or form.end_time.data.date() > activity.end_date:
            flash(u'日程的开始日期必须大于活动开始日期，结束日期必须小于活动结束日期')
            form.start_time.data = None
            return render_template('host/add_schedule.html', form=form, method=method, page=page,
                                   activity_id=activity_id)
        schedule.update(form.information.data, form.location.data,
                        form.start_time.data, form.end_time.data)
        db.session.add(schedule)
        db.session.commit()
        flash(u'更新成功')
        return redirect(
            url_for('hosts.manage_schedule', activity_id=activity_id, page=page))
    form.information.data = schedule.information
    form.location.data = schedule.location
    form.start_time.data = schedule.start_time
    form.end_time.data = schedule.end_time
    return render_template('host/add_schedule.html', form=form, activity_id=activity_id, method=method, page=page, schedule_id=schedule_id)


@hosts.route('/host/manage_schedule/<int:activity_id>', methods=['GET', 'POST'])
@login_required
def manage_schedule(activity_id):
    g.activity_id = activity_id
    page = request.args.get('page', 1, type=int)
    activity = Activity.query.get_or_404(activity_id)
    schedules = activity.schedules
    # schedules = Schedule.query.filter_by(activity_id=activity_id)
    pagination = schedules.paginate(page, 3, False)
    form1 = DeleteScheduleForm()
    form2 = DeleteSchedulesForm()
    return render_template('host/manage_schedule.html', schedules=schedules, endpoint='hosts.manage_schedule',
                           form1=form1, form2=form2, page=page, pagination=pagination, activity=activity)


@hosts.route('/host/delete-schedule', methods=['GET', 'POST'])
@login_required
def delete_schedule():
    form = DeleteScheduleForm()
    if form.validate_on_submit():
        schedule_id = int(form.schedule_id.data)
        schedule = Schedule.query.get_or_404(schedule_id)
        db.session.delete(schedule)
        db.session.commit()
        flash('success')
        return redirect(url_for('hosts.manage_activity', page=request.args.get('page', 1, type=int)))
    return redirect(
        url_for('hosts.manage_schedule', activity_id=g.activity_id, page=request.args.get('page', 1, type=int)))


@hosts.route('/host/delete-schedules', methods=['GET', 'POST'])
@login_required
def delete_schedules():
    form = DeleteSchedulesForm()
    if form.validate_on_submit():
        schedule_ids = json.loads(form.schedule_ids.data)
        for schedule_id in schedule_ids:
            schedule = Schedule.query.get_or_404(int(schedule_id))
            db.session.delete(schedule)
            db.session.commit()
        flash('success')
        return redirect(url_for('hosts.manage_activity', page=request.args.get('page', 1, type=int)))
    return redirect(url_for('hosts.manage_schedule', activity_id=g.activity_id))


@hosts.route('/host/activity_detail/<int:activity_id>', methods=['GET'])
@login_required
def activity_detail(activity_id):
    activity = Activity.query.get_or_404(int(activity_id))
    activity.update_flag = False
    host = User.query.filter_by(id=activity.host_id).first()
    schedules = activity.schedules
    return render_template('activity_details.html',
                           activity=activity, host=host, schedules=schedules, identity='hosts')
