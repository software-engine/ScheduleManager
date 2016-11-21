#!flask/bin/python
# encoding: utf-8
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired


class ACdetailsForm(Form):
    AC = StringField(validators=[DataRequired])

class SearchHForm(Form):
    host = StringField('host', validators=[DataRequired])


class SearchACForm(Form):
    activity = StringField('activity', validators=[DataRequired])


class DeleteItemForm(Form):
    item = StringField(validators=[DataRequired])


class DeleteItemsForm(Form):
    items = StringField(validators=[DataRequired])


class AddItemForm(Form):
    item = StringField(validators=[DataRequired])


class AddItemsForm(Form):
    items = StringField(validators=[DataRequired])







