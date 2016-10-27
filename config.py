#!flask/bin/python
# encoding: utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    def __init__(self):
        pass

    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'uestc2014'

    @staticmethod
    def init_app(self, app):
        pass
