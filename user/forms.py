from flask_wtf import Form
from wtforms import validators, StringField, PasswordField


class LoginForm(Form):

    email = StringField('Email address', [validators.DataRequired(), validators.length(min=4, max=80)])
    password = PasswordField("Password", validators=[validators.DataRequired(), validators.length(min=8, max=80)])