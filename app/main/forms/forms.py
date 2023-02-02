from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from flask_wtf.file import FileRequired, FileField, FileSize, FileAllowed
from flask_login import current_user
from app.models import User
from flask import flash

def existing_email(form, field):
        if User.query.filter_by(email=field.data).first() is not None and field.data != current_user.email:
            flash(f"Email: {field.data} is already registered.", category='alert-warning')
            raise ValidationError(f"Email: {field.data} is already registered.")

def existing_username(form, field):
        if User.query.filter_by(username=field.data).first() is not None and field.data != current_user.username:
            flash(f"Username: {field.data} is already registered.", category='alert-warning')
            raise ValidationError(f"Username: {field.data} is already registered.")

class PasswordReset(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm your password', validators=[EqualTo('password', message='Must match password field'), Length(12,256)])
    submit = SubmitField('Update Password')

class ProfileUpdate(FlaskForm):
    email = EmailField('Update your email', validators=[existing_email])
    email_confirm = EmailField('Confirm new email', validators=[EqualTo('email')])
    username = StringField('Update your username', validators=[existing_username])
    submit = SubmitField('Update Details')

class ProfilePhotoUpload(FlaskForm):
        profile_photo = FileField(
            validators=[
                FileRequired(),
                FileAllowed(["png", "jpg", "jpeg"], "This file is not a valid image !",),
            ]
        )
        submit = SubmitField()