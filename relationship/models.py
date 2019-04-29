from mongoengine import CASCADE

from app import db
from relationship import constants
from utils.common import time_stamp
from user.models import User


class Relationship(db.Document):

    FRIENDS = 1
    BLOCKED = -1

    RELATIONSHIP_TYPE = (
        (FRIENDS, "friends"), (BLOCKED, "Blocked"),
    )

    PENDING = -1
    APPROVED = 1

    STATUS_TYPE = (
        (PENDING, "Pending"), (APPROVED, "Approved"),
    )

    from_user = db.ReferenceField(User, db_field="fu", reverse_delete_rule=CASCADE)
    to_user = db.ReferenceField(User, db_field="tu", reverse_delete_rule=CASCADE)
    relationship_type = db.IntField(db_field="rt", choices=RELATIONSHIP_TYPE)
    status = db.IntField(db_field="s", choices=STATUS_TYPE)
    request_date = db.IntField(db_field="rd", default=time_stamp())
    approved_date = db.IntField(db_field="ad", default=0)

    def is_friend(self, user):
        return self.get_relationship(user, self.to_user) if user else None

    @staticmethod
    def get_relationship(from_user, to_user):

        if from_user == to_user:
            return constants.VIEWING_YOUR_SELF

        rel = Relationship.objects.filter(from_user=from_user, to_user=to_user).first()
        status = None

        if not rel:
            status = Relationship._is_there_already_a_pending_connection_between_users(to_user, from_user)
        elif rel.relationship_type == Relationship.FRIENDS:
            status = Relationship._check_request(rel)
        elif rel.relationship_type == Relationship.BLOCKED:
            status = constants.BLOCKED
        return status

    @staticmethod
    def delete_connection_between_users(to_user, from_user):
        """"""
        Relationship.objects.filter(from_user=from_user, to_user=to_user).delete()
        Relationship.objects.filter(from_user=to_user, to_user=from_user).delete() # delete reversed relationship

    @staticmethod
    def _check_request(relationship_obj):

        status = None

        if relationship_obj.status == Relationship.PENDING:
            status = constants.FRIENDS_PENDING
        elif relationship_obj.status == Relationship.APPROVED:
            status = constants.FRIEND_APPROVED
        return status

    @staticmethod
    def _is_there_already_a_pending_connection_between_users(to_user, from_user):

        reverse_relationship = Relationship.objects.filter(from_user=to_user, to_user=from_user).first()

        if not reverse_relationship:
            return None
        elif reverse_relationship.status == Relationship.PENDING:
            return constants.REVERSE_PENDING_FRIEND_REQUEST
        elif reverse_relationship.status == Relationship.BLOCKED:
            return constants.REVERSED_BLOCK

    meta = {
        'indexes': [('from_user', 'to_user'), ('from_user', 'to_user', 'relationship_type', 'status')]
    }