from flask_wtf import Form
from wtforms import PasswordField, validators


class BasePasswordForm(Form):

    password = PasswordField("Password", validators=[validators.DataRequired(), validators.length(min=8, max=80),
                                                     validators.EqualTo("confirm", message="The passwords does not match")])
    confirm = PasswordField("Repeat password")
