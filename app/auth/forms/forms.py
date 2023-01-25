from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectMultipleField, EmailField, SubmitField
from wtforms.validators import Length, DataRequired, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(12, 256), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(12, 256)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('You must type your username')])
    password = PasswordField('Password', validators=[DataRequired(), Length(12, 256)])
    remember_me = BooleanField('Keep me logged in.')
    submit = SubmitField('Submit')