from flask import Blueprint, render_template
from utils.security.secure import Session

from user.models import User
from feeds.models import Feed
from feeds.forms import FeedPostForm

home_app = Blueprint("home_app", __name__)


@home_app.route("/")
def home():

    username = Session.get_session_by_name("username")

    if username:
        user_obj = _get_user_object(username)
        feed_messages = _get_all_feed_messages(user_obj)

        return render_template("users/home/home_feed.html", user=user_obj, feed_messages=feed_messages, form=FeedPostForm())
    return render_template("home/home.html")


def _get_user_object(username):
    return User.objects.filter(username=username).first()


def _get_all_feed_messages(user_obj, feed_per_page=10):
    return Feed.objects.filter(user=user_obj).order_by('-create_date')[:feed_per_page]