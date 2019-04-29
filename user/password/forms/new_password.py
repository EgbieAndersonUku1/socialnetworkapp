from wtforms import PasswordField, validators

from user.base_password_form import BasePasswordForm


class NewPasswordForm(BasePasswordForm):
    """"""
    current_password = PasswordField("Current Password",
                                     validators=[validators.DataRequired(),
                                                 validators.Length(min=8, max=80)])
