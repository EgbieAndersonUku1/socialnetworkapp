from mongoengine import CASCADE

from app import db
from utils.common import utc_time_stamp_mill_seconds as timestamp
from user.models import User
from messages.models import Message


class Feed(db.Document):

    user = db.ReferenceField(User, db_field="u", reverse_delete_rule=CASCADE)
    message = db.ReferenceField(Message, db_field="m", reverse_delete_rule=CASCADE)
    create_date = db.LongField(db_field="cd", default=timestamp())

    meta = {
        "indexes": [("user", "-create_date")]
    }