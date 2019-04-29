from functools import wraps
from flask import request, redirect, url_for

from utils.security.secure import Session


def login_required(f):
    @wraps(f)
    def login(*args, **kwargs):
        if Session.get_session_by_name("username") is None:
            return redirect(url_for('login_app.login', next=request.url))
        return f(*args, **kwargs)
    return login


def is_user_already_logged_in(f):
    @wraps(f)
    def is_user_logged_in(*args, **kwargs):
        if Session.get_session_by_name("username"):
            return redirect(url_for("profile_app.profile", username=Session.get_session_by_name("username")))
        return f(*args, **kwargs)
    return is_user_logged_in
