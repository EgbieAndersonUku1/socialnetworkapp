from os.path import join as join_path

from app import db
from settings import STATIC_IMAGE_URL
from utils.common import time_stamp


class User(db.Document):
    """The database uses mongoEngine and when called saves the user's details to the database"""

    username = db.StringField(db_field="u", required=True, unique=True)
    password = db.StringField(db_field="p", required=True)
    email = db.EmailField(db_field="e", required=True, unique=True)
    first_name = db.StringField(db_field="fn", max_length=50)
    last_name = db.StringField(db_field="ln", max_length=50)
    created = db.IntField(db_field="c", default=time_stamp())
    bio = db.StringField(db_field="b", max_length=150)
    email_confirmed = db.BooleanField(db_field="ec", default=False)
    change_configuration = db.DictField(db_field="cc")
    profile_image = db.StringField(db_field="pi", default=None)

    def profile_image_src(self, size):
        """profile_image_src(str) -> return img path

           The profile function allows the user of the application to fetch the path
           of the desired image which will then be rendered to by the application

          :param
             size: Takes a string relating to the size of image
        """
        if self.profile_image:
            return join_path(STATIC_IMAGE_URL, 'users', "{}.{}.{}.png".format(self.id, self.profile_image, size)).replace("\\", '/')
        return join_path(STATIC_IMAGE_URL, "users", "no_profile.jpg").replace("\\", '/')


    meta = {
        "indexes": ["username", "email", "-created"]
    }