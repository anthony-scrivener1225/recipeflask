from app.main import blp 
from flask import abort, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from app.models import Recipe
from app import db
import os
from config import basedir
from app.main.forms import PasswordReset,ProfileUpdate, PhotoUpload
from app.auth.views.views import role_access


@blp.route('/adminpanel')
@login_required
@role_access(2)
def test_admin():
    return render_template('adminpanel.html')


@blp.route('/')
def index():
    return render_template('index.html')

@blp.route('/myaccount', methods=['GET'])
@login_required
def my_account():
    recipes = Recipe.query.filter_by(created_by=current_user.id).all()
    return render_template('myaccount.html',user=current_user, recipes=recipes)


@blp.route('/updateprofilephoto', methods=["POST"])
def update_profile_photo():
    photo_form = PhotoUpload()
    if photo_form.is_submitted():
        uploaded_file = photo_form.file.data
        if uploaded_file.filename != '':
            sep_file = os.path.splitext(uploaded_file.filename)[1]
            current_user.avatar = str(current_user.id)+sep_file
            uploaded_file.save(basedir+'/app/static/avatars/'+current_user.avatar)
            db.session.add(current_user)
            db.session.commit()
            flash('Profile photo updated.', category='alert-success')
            return redirect(url_for('main.my_account'))
        else:
            raise ValueError('File name not added!')
    else:
        flash('Invalid file upload', category='alert-warning')
        return redirect(url_for('main.update_account'))


@blp.route('/updateprofileinfo', methods=["POST"])
def update_profile_info():
    profile_form = ProfileUpdate()
    email_change = False
    if profile_form.validate_on_submit():
        if current_user.email != profile_form.email.data:
            current_user.email = profile_form.email.data
            current_user.confirmed = False
            email_change = True
        elif current_user.username != profile_form.username.data:
            current_user.username = profile_form.username.data
        db.session.add(current_user)
        db.session.commit()
        flash(('Profile successfully updated.' if not email_change else 'A confirmation email was sent to your new email!'), category='alert-success')
        return redirect(url_for('main.my_account'))
    else:
        flash("Incorrect Password Data", category='alert-warning')
        return redirect(url_for('main.update_account'))

@blp.route('/updatepassword', methods=["POST"])
def update_password():
    pass_form = PasswordReset()
    if pass_form.is_submitted():
        current_user.password = pass_form.password.data
        db.session.add(current_user)
        db.session.commit()
        flash('Password successfully changed.', category='alert-success')
        return redirect(url_for('main.my_account'))
    else:
        flash("Incorrect Password Data", category='alert-warning')
        return redirect(url_for('main.update_account'))

@blp.route('/updateaccount', methods=["GET"])
@login_required
def update_account():
    pass_form = PasswordReset()
    profile_form = ProfileUpdate()
    update_profile_photo = PhotoUpload()
    return render_template('updateaccount.html', pass_form=pass_form,profile_form=profile_form,update_profile_photo=update_profile_photo, user=current_user)