from app.main import blp 
from flask import abort, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from app.models import Recipe
from app import db
from app.main.forms import PasswordReset,ProfileUpdate


@blp.route('/')
def index():
    return render_template('index.html')

@blp.route('/myaccount')
@login_required
def my_account():
    recipes = Recipe.query.filter_by(created_by=current_user.id).all()
    return render_template('myaccount.html',user=current_user, recipes=recipes)


@blp.route('/updateaccount', methods=["POST","GET"])
@login_required
def update_account():
    pass_form = PasswordReset()
    profile_form = ProfileUpdate()
    if pass_form.validate_on_submit():
        current_user.password = pass_form.new_pwd.data
        db.session.add(current_user)
        db.session.commit()
        flash('Password successfully changed.', category='alert-success')
        return redirect(url_for('main.my_account'))
    elif profile_form.validate_on_submit():
        if current_user.email != profile_form.email.data:
            current_user.email = profile_form.email.data
            current_user.confirmed = False
        elif current_user.username != profile_form.username.data:
            current_user.username = profile_form.username.data
        db.session.add(current_user)
        db.session.commit()
        flash('Profile successfully updated.', category='alert-success')
        return redirect(url_for('main.my_account'))
    return render_template('updateaccount.html', pass_form=pass_form,profile_form=profile_form, user=current_user)