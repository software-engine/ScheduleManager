#!flask/bin/python
# encoding: utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(message=u'还没输入邮箱'), Length(1, 128),
                                             Email(message=u'格式不对哦')])
    name = StringField('Name', validators=[
        DataRequired(message=u'这里必须填哦'), Length(1, 64, message=u'必须1到64位字符串'),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, message=u'必须由1到64位以字母开头的数字和字母组成')])
    password = PasswordField('Password', validators=[
        DataRequired(message=u'密码都不填怎么行'), EqualTo('password2', message=u'密码不一致')])
    password2 = PasswordField('Confirm password', validators=[DataRequired(message=u'这里必须填哦')])
    role = SelectField('Role', choices=[('par', 'Participant'), ('host', 'host')], coerce=str,
                       validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱已经注册')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError(u'该用户名已存在')
