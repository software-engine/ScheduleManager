#!flask/bin/python
# encoding: utf-8
from flask import request, render_template, json, redirect, url_for, g, flash
from flask_login import login_required, current_user
from . import participant
from forms import SearchByActivityForm, SearchByHostForm, DeleteActivityForm, \
    DeleteActivitiesForm, AddActivityForm, AddActivitiesForm
from ..models import User, Bookmark, Activity, get_activities
from .. import db


@participant.before_request
def before_request():
    g.user = current_user


@participant.route('/participant', methods=['GET', 'POST'])
@participant.route('/participant/homepage', methods=['GET', 'POST'])
@participant.route('/participant/homepage/<int:page>', methods=['GET', 'POST'])
@login_required
def homepage(page=1):
    form1 = SearchByHostForm()
    form2 = SearchByActivityForm()
    bookmarks = Bookmark.query.filter_by(owner_id=g.user.id)
    pagination = bookmarks.paginate(page, 2, False)
    activities = get_activities(pagination.items)
    return render_template('participant/homepage.html', activities=activities,
                           form1=form1, form2=form2, pagination=pagination,
                           endpoint='participant.homepage', page=page)


@participant.route('/participant/activity_details/<activity_id>')
@login_required
def activity_details(activity_id):
    activity = Activity.query.get_or_404(int(activity_id))
    activity.update_flag = False
    host = User.query.filter_by(id=activity.host_id).first()
    schedules = activity.schedules
    return render_template('activity_details.html',
                           activity=activity, host=host, schedules=schedules, identity='participant')


@participant.route('/participant/search_host', methods=['GET', 'POST'])
@login_required
def search_host():
    method = 'host'
    form = SearchByHostForm()
    if form.validate_on_submit():
        return redirect(url_for('participant.search_result', method=method, query=form.host_name.data))
    return redirect(url_for('participant.homepage'))


@participant.route('/participant/search_activity', methods=['GET', 'POST'])
@login_required
def search_activity():
    method = 'activity'
    form = SearchByActivityForm()
    if form.validate_on_submit():
        return redirect(url_for('participant.search_result', method=method, query=form.activity_name.data))
    return redirect(url_for('participant.homepage'))


@participant.route('/participant/search_result/<method>/<query>', methods=['GET', 'POST'])
@participant.route('/participant/search_result/<method>/<query>/<int:page>', methods=['GET', 'POST'])
@login_required
def search_result(method, query, page=1):
    activities = None
    if method == 'host':
        host_id = User.query.filter_by(name=query).first().id
        activities = Activity.query.filter_by(host_id=host_id).order_by(Activity.start_date.desc())
        if activities is None:
            flash(u'未找到相关主办方的活动')
            return redirect(url_for('participant.homepage'))
    if method == 'activity':
        activities = Activity.query.filter(Activity.name.like('%' + query + '%')).order_by(
            Activity.start_date.desc())
        a_list = activities.all()
        if len(a_list) == 0:
            flash(u'没有找到含有该字段的活动')
            return redirect(url_for('participant.homepage'))
    form1 = AddActivityForm()
    form2 = AddActivitiesForm()
    activities_per_page = activities.paginate(page, 2, False)
    return render_template('participant/search_result.html', query=query, activities=activities_per_page, form1=form1,
                           form2=form2, method=method, endpoint='participant.search_result', page=page)


@participant.route('/participant/search_add_activity', methods=['GET', 'POST'])
@login_required
def add_activity():
    form = AddActivityForm()
    method = request.args.get('method', type=unicode)
    query = request.args.get('query', type=unicode)
    if form.validate_on_submit():
        activity_id = int(form.activity_id.data)
        owner_id = g.user.id
        bookmark = Bookmark(owner_id=owner_id, activity_id=activity_id)
        bookmark.add()
        db.session.commit()
        flash(u'活动添加成功')
        return redirect(url_for('participant.search_result', method=method, query=query,
                                page=request.args.get('page', 1, type=int)))
    return redirect(url_for('participant.search_result', method=method, query=query,
                            page=request.args.get('page', 1, type=int)))


@participant.route('/participant/search_add_activities', methods=['GET', 'POST'])
@login_required
def add_activities():
    form = AddActivitiesForm()
    method = request.args.get('method', type=unicode)
    query = request.args.get('query', type=unicode)
    if form.validate_on_submit():
        activity_ids = json.loads(form.activity_ids.data)
        for activity_id in activity_ids:
            activity_id_int = int(activity_id)
            owner_id = g.user.id
            bookmark = Bookmark(owner_id=owner_id, activity_id=activity_id_int)
            bookmark.add()
        db.session.commit()
        flash(u'活动添加成功')
        return redirect(url_for('participant.homepage'))
    if g.method == 'host':
        return redirect(
            url_for('participant.search_result', method=method, query=query,
                    page=request.args.get('page', 1, type=int)))
    if g.method == 'activity':
        return redirect(
            url_for('participant.search_result', method=method, query=query,
                    page=request.args.get('page', 1, type=int)))


@participant.route('/participant/bookmark_manage', methods=['GET', 'POST'])
@login_required
def bookmark_manage():
    form1 = DeleteActivityForm()
    form2 = DeleteActivitiesForm()
    page = request.args.get('page', 1, type=int)
    bookmarks = Bookmark.query.filter_by(owner_id=g.user.id)
    pagination = bookmarks.paginate(page, 2, False)
    activities = get_activities(pagination.items)
    return render_template('participant/manage_bookmark.html', activities=activities, form1=form1,
                           form2=form2, page=page,
                           endpoint='participant.bookmark_manage', pagination=pagination)


@participant.route('/participant/bookmark_manage/delete_activity', methods=['GET', 'POST'])
@login_required
def delete_activity():
    form = DeleteActivityForm()
    if form.validate_on_submit():
        bookmark = Bookmark.query.filter_by(owner_id=g.user.id, activity_id=int(form.activity_id.data)).first()
        db.session.delete(bookmark)
        db.session.commit()
        flash(u'删除成功')
        return redirect(url_for('participant.bookmark_manage', page=request.args.get('page', 1, type=int)))
    return redirect(url_for('participant.bookmark_manage', page=request.args.get('page', 1, type=int)))


@participant.route('/participant/bookmark_manage/delete_activities', methods=['GET', 'POST'])
@login_required
def delete_activities():
    form = DeleteActivitiesForm()
    if form.validate_on_submit():
        activity_ids = json.loads(form.activity_ids.data)
        for item in activity_ids:
            bookmark = Bookmark.query.filter_by(owner_id=g.user.id, activity_id=int(item)).first()
            db.session.delete(bookmark)
        db.session.commit()
        flash(u'成功删除')
        return redirect(url_for('participant.homepage'))
    return redirect(url_for('participant.bookmark_manage', page=request.args.get('page', 1, type=int)))
