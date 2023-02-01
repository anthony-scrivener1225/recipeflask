from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, StringField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from flask_login import current_user
from app.models import User

def existing_email(form, field):
    if User.query.filter_by(email=field.data).first() is not None and field.data != current_user.email:
        raise ValidationError("Email already in use.")
    else:
        return True

def existing_username(form, field):
    if User.query.filter_by(username=field.data).first() is not None and field.data != current_user.username:
        raise ValidationError("Username is already in use.")
    else:
        return True

class PasswordReset(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm your password', validators=[EqualTo('password', message='Must match password field'), Length(12,256)])
    submit = SubmitField('Update Password')

class ProfileUpdate(FlaskForm):
    email = EmailField('Update your email',default=current_user.email, validators=[existing_email])
    email_confirm = EmailField('Confirm new email',default=current_user.email, validators=[EqualTo('email')])
    username = StringField('Update your username', default=current_user.username, validators=[existing_username])