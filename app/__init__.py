#!flask/bin/python
# encoding: utf-8


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask_moment import Moment
from config import Config
from flask_mail import Mail

db = SQLAlchemy()
moment = Moment()
bootstrap = Bootstrap()
mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login.user_login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from .login import login as login_blueprint
    app.register_blueprint(login_blueprint)

    from .register import register as register_blueprint
    app.register_blueprint(register_blueprint, url_prefix='/register')

    return app
