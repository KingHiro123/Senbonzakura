from sqlite3 import Date
from wtforms import Form, StringField, RadioField, SelectField, PasswordField, TextAreaField, EmailField, DateField, validators
from wtforms.validators import Length, EqualTo

class Signup_Form(Form):
    username = StringField('Username', [validators.DataRequired(), Length(min=2)])
    email = EmailField('Email',[validators.Email(), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    birthday = DateField('Birthday', format='%Y-%m-%d')
    password = PasswordField('Password', [validators.DataRequired, Length(min=8)])
    confirmpass = PasswordField("Repeat Password", [validators.DataRequired(), Length(min=8), EqualTo('password', message="Passwords must match.")])