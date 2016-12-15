#!flask/bin/python
# encoding: utf-8
from flask import render_template, redirect, request, url_for, flash, current_app
from flask.ext.login import login_user, logout_user, login_required
from . import login
from ..models import User
from .forms import *
from flask.ext.login import current_user
from ..register.views import send_email
from .. import db


# @login.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         if not current_user.confirmed \
#                 and request.endpoint[:5] != 'login.' \
#                 and request.endpoint != 'static':
#             return redirect(url_for('login.unconfirmed'))
#
#
# @login.route('/unconfirmed')
# def unconfirmed():
#     if current_user.is_anonymous or current_user.confirmed:
#         return redirect(url_for('login.user_login'))
#     return render_template('login/unconfirmed.html')


@login.route('/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            if not user.confirmed:
                email_url = 'http://mail.' + form.email.data.split('@', 1)[-1]
                return render_template('login/unconfirmed.html', user=user, email_url=email_url)
            if user.identity == 'par':
                return redirect(url_for('participant.homepage'))
            else:
                return redirect(url_for('hosts.index'))
        flash(u'检查一下是不是邮箱或者密码输错了')
    return render_template('login/user_login.html', form=form)


@login.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login.user_login'))


@login.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_password_token()
            try:
                send_email(user.email, 'Reset Your Password',
                           'login/email/change_password',
                           user=user, token=token)
                flash('An email with instructions to reset your password has been '
                      'sent to you.')
                return redirect(url_for('login.user_login'))
            except:
                flash('Email sending fail')
    return render_template('login/reset_password_request.html', form=form)


@login.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('the email is not registered')
            return redirect(url_for('login.user_login'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('login.user_login'))
        else:
            flash('unsuccessful')
            return redirect(url_for('login.user_login'))
    return render_template('login/reset_password.html', form=form)


@login.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            # if current_user.identity == 'par':
            #     return redirect(url_for('participant.homepage'))
            # else:
            #     return redirect(url_for('hosts.index'))
            return redirect(url_for('login.user_login'))
        else:
            flash('Invalid password.')
    return render_template("login/change_password.html", form=form)


@login.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.new_email.data
            token = current_user.generate_change_email_token(new_email)
            try:
                send_email(form.old_email.data, 'Confirm your email address',
                           'login/email/change_email',
                           user=current_user, token=token)
                flash('An email with instructions to reset your password has been '
                      'sent to you.')
                return redirect(url_for('login.user_login'))
            except:
                flash('Email sending failed')
    return render_template("login/change_email.html", form=form)


@login.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    if current_user.identity == 'par':
        return redirect(url_for('participant.homepage'))
    else:
        return redirect(url_for('hosts.index'))


@login.route('/change-name', methods=['GET', 'POST'])
@login_required
def change_name():
    form = ChangeNameForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_name = form.name.data
            if current_user.change_name(new_name):
                flash('Your name has been update.')
            else:
                flash('Invalid request.')
    return render_template("login/change_name.html", form=form)
