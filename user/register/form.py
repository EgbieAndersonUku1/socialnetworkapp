from wtforms.validators import ValidationError

from user.models import User
from utils.matcher.match import match_str_using_reg
from user.base_form import BaseUserForm
from user.base_password_form import BasePasswordForm


_PATTERN_TO_MATCH = "^[a-zA-Z0-9_-]{4,80}$"


class RegisterForm(BaseUserForm, BasePasswordForm):

    def validate_username(form, field):
        """"""
        if User.objects.filter(username=field.data).first():
            raise ValidationError("Username already exists")

        if not match_str_using_reg(reg_expression_pattern=_PATTERN_TO_MATCH, str_to_match=field.data):
            raise ValidationError("Invalid username")

    def validate_email(form, field):
        """"""
        if User.objects.filter(email=field.data).first():
            raise ValidationError("Email already exists")
