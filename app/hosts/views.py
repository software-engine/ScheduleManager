#!flask/bin/python
# encoding: utf-8

from .forms import addactivityform, deleteactivityform,  deletescheduleform, activityscheduleform, \
    deleteactivitysform, deleteschedulesform
from ..models import Activity, Schedule
from flask import flash, redirect, url_for, request, render_template
from flask_login import login_required, current_user
from .. import db
from . import hosts
import json
import pdfkit


@hosts.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    activity = Activity.query.filter_by(host_id=current_user.id).order_by(Activity.id)
    pagination = activity.paginate(1, 10, False)
    return render_template('hosts/index.html', page=page, pagination=pagination,
                           activity=activity, endpoint='.index')


@hosts.route('/add_activity', methods=['GET', 'POST'])
@login_required
def add_activity():
    form = addactivityform()
    if form.validate_on_submit():
        name = form.name.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        location = form.location.data
        intro = form.introduction.data
        act = Activity(name=name, start_data=start_time, end_data=end_time, location=location, introduction=intro,
                       host_id=current_user.id)
        db.session.add(act)
        db.session.commit()
        flash('success!')
        act_id = Activity.query.filter_by(name=name).first().id
        return redirect(url_for('.activity_detail', id=act_id))
    if form.errors:
        flash('danger')


@hosts.route('/manage_activity', methods=['GET', 'POST'])
@login_required
def manage_activity():
    activity = Activity.query.filter_by(id=current_user.id)
    pagination = activity.paginate(1, 10, False)
    form1 = deleteactivityform()
    form2 = deleteactivitysform()
    return render_template('hosts/manage_activity.html', activity=activity, endpoint='.manage_activity',
                           form1=form1, form2=form2, pagination=pagination)


@hosts.route('/manage_activity/delete_activity', methods=['GET', 'POST'])
@login_required
def delete_activity():
    form = deleteactivityform()
    if form.validate_on_submit():
        activity_id = int(form.activity_id.data)
        act = Activity.query.get_or_404(activity_id)
        db.session.delete(act)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('danger')
        else:
            flash('success')
    if form.errors:
        flash('danger')
    return redirect(url_for('.manage_activity', page=request.args.get('page', 1, type=int)))


@hosts.route('/manage_activity/detele_activitys', methods=['GET', 'POST'])
@login_required
def delete_activitys():
    form = deleteactivitysform()
    if form.validate_on_submit():
        activity_ids = json.loads(form.activity_ids.data)
        for activity_id in activity_ids:
            act = Activity.query.get_or_404(activity_id)
            db.session.delete(act)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                flash('danger')
            else:
                flash('success')
    if form.errors:
        flash('danger')
    return redirect(url_for('.manage_activity', page=request.args.get('page', 1, type=int)))


@hosts.route('/activity_detail/<int:activity_id>', method=['GET', 'POST'])
@login_required
def addschedule(activity_id):
    return redirect(url_for('.add_schedule', activity_id=activity_id))


@hosts.route('/activity_detail/<int:activity_id>', method=['GET', 'POST'])
@login_required
def manageschedule(activity_id):
    return redirect(url_for('.manage_schedule', activity_id=activity_id))


@hosts.route('/add_schedule', methods=['GET', 'POST'])
@login_required
def add_schedule():
    form = activityscheduleform()
    activity_id = request.args.get('activity_id')
    if form.validate_on_submit():
        start_time = form.start_time.data
        end_time = form.end_time.data
        location = form.location.data
        introduction = form.introduction.data
        sch = Schedule(activity_id=activity_id,
                       start_time=start_time, end_time=end_time, location=location, intromation=introduction)
        db.session.add(sch)
        db.session.commit()
        flash('success!')
        return redirect(url_for('.activity_detail', id=activity_id))
    if form.errors:
        flash('danger')
    activity = Activity.query.filter_by(id=activity_id)
    return render_template('hosts/activity_detail.html', activity=activity, schedules=activity.schedules,
                           endpoint='.activity_detail', id=activity.id)


@hosts.route('/manage-schedule', methods=['GET', 'POST'])
@login_required
def manage_schedule():
    schedule_id = request.arg.get('activity_id')
    schedule = Schedule.query.filter_by(id=schedule_id)
    form1 = deletescheduleform()
    form2 = deleteschedulesform()
    return render_template('hosts/manage_schedule.html', schedule=schedule, endpoint='.manage_schedule',
                           form1=form1, form2=form2)


@hosts.route('/manage-schedule/delete-schedule', methods=['GET', 'POST'])
@login_required
def delete_schedule():
    form = deletescheduleform()
    if form.validate_on_submit():
        schedule_id = int(form.schedule_id.data)
        schedule = Schedule.query.filter_by(id=schedule_id)
        db.session.delete(schedule)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('danger')
        else:
            flash('success')
            return redirect(url_for('.manage_schedule', activity_id=schedule.activity_id,
                                    page=request.args.get('page', 1, type=int)))
    if form.errors:
        flash('danger')


@hosts.route('/manage-schedule/delete-schedules', methods=['GET', 'POST'])
@login_required
def delete_schedules():
    form = deleteschedulesform()
    if form.validate_on_submit():
        schedule_ids = json.loads(form.schedule_ids.data)
        for schedule_id in schedule_ids:
            sch = Schedule.query.get_or_404(schedule_id)
            db.session.delete(sch)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                flash('danger')
            else:
                flash('success')
                return redirect(url_for('.manage_schedule', activity_id=sch.activity_id,
                                        page=request.args.get('page', 1, type=int)))
    if form.errors:
        flash('danger')


@hosts.route('/activity-detail/<int:activity_id>', methods=['POST'])
@login_required
def activity_detail(activity_id):
    activity = Activity.query.filter_by(id=activity_id)
    return render_template('activity_detail.html', activity=activity, schedules=activity.schedules,
                           endpoint='.activity_detail', id=activity.id)


@hosts.route('/activity-detail/<int:activity_id>', methods=['POST'])
@login_required
def print_pdf():
    pdfkit.from_url(request.path.url, 'activity.pdf')