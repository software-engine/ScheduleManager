#!flask/bin/python
# encoding: utf-8

from flask_wtf import Form
from wtforms import StringField, TextAreaField, DateTimeField, DateField
from wtforms.validators import DataRequired, Length, ValidationError


class BigThan(object):
    def __init__(self, fieldname):
        self.fieldname = fieldname

    def __call__(self, form, field):
        other = form[self.fieldname]
        if field.data < other.data:
            raise ValidationError(u'结束时间必须大于开始时间')


class AddActivityForm(Form):
    name = StringField('name', validators=[DataRequired(message=u'必填项'), Length(1, 30, message=u'必须1到15位字符串')])
    start_date = DateField('start_date', validators=[DataRequired(message=u'必填项')])
    end_date = DateField('end_date', validators=[DataRequired(message=u'必填项'), BigThan('start_date')])
    location = StringField('location', validators=[DataRequired(message=u'必填项'), Length(1, 15, message=u'必须1到15位字符串')])
    introduction = TextAreaField('introduction',
                                 validators=[DataRequired(message=u'必填项'), Length(1, 140, message=u'不能超过140字')])


class DeleteActivityForm(Form):
    activity_id = StringField(validators=[DataRequired()])


class DeleteActivitiesForm(Form):
    activity_ids = StringField(validators=[DataRequired()])


class AddScheduleForm(Form):
    start_time = DateTimeField('start_time', format=u'%Y-%m-%d %H:%M', validators=[DataRequired(message=u'必填项')])
    end_time = DateTimeField('end_time', format=u'%Y-%m-%d %H:%M',
                             validators=[DataRequired(message=u'必填项'), BigThan('start_time')])
    location = StringField('location', validators=[DataRequired(message=u'必填项'), Length(1, 30, message=u'不能超过30字符')])
    information = TextAreaField('introduction',
                                validators=[DataRequired(message=u'必填项'), Length(1, 140, message=u'不能超过140字符')])


class DeleteScheduleForm(Form):
    schedule_id = StringField(validators=[DataRequired()])


class DeleteSchedulesForm(Form):
    schedule_ids = StringField(validators=[DataRequired()])


class ActivityScheduleForm(AddScheduleForm):
    act = StringField(validators=[DataRequired()])
