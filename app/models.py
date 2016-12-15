#!flask/bin/python
# encoding: utf-8

import hashlib
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from flask import current_app, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(64), unique=True)
    identity = db.Column(db.String(5))
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))
    confirmed = db.Column(db.Boolean, default=False)
    activities = db.relationship('Activity', backref='host', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    def gravatar(self, size=40, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def generate_reset_password_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'password': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('password') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    def generate_change_email_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        if data.get('email') != self.id:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        db.session.commit()
        return True

    def change_name(self, new_name):
        if self.query.filter_by(name=new_name).first() is not None:
            return False
        self.name = new_name
        db.session.add(self)
        db.session.commit()
        return True

    def __repr__(self):
        return '<User %r>' % self.name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(15))
    introduction = db.Column(db.Text(140))
    location = db.Column(db.String(30))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    update_flag = db.Column(db.Boolean, default=False)
    schedules = db.relationship('Schedule', backref='activity', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Activity, self).__init__(**kwargs)

    def update(self, new_name=name, new_location=location, new_introduction=introduction,
               new_start_date=start_date, new_end_date=end_date):
        self.name = new_name
        self.introduction = new_introduction
        self.location = new_location
        self.start_date = new_start_date
        self.end_date = new_end_date
        self.update_flag = True


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    information = db.Column(db.Text(140))
    location = db.Column(db.String(30))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super(Schedule, self).__init__(**kwargs)

    def update(self, new_information=information, new_location=location,
               new_start_time=start_time, new_end_time=end_time):
        self.information = new_information
        self.location = new_location
        self.start_time = new_start_time
        self.end_time = new_end_time
        Activity.query.filter_by(id=self.activity_id).first().update_flag = True


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))

    def __init__(self, **kwargs):
        super(Bookmark, self).__init__(**kwargs)

    def add(self):
        bookmark = Bookmark.query.filter_by(activity_id=self.activity_id).first()
        if bookmark is not None:
            pass
        else:
            db.session.add(self)


def get_activities(bookmarks):
    activities = []
    for bookmark in bookmarks:
        activities.append(Activity.query.filter_by(id=bookmark.activity_id).first())
    return activities
