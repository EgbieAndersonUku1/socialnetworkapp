from flask_wtf import Form, validators
from wtforms import StringField, PasswordField


class LoginForm(Form):
    """This class renders the form's username and password which is needed for the user to sign in"""

    email = StringField('Email address', [validators.DataRequired(), validators.length(min=4, max=80)])
    password = PasswordField("Password", validators=[validators.DataRequired(), validators.length(min=8, max=80)])