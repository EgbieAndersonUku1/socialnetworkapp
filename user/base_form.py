from flask_wtf import Form
from wtforms import StringField, validators
from wtforms.fields.html5 import EmailField
from wtforms.widgets import TextArea


class BaseUserForm(Form):

    username = StringField("Username", validators=[validators.DataRequired(), validators.length(max=50)])
    email = EmailField("Email", validators=[validators.DataRequired(), validators.Email()])
    first_name = StringField("First name", validators=[validators.DataRequired(), validators.length(max=50)])
    last_name = StringField("Last name", validators=[validators.DataRequired(), validators.length(max=50)])
    bio = StringField("Bio", widget=TextArea(), validators=[validators.Length(max=160)])

