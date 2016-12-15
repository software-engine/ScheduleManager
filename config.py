#!flask/bin/python
# encoding: utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    def __init__(self):
        pass

#    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'uestc2014'

    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = '25'
    MAIL_USE_TLS = True
    MAIL_USERNAME = '15680781730@163.com'  # os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = 'liupeng527527'  # os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = '15680781730@163.com'  # 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    POSTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass
