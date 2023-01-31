from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectMultipleField, EmailField, SubmitField, ValidationError
from wtforms.validators import Length, DataRequired, EqualTo
from app.models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Length(4,128)])
    username = StringField('Username',validators=[DataRequired()])
    password2 = PasswordField('Confirm password',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message='Passwords do not match.')])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('You must type your username')])
    password = PasswordField('Password', validators=[DataRequired(), Length(12, 256)])
    remember_me = BooleanField('Keep me logged in.')
    submit = SubmitField('Submit')