from flask import render_template, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth import blp
from app.auth.forms import LoginForm, RegistrationForm



@blp.route('/login')
def login():
    form = LoginForm()
    # User Class database build out
    # create login html page
    # return render_template('login.html', form=form)
    pass

@blp.route('register')
def register():
    form = RegistrationForm
    # User Class database build out
    # create registration html
    # return render_template('registration.html', form=form)
    