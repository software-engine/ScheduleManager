#!flask/bin/python
# encoding: utf-8

from flask import Blueprint

participant = Blueprint('participant', __name__)

from . import views
