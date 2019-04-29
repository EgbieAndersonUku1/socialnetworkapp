from flask import Blueprint, abort, redirect, url_for, request, render_template

from relationship import constants
from user.models import User
from relationship.models import Relationship
from user.decorators import login_required
from utils.security.secure import Session, is_safe_url
from utils.emailer.sender import EmailSender
from user.edit.views import IMAGE_SIZE

relationship_app = Blueprint("relationship_app", __name__)


@relationship_app.route("/friends/add/<username>")
@login_required
def add_friend(username):

    logged_user, to_user = _get_requesting_user_and_logged_in_user_obj(username)

    if to_user:
        relationship = Relationship.get_relationship(logged_user, to_user)

        if relationship == constants.REVERSE_PENDING_FRIEND_REQUEST:
            _save_approved_relationship_to_database(logged_user, to_user)
        elif relationship is None and relationship != constants.REVERSED_BLOCK:
            Relationship(from_user=logged_user, to_user=to_user, relationship_type=Relationship.FRIENDS,
                         status=Relationship.PENDING).save()

            _email_user_about_friend_request(logged_user, to_user)

        return _redirect_to_referred_url_if_safe(username)
    abort(404)


@relationship_app.route("/friends/remove/<username>")
@login_required
def remove_friend(username):

    _dissolve_connection_between_users(username)
    return _redirect_to_referred_url_if_safe(username)


@relationship_app.route("/friends/block/<username>")
@login_required
def block(username):

    logged_user, to_user = _get_requesting_user_and_logged_in_user_obj(username)

    if to_user and logged_user:
        Relationship.delete_connection_between_users(to_user, logged_user)
        Relationship(from_user=logged_user, to_user=to_user, relationship_type=Relationship.BLOCKED,
                     status=Relationship.APPROVED).save()
        return _redirect_to_referred_url_if_safe(username)
    abort(404)


@relationship_app.route("/friends/unblock/<username>")
@login_required
def unblock(username):

    logged_user, to_user = _get_requesting_user_and_logged_in_user_obj(username)

    if to_user:
        rel = Relationship.get_relationship(logged_user, to_user)

        if rel == constants.BLOCKED:
            Relationship.delete_connection_between_users(logged_user, to_user)
        return _redirect_to_referred_url_if_safe(username)
    abort(404)


@relationship_app.route("/friends/pendings/<int:page>")
@login_required
def get_all_friend_requests(page=1):
    """"""

    logged_user = User.objects.filter(username=Session.get_session_by_name("username")).first()
    pending = Relationship.objects.filter(to_user=logged_user,
                                          relationship_type=Relationship.FRIENDS,
                                          status=Relationship.PENDING
                                          )

    return render_template("users/profile/pending_friends.html", pending=pending.paginate(page=page, per_page=4),
                           page=page, user=logged_user, image_size=IMAGE_SIZE, relationship_type=None)


@relationship_app.route("/friends/block/<int:page>")
@login_required
def get_all_blocked_people(page=1):

    logged_user = User.objects.filter(username=Session.get_session_by_name("username")).first()
    blocked = Relationship.objects.filter(from_user=logged_user,
                                          relationship_type=Relationship.BLOCKED,
                                          status=Relationship.APPROVED
                                          )

    return render_template("users/profile/blocked_friends.html", blocked=(blocked.paginate(page=page, per_page=16)),
                           page=page, user=logged_user, image_size=IMAGE_SIZE, relationship_type=constants.BLOCKED)


def _dissolve_connection_between_users(username):

    logged_user, to_user = _get_requesting_user_and_logged_in_user_obj("" or username.lower())

    if to_user and _is_there_relationship_between_users(logged_user, to_user):
        Relationship.delete_connection_between_users(logged_user, to_user)


def _get_requesting_user_and_logged_in_user_obj(username_to_find):

    logged_user = User.objects.filter(username=Session.get_session_by_name("username")).first()
    to_user = User.objects.filter(username=username_to_find.lower()).first()

    return logged_user, to_user


def _save_approved_relationship_to_database(logged_user, to_user):

    Relationship(
        from_user=logged_user,
        to_user=to_user,
        relationship_type=Relationship.FRIENDS,
        status=Relationship.APPROVED
    ).save()

    reversed_relationship = Relationship.objects.get(from_user=to_user, to_user=logged_user)
    reversed_relationship.status = Relationship.APPROVED
    reversed_relationship.save()


def _is_there_relationship_between_users(logged_user, to_user):

    relationship_type = Relationship.get_relationship(logged_user, to_user)

    return relationship_type == constants.PENDING_REQUEST or \
           relationship_type == constants.FRIEND_APPROVED or \
           relationship_type == constants.REVERSED_BLOCK or \
           relationship_type == constants.REVERSE_PENDING_FRIEND_REQUEST or \
           relationship_type == constants.FRIENDS_PENDING or constants.BLOCKED


def _redirect_to_referred_url_if_safe(username):
    if is_safe_url(request.referrer):
        return redirect(request.referrer)
    return redirect(url_for("profile_app.profile", username=username))


def _email_user_about_friend_request(logged_user, to_user):

    body_html = render_template("users/mail/relationship/friends_request.html", from_user=logged_user, to_user=to_user)
    email = EmailSender(recipient=to_user.email, subject="Friends requests", content=body_html)
    email.send()