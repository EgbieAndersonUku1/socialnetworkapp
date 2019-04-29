from flask import render_template, abort, Blueprint, request
from mongoengine import Q

from relationship import constants
from user.models import User
from relationship.models import Relationship
from utils.security.secure import Session
from user.edit.views import IMAGE_SIZE
from feeds.forms import FeedPostForm
from messages.models import Message, POST


profile_app = Blueprint("profile_app", __name__)


@profile_app.route("/<username>/friends/<int:friends_page_number>", endpoint="profile-friends-page")
@profile_app.route("/<username>/friends", endpoint='profile_friends')
@profile_app.route("/<username>", methods=["GET", "POST"])
def profile(username, friends_page_number=1):
    """profile(str) -> returns render_obj

       Takes a username and if found renders the template else returns
       nothing.

       :param
            username: The username (str) to be rendered if found.
    """

    profile_messages =[]
    user = User.objects.filter(username="" or username.lower()).first()
    logged_user = User.objects.filter(username=Session.get_session_by_name("username")).first()
    display_message_box = False


    if not user:
        abort(404)

    relationship_type = _get_relationship_between_logged_user_and_viewing_user_profile(user)
    friends = _get_all_my_friends(user)
    total_number_of_friends = friends.count()
    friends, current_friends_page_number = _friends_obj_to_friends_pagination_object(friends, friends_page_number)

    if logged_user and relationship_type == constants.VIEWING_YOUR_SELF or relationship_type == constants.FRIEND_APPROVED:
        profile_messages = _get_user_messages(user, num_of_msg_to_return=15)
        display_message_box = True

    return render_template("users/profile/profile.html", user=user, relationship_type=relationship_type,
                           image_size=IMAGE_SIZE,
                           logged_user=user,
                           display_message_box=display_message_box,
                           friends=friends,
                           friends_total=total_number_of_friends,
                           friends_page=current_friends_page_number,
                           form=FeedPostForm(),
                           profile_messages=profile_messages,
                           )


def _get_user_messages(user, num_of_msg_to_return=10):
    """_get_user_messages(user_obj, int) -> mongoengine query object

      A function that when called returns all the messages belonging to the user.
      The function takes an optional parameter with a default value of ten that
      allows the user to set the number of messages returned for a given page.


      :param
        user: The user object which contains all the user's details
        num_of_msg_to_return: The number of messages to return for any given query
    """
    return Message.objects.filter(Q(from_user=user) | Q(to_user=user),
                                  message_type=POST).order_by("-created_date")[:num_of_msg_to_return]


def _friends_obj_to_friends_pagination_object(friends, page):

    friends_page = False

    if "friends" in request.url:
        friends_page = True
        friends = friends.paginate(page=page, per_page=10)
    else:
        friends = friends[:10]

    return friends, friends_page


def _get_all_my_friends(user):
    return Relationship.objects.filter(from_user=user,
                                       relationship_type=Relationship.FRIENDS,
                                        status=Relationship.APPROVED)


def _get_relationship_between_logged_user_and_viewing_user_profile(user):

    username = Session.get_session_by_name("username")

    if username:
        logged_user = User.objects.filter(username=username).first()
        return Relationship.get_relationship(logged_user, user)


def _is_user_viewing_their_own_profile(user):
    """Returns True if the user is viewing their own profile else False"""
    return True if user and Session.get_session_by_name("username") == user.username else False