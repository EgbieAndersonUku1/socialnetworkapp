from flask_wtf import Form
from wtforms import PasswordField, validators
from wtforms.fields.html5 import EmailField

from user.base_password_form import BasePasswordForm


class ForgottenPasswordForm(Form):
    """"""
    email = EmailField("Email", validators=[validators.DataRequired(), validators.Email()])


class NewPasswordForm(BasePasswordForm):
    """"""
    current_password = PasswordField("Current Password", validators=[validators.DataRequired(),
                                                                     validators.Length(min=8, max=80)])




