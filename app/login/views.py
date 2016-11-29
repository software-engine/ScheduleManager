#!flask/bin/python
# encoding: utf-8
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from . import login
from ..models import User
from .forms import LoginForm, PasswordResetForm, PasswordResetRequestForm, ChangePasswordForm, ChangeEmailForm, ChangeNameForm
from flask.ext.login import current_user
from ..register.views import resend_confirmation, send_email
from .. import db


@login.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'login.' \
                and request.endpoint != 'static':
            return redirect(url_for('login.unconfirmed'))


@login.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('login.login'))
    return render_template('login/unconfirmed.html')


@login.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('login.login'))
        flash('Invalid username or password.')
    return render_template('login/login.html', form=form)


@login.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login.login'))


@login.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('login.login'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_password_token()
            if not send_email(user.email, 'Reset Your Password',
                              'login/email/reset_password',
                              user=user, token=token,
                              next=request.args.get('next')):
                flash('Email sending fail')
            else:
                flash('An email with instructions to reset your password has been '
                      'sent to you.')
        return redirect(url_for('login.login'))
    return render_template('login/reset_password.html', form=form)


@login.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('login.login'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('login.login'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('login.login'))
        else:
            return redirect(url_for('login.login'))
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
            return redirect(url_for('login.login'))
        else:
            flash('Invalid password.')
    return render_template("login/change_password.html", form=form)


@login.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_change_email_token(new_email)
            if not send_email(new_email, 'Confirm your email address',
                              'login/email/change_email',
                              user=current_user, token=token):
                flash('Email sending failed')
            else:
                flash('An email with instructions to reset your password has been '
                      'sent to you.')
            return redirect(url_for('login.login'))
        else:
            flash('Invalid email or password.')
    return render_template("login/change_email.html", form=form)


@login.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('login.login'))


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
    return redirect(url_for('login.login'))


