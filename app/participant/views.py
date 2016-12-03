#!flask/bin/python
# encoding: utf-8
from flask import request, render_template, json,redirect, url_for,g, flash
from flask_login import login_required, current_user
from . import participant
from forms import SearchActivityForm, SearchHostForm, DeleteActivityForm,\
    DeleteActivitiesForm, AddActivityForm, AddActivitiesForm
from ..models import User, Bookmark, Activity, get_activities
from .. import db


@participant.before_request
def before_request():
    g.user = current_user


@participant.route('/participant/bookmark_homepage', methods=['POST'])
@login_required
def bookmark_homepage():
    if g.user.is_anonymous or g.user.confirmed:
        return redirect(url_for('user.unconfirmed'))
    results = get_activities(g.user_id)
    results = results.paginate(1, 10, False)
    form1 = SearchActivityForm
    form2 = SearchHostForm
    return render_template('participant/bookmark_homepage.html', results=results,
                           form1=form1, form2= form2)


@participant.route('/participant/activity_details/<id>', methods=['POST'])
@login_required
def activity_details(id):
        activity = Activity.query.get_or_404(int(id))
        host = User.query.filter_by(User.name,id=activity.host_id).first()
        return render_template('participant/activity_details.html',
                               activity=activity, organizer=host)


@participant.route('/participant/back_to_homepage', methods=['POST'])
@login_required
def back_to_homepage():
    return redirect(url_for('participant/bookmark_homepage'))


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
                               form=form, page=request.args.get('page', 1, type=int))
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
                               form=form, page=request.args.get('page', 1, type=int))
    flash('Invalid activity name!')


@participant.route('/participant/search_add_activity', methods=['GET', 'POST'])
@login_required
def add_activity():
    form = AddActivityForm()

    if form.validate_on_submit():
        activity_id = int(form.activity_id.data)
        owner_id = g.user.id
        bookmark = Bookmark(owner_id=owner_id,activity_id=activity_id)
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

    return render_template(url_for('participant/search.html',
                                   page=request.args.get('page', 1, type=int)))


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

    return render_template(url_for('participant/search.html',
                                   page=request.args.get('page', 1, type=int)))


@participant.route('/participant/bookmark_manage', methods=['POST'])
@login_required
def bookmark_manage():
    return redirect(url_for('participant/bookmark_manage.html'))


@participant.route('/participant/bookmark_manage/delete_activity', methods=['GET', 'POST'])
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

    return render_template(url_for('participant/bookmark_manage.html',
                                   page=request.args.get('page', 1, type=int)))


@participant.route('/participant/bookmark_manage/delete_activities', methods=['GET', 'POST'])
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

    return render_template(url_for('participant/bookmark_manage.html',
                                   page=request.args.get('page', 1, type=int)))












