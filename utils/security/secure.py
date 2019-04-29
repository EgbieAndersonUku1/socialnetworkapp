from flask import session
from flask import request, url_for, redirect
from urllib.parse import urlparse, urljoin


def is_safe_url(target):

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_to_referred_url_if_safe(username=None, redirect_page_to_url="profile_app.profile"):

    if username is None:
        username = Session.get_session_by_name("username")
    if is_safe_url(request.referrer):
        return redirect(request.referrer)
    return redirect(url_for(redirect_page_to_url, username=username))


class Session(object):

    @staticmethod
    def add(session_name, session_value):
        session[session_name] = session_value

    @classmethod
    def get_session_by_name(cls, session_name):
        return session.get(session_name)

    @classmethod
    def remove_session_by_name(cls, session_name):

        if cls.get_session_by_name(session_name):
            return session.pop(session_name)

    @staticmethod
    def clear_all():
        Session.remove_session_by_name("username")

