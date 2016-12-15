#!flask/bin/python
# encoding: utf-8

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp


class SearchByHostForm(Form):
    host_name = StringField('host_name', validators=[
        DataRequired(message=u'这里必须填哦'), Length(1, 64, message=u'必须1到64位字符串'),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, message=u'必须由1到64位以字母开头的数字和字母组成')])


class SearchByActivityForm(Form):
    activity_name = StringField('activity_name', validators=[DataRequired(message=u'这里必须填哦')])


class DeleteActivityForm(Form):
    activity_id = StringField('activity_id', validators=[DataRequired(message=u'这里必须填哦')])


class DeleteActivitiesForm(Form):
    activity_ids = StringField('activity_ids', validators=[DataRequired(message=u'这里必须填哦')])


class AddActivityForm(Form):
    activity_id = StringField('activity_id', validators=[DataRequired(message=u'这里必须填哦')])


class AddActivitiesForm(Form):
    activity_ids = StringField('activity_ids', validators=[DataRequired(message=u'这里必须填哦')])
