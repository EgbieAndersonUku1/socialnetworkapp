from mongoengine import CASCADE
from os.path import join as join_path

from app import db
from utils.common import ms_stamp_humanize, linkify_text
from utils.common import utc_time_stamp_mill_seconds as now
from user.models import User
from settings import STATIC_IMAGE_URL


POST = 1
COMMENT = 2
LIKE = 3

MESSAGE_TYPE = (
    (POST, "Post"),
    (COMMENT, "Comment"),
    (LIKE, "Like")
)


class Message(db.Document):

    from_user = db.ReferenceField(User, db_field="fu", reverse_delete_rule=CASCADE)
    to_user = db.ReferenceField(User, db_field="tu", default=None, reverse_delete_rule=CASCADE)
    post = db.StringField(db_field="pt", max_length=1024)
    live = db.BooleanField(db_field="l", default=None)
    create_date = db.LongField(db_field="c", default=now())
    images = db.ListField(db_field="is", default=None)
    parent = db.ObjectIdField(db_field="p", default=None)
    message_type = db.IntField(db_field="mt", default=POST, choices=MESSAGE_TYPE)

    @property
    def likes(self):
        return Message.objects.filter(parent=self.id, message_type=LIKE).order_by("-create_date")

    @property
    def comments(self):
        return Message.objects.filter(parent=self.id, message_type=COMMENT).order_by("create_date")

    @property
    def text_linkified(self):
        return linkify_text(self.post)

    @property
    def human_timestamp(self):
        return ms_stamp_humanize(self.create_date)

    def post_image_src(self, images_time_stamp, size):
        if self.images:
            profile_img = join_path(STATIC_IMAGE_URL, 'posts', "{}.{}.{}.png".format(self.id, images_time_stamp, size))
            return profile_img.replace("\\", '/') # mostly for windows because windows uses a black slash to save.

    meta = {
        'indexes': [("from_user", "to_user", "-create_date", "message_type", "parent", "live")]
    }