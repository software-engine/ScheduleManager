#!flask/bin/python
# coding: utf
from flask_wtf import Form
from wtforms import StringField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired

class  addactivityform(Form):
    name = StringField('name', validators=[DataRequired()])
    start_time = DateTimeField('start time', format='%m%d%y')
    end_time = DateTimeField('end time', format='%m%d%y')
    location = StringField('location', validators=[DataRequired()])
    introduction = TextAreaField('introduction', validators=[DataRequired()])

class deleteactivityform(Form):
    activity_id = StringField(validators=[DataRequired()])

class deleteactivitysform(Form):
     activity_ids = StringField(validators=[DataRequired()])

class  addscheduleform(Form):
    start_time = DateTimeField('start time', format='%m%d%y')
    end_time = DateTimeField('end time', format='%m%d%y')
    location = StringField('location', validators=[DataRequired()])
    introduction = TextAreaField('introduction', validators=[DataRequired()])

class deletescheduleform(Form):
    schedule_id = StringField(validators=[DataRequired()])

class deleteschedulesform(Form):
    schedule_ids = StringField(validators=[DataRequired()])

class activityscheduleform(addscheduleform):
    act = StringField(validators=[DataRequired()])
