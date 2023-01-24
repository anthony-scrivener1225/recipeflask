from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectMultipleField
from wtforms.validators import Length, DataRequired, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(12, 256), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(12, 256)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('You must type your username')])
    password = PasswordField('Password', validators=[DataRequired(), Length(12, 256)])
    stay_logged = BooleanField('Stay Logged in.', )