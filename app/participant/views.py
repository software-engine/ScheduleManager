#!flask/bin/python
# encoding: utf-8
from flask import request, render_template, json,redirect, url_for,g, flash
from flask_login import login_required, current_user
from . import participant
from forms import SearchActivityForm, SearchHostForm, DeleteActivityForm,\
    DeleteActivitiesForm, AddActivityForm, AddActivitiesForm, ActivitydetailsForm
from ..models import User, Bookmark, Activity, get_activities
from .. import db


@participant.before_request
def before_request():
    g.user = current_user


@participant.route('/participant/my_bookmark', methods=['POST'])
@login_required
def my_bookmark():
    if g.user.is_anonymous or g.user.confirmed:
        return redirect(url_for('user.unconfirmed'))
    results = get_activities(g.user_id).name
    results = results.paginate(1, 10, False)
    return render_template('participant/bookmark.html', results=results)


@participant.route('/participant/activity_details', methods=['POST'])
@login_required
def activity_details():
    form = ActivitydetailsForm()

    bookmarks = Bookmark.query.filter_by(owner_id=g.user_id).all()
    if form.validate_on_submit():
        id = int(form.bookmark_id.data)
        bookmark = bookmarks.query.get_or_404(id)
        activity = Activity.query.get_or_404(bookmark.activity_id)
        host = User.query.filter_by(User.name,id=activity.host_id).first()
        return render_template('participant/activity_details.html',
                               name=activity.name,
                               start_date=activity.start_date,
                               end_date=activity.end_date,
                               introduction=activity.introduction,
                               organizer=host,
                               location=activity.location)


@participant.route('/participant/bookmark_delete_activity', methods=['GET', 'POST'])
@login_required
def delete_activity():
    form = DeleteActivityForm()
    bookmarks = Bookmark.query.filter_by(owner_id=g.user_id).all()

    if form.validate_on_submit():
        id = int(form.bookmark_id.data)
        bookmark = bookmarks.query.get_or_404(id)
        db.session.delete(bookmark)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'fail to delete the item!', 'danger')
        else:
            flash(u'success to delete the item!', 'success')
    if form.errors:
        flash(u'fail to delete the item!', 'danger')

    return redirect(url_for('participant/bookmark.html', page=request.args.get('page', 1, type=int)))


@participant.route('/participant/bookmark_delete_activities', methods=['GET', 'POST'])
@login_required
def delete_activities():
    form = DeleteActivitiesForm()
    bookmarks = Bookmark.query.filter_by(owner_id=g.user_id).all()

    if form.validate_on_submit():
        ids = json.loads(form.bookmark_ids.data)
        for item in ids:
            bookmark = bookmarks.query.get_or_404(int(item))
            db.session.delete(bookmark)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'fail to delete the %s items!'%(len(ids)), 'danger')
        else:
            flash(u'success to delete the %s items!' % (len(ids)), 'success')
    if form.errors:
        flash(u'fail to delete these items!', 'danger')

    return redirect(url_for('participant/bookmark.html', page=request.args.get('page', 1, type=int)))


@participant.route('/participant/search_host', methods=['GET', 'POST'])
@login_required
def search_host():
    form = SearchHostForm

    if form.validate_on_submit():
        host_id = User.query.filter_by(id,name=form.host_name).first()
        results = Activity.query.filter_by(host_id=host_id).all().order_by(Activity.start_date.desc())
        results = results.name
        results = results.paginate(1, 10, False)
        return render_template('participant/search.html', results=results,
                               page=request.args.get('page', 1, type=int))
    flash('Invalid hostname!')


@participant.route('/participant/search_activity', methods=['GET', 'POST'])
@login_required
def search_activity():
    form = SearchActivityForm

    if form.validate_on_submit():
        results = Activity.query.filter_by(name=form.activity_name).first()
        results = results.anme
        results = results.paginate(1, 10, False)
        return render_template('participant/search.html', results=results,
                               page=request.args.get('page', 1, type=int))
    flash('Invalid activity name!')


@participant.route('/participant/search_add_activity', methods=['GET', 'POST'])
@login_required
def add_activity():
    form = AddActivityForm()

    if form.validate_on_submit():
        activity_id = int(form.activity_id.data)
        ower_id = g.user.id
        bookmark = Bookmark(ower_id=ower_id,activity_id=activity_id)
        db.session.add(bookmark)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'fail to add the item!', 'danger')
        else:
            flash(u'success to add the item!', 'success')
    if form.errors:
        flash(u'fail to add the item!', 'danger')

    return redirect(url_for('participant/search.html', page=request.args.get('page', 1, type=int)))


@participant.route('/participant/search_add_activities', methods=['GET', 'POST'])
@login_required
def add_activities():
    form = AddActivitiesForm()

    if form.validate_on_submit():
        ids = json.loads(form.activity_ids.data)
        for id in ids:
            activity_id = int(id)
            owner_id = g.user.id
            bookmark = Bookmark(owner_id=owner_id, activity_id=activity_id)
            db.session.add(bookmark)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'fail to add the 5s items!'% (len(ids)), 'danger')
        else:
            flash(u'success to add the %s items!' % (len(ids)), 'success')
    if form.errors:
        flash(u'fail to add these items!', 'danger')

    return redirect(url_for('participant.search.html', page=request.args.get('page', 1, type=int)))












