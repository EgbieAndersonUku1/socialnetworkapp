from feeds.models import Feed
from relationship.models import Relationship
from relationship import constants


class MessageProcessor(object):

    def __init__(self, message_obj):
        self._message_obj = message_obj
        self._from_user = message_obj.from_user

    def post_message_to_all_friends_feeds(self):

        friends = self._get_all_my_friends_obj()

        for friend in friends:

            rel_status = Relationship.get_relationship(friend.to_user, self._message_obj.to_user)

            if rel_status != constants.BLOCKED:
                Feed(user=friend.to_user, message=self._message_obj).save()
        return True

    def _get_all_my_friends_obj(self):

        return Relationship.objects.filter(
            from_user=self._from_user,
            relationship_type=Relationship.FRIENDS,
            status=Relationship.APPROVED,
        )
