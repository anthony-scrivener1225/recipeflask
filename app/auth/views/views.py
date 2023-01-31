from flask import session, render_template, url_for, redirect, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_smorest import abort
from app.auth import blp as auth
from app import db
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
            and request.blueprint != 'auth' \
                and request.endpoint != 'static' \
                    and request.endpoint != 'main.index':
                        return redirect(url_for('auth.unconfirmed'))
    elif current_user.is_authenticated \
            and not current_user.confirmed \
                and request.endpoint == 'main.index':
                    flash('Account is not confirmed!', category='alert-danger')


@auth.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data) and not user.account_locked:
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        elif user.account_locked:
            flash('Your account has been locked!', category='alert-warning')
            form.data.clear()
            return render_template('login.html', form=form)
        flash('Invalid username or password!', category='alert-danger')
    return render_template('login.html', form=form)


@auth.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first() is None:
            user = User(username=form.username.data, password=form.password.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
    
            msg = Mail(
                subject=f"Account Verification - {user.username}",
                from_email=os.environ.get('MAIL_SENDER'),
                to_emails=[user.email],
                html_content=render_template("welcome_email.html",token=token,username=user.username,port=os.environ.get('PORT'))
            )
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                json_msg = msg.get()
                sg.send(message=json_msg)
            except Exception as e:
                print(e)
            flash('Account was successfully created.', category='alert-success')
            return redirect(url_for('auth.login'))
        else:
            flash('Username or email already registered!', category='alert-warning')
            render_template('register.html', form=form)
    return render_template('register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!', category='alert-success')
        return redirect(url_for('main.index'))
    if not current_user.confirm(token):
        abort(303, message='Token is expired')
    return redirect(url_for('main.index'))

@auth.route('/reconfirm')
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    msg = Mail(
        subject=f"Account Verification - {current_user.username}",
        from_email=os.environ.get('MAIL_SENDER'),
        to_emails=[current_user.email],
        html_content=render_template("welcome_email.html",token=token,username=current_user.username,port=os.environ.get('PORT'))
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        json_msg = msg.get()
        sg.send(message=json_msg)
        flash('New confirmation email sent!', category='alert-warning')
    except Exception as e:
        print(e)
    return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('unconfirmed.html')

@auth.route('/logout')
def logout():
    logout_user()
    flash('You were successfully logged out.', category='alert-success')
    return redirect(url_for('main.index'))