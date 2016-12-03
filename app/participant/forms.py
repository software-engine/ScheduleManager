#!flask/bin/python
# encoding: utf-8
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired


class SearchHostForm(Form):
    host_name = StringField('host_name', validators=[DataRequired])
    submit = SubmitField('Search Host')


class SearchActivityForm(Form):
    activity_name = StringField('activity_name', validators=[DataRequired])
    submit = SubmitField('Search Activity')


class DeleteActivityForm(Form):
    bookmark_id = StringField(validators=[DataRequired])
    submit = SubmitField('Delete')


class DeleteActivitiesForm(Form):
    bookmark_ids = StringField(validators=[DataRequired])
    submit = SubmitField('Batch Delete')


class AddActivityForm(Form):
    activity_id = StringField(validators=[DataRequired])
    submit = SubmitField('Add')


class AddActivitiesForm(Form):
    activity_ids = StringField(validators=[DataRequired])
    submit = SubmitField('Batch Add')







