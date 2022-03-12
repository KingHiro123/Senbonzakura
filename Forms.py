from sqlite3 import Date
from wtforms import Form, SubmitField, StringField, RadioField, SelectField, PasswordField, TextAreaField, EmailField, DateField, validators
from wtforms.validators import Length, EqualTo, ValidationError

class Signup_Form(Form):
    username = StringField('Username', [validators.DataRequired(), Length(min=2)])
    email = EmailField('Email',[validators.Email(), validators.DataRequired()])
    birthday = DateField('Birthday', format='%Y-%m-%d')
    password = PasswordField('Password', [validators.DataRequired(), Length(min=8)])
    confirmpass = PasswordField("Repeat Password", [validators.DataRequired(), Length(min=8), EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Sign Up')

class Login_Form(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Log In')