#!flask/bin/python
# encoding: utf-8



from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class RegistrationForm(Form):
    email = StringField('Email', validators=[DeprecationWarning(), Length(1, 64),
                                             Email()])
    name = StringField('Name', validators=[
        DeprecationWarning(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                    'Username must have only letters, '
                                                    'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        DeprecationWarning(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DeprecationWarning()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username already in use.')
