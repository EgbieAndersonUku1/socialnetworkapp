from user.base_form import BaseUserForm
from flask_wtf.file import FileField, FileAllowed


class EditForm(BaseUserForm):
    image = FileField("Profile image", validators=[
        FileAllowed(["jpg", "jpeg", "png", "gif"],
                    "Only files with the following extensions .jpg, .jpeg, .png, .gif are allowed")
    ])


