#!flask/bin/python
# encoding: utf-8

from app.register import register
from app.register.forms import RegistrationForm
from ..models import User
from flask import redirect, url_for, flash, render_template, Flask, request, current_app
from app import db
from flask.ext.login import current_user
from flask.ext.login import login_required
from threading import Thread
from flask_mail import Message
from app import mail
from flask_login import login_user


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


@register.route('/user_register', methods=['GET', 'POST'])
def user_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name=form.name.data,
                    password=form.password.data,
                    identity=form.role.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        email_url = 'http://mail.' + form.email.data.split('@', 1)[-1]
        token = user.generate_confirmation_token()
        try:
            send_email(user.email, 'Confirm Your Account',
                       'register/email/confirm', user=user, token=token)
            flash('A confirmation email has been sent to you by email.')
            return render_template('login/unconfirmed.html', user=user, email_url=email_url)
        except:
            flash('Email sending failed and the  email is wrong')
            return render_template('login/unconfirmed.html', user=user, email_url=email_url)
    return render_template('register/user_register.html', form=form)


@register.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.is_anonymous:
        flash(u'请先登录再验证')
        return redirect(url_for('login.user_login'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('register.resend_confirmation'))
    if current_user.identity == 'par':
        return redirect(url_for('participant.homepage'))
    else:
        return redirect(url_for('hosts.index'))


@register.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    if not send_email(current_user, 'register/email/confirm',
                      'Confirm Your Account', user=current_user, token=token):
        flash('Email sending failed')
    else:
        flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('login.user_login'))
