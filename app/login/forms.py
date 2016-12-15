#!flask/bin/python
# encoding: utf-8
# coding:utf-8

from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from flask.ext.wtf import Form
from wtforms import PasswordField, StringField
from ..models import User
from wtforms import ValidationError


class PasswordResetRequestForm(Form):
    email = StringField('Email',
                        validators=[DataRequired(message=u'不输入邮箱就到不了下一步哦'), Length(1, 128), Email(message=u'邮箱格式好像不对')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'邮箱没注册')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[DataRequired(message=u'没有邮箱我们不知道你谁哦'), Length(1, 128),
                                             Email(message=u'邮箱格式好像不对')])
    password = PasswordField('New Password', validators=[
        DataRequired(message=u'改密码怎么能不写密码呢'), EqualTo('password2', message=u'密码必须一致')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'邮箱没注册')


class LoginForm(Form):
    email = StringField(u'邮箱', validators=[DataRequired(message=u'邮箱都不写怎么登陆'), Length(1, 128), Email(message=u'格式不对哦')])
    password = PasswordField(u'密码', validators=[DataRequired(message=u'请输入密码')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'邮箱没注册')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[DataRequired(message=u'是不是忘了密码了')])
    password = PasswordField('New password', validators=[
        DataRequired(message=u'新密码一定要输的'), EqualTo('password2', message='密码不一致')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])


class ChangeEmailForm(Form):
    old_email = StringField('Old Email', validators=[DataRequired(message=u'不写邮箱怎么改'), Length(1, 128),
                                                     Email(message=u'邮箱格式错啦!!')])
    new_email = StringField('New Email', validators=[DataRequired(message=u'新邮箱要输的'), Length(1, 128),
                                                     Email(message=u'邮箱格式错啦!!')])
    password = PasswordField('password', validators=[DataRequired(message=u'请输入密码验证')])

    def validate_old_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'邮箱没注册')


class ChangeNameForm(Form):
    name = StringField('Name', validators=[
        DataRequired(message=u'新名字必须输入'), Length(1, 20, message=u'必须是1到20位'),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, message=u'必须是以英文字母开头的1到64位只含字母和数字的字符串')])
    password = PasswordField('Password', validators=[DataRequired(message=u'密码忘输啦!!')])

    def validate_name(self, field):
        if User.query.filter_by(name=field.data):
            raise ValidationError(u'该用户名已经存在')
