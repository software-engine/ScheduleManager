#!flask/bin/python
# encoding: utf-8
from flask import Blueprint
hosts = Blueprint('hosts',__name__)
from .import views