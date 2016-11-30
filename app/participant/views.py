#!flask/bin/python
# encoding: utf-8
from flask import request,render_template,json,redirect,url_for,g,flash
from flask_login import login_required,current_user
from . import participant
from forms import SearchACForm,SearchHForm,DeleteItemsForm,\
    DeleteItemForm,AddItemsForm,AddItemForm,ACdetailsForm
from ..models import User,Bookmark,Activity,get_activities
from .. import db

@participant.before_request
def before_request():
    g.user = current_user


@participant.route('/participant/mypage',methods=['POST'])
@login_required
def mypage():
    if g.user.is_anonymous or g.user.confirmed:
        return redirect(url_for('user.uncomfirmed'))
    results = get_activities(g.user_id)
    results = results.paginate(1,10,False)
    return render_template('participant/mypage.html',results=results)


@participant.route('/participant/ACdetails',methods=['POST'])
@login_required
def ACdetails():
    form = ACdetailsForm()
    bookmarks = Bookmark.query.filter_by(owner_id=g.user_id).all()
    if form.validate_on_submit():
        id = int(form.AC.data)
        bk = bookmarks.query.get_or_404(id)
        AC = Activity.query.filter_by(bk.activity_id == Activity.id).all()
        Or = User.query.join(User.name,AC.host_id == User.id).first()
        return render_template('participant/ACdetails.html',
                               name = AC.name,
                               start_date = AC.start_date,
                               end_date = AC.end_date,
                               introduction = AC.introduction,
                               organizer = Or,
                               location = AC.location)


@participant.route('/participant/bookmark_delete_items', methods=['GET', 'POST'])
@login_required
def delete_item():
    form = DeleteItemForm()
    bookmarks = Bookmark.query.filter_by(owner_id=g.user_id).all()

    if form.validate_on_submit():
        id = int(form.item.data)
        bk = bookmarks.query.get_or_404(id)
        db.session.delete(bk)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'fail to delete the item！', 'danger')
        else:
            flash(u'success to delete the item！' ,'success')
    if form.errors:
        flash(u'fail to delete the item！', 'danger')

    return redirect(url_for('participant/bookmark.html', page=request.args.get('page', 1, type=int)))


@participant.route('/participant/bookmark_delete_items', methods=['GET', 'POST'])
@login_required
def delete_items():
    form = DeleteItemsForm()
    bookmarks = Bookmark.query.filter_by(owner_id=g.user_id).all()

    if form.validate_on_submit():
        ids = json.loads(form.items.data)
        for item in ids:
            bk = bookmarks.query.get_or_404(int(item))
            db.session.delete(bk)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'fail to delete these items！', 'danger')
        else:
            flash(u'success to detele the %s items！' % (len(ids)), 'success')
    if form.errors:
        flash(u'fail to delete these items！', 'danger')

    return redirect(url_for('participant/bookmark.html',page=request.args.get('page', 1, type=int)))


@participant.route('/participant/searchH',methods=['GET','POST'])
@login_required
def searchH():
    form = SearchHForm

    if form.validate_on_submit():
        results = Activity.query.filter_by(Activity.name,
                                       (form.host==User.name)).all().order_by(Activity.start_date.desc())
        results = results.paginate(1,10,False)
        return render_template('participant/search.html',results=results)
    flash('Inviad hostname!')


@participant.route('/participant/searchAC',methods=['GET','POST'])
@login_required
def searchAC():
    form = SearchACForm
    if form.validate_on_submit():
        results = Activity.query.filter_by(Activity.name,
                                       (form.activity==Activity.name)).order_by(Activity.start_date.desc())
        results = results.paginate(1,10,False)
        return render_template('participant/search.html',results=results)
    flash('Inviad activityname!')


@participant.route('/participant/search_add_item', methods=['GET', 'POST'])
@login_required()
def add_article():
    form = AddItemForm()

    if form.validate_on_submit():
        activity_id = int(form.item.data)
        ower_id = g.user.id
        bookmark = Bookmark(ower_id=ower_id,activity_id=activity_id)
        db.session.add(bookmark)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'fail to add the item！', 'danger')
        else:
            flash(u'success to add the item！' ,'success')
    if form.errors:
        flash(u'fail to add the item！', 'danger')

    return redirect(url_for('participant/search.html', page=request.args.get('page', 1, type=int)))


@participant.route('/participant/search_add_items', methods=['GET', 'POST'])
@login_required
def add_items():
    form = AddItemsForm()

    if form.validate_on_submit():
        ids = json.loads(form.items.data)
        for id in ids:
            activity_id = int(id)
            ower_id = g.user.id
            bookmark = Bookmark(ower_id=ower_id,activity_id=activity_id)
            db.session.add(bookmark)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'fail to add these items！', 'danger')
        else:
            flash(u'success to add the %s items！' % (len(ids)), 'success')
    if form.errors:
        flash(u'fail to add these items！', 'danger')

    return redirect(url_for('participant.search.html',page=request.args.get('page', 1, type=int)))












