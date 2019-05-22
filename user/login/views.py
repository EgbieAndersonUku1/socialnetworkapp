from flask import request, render_template, Blueprint, redirect, url_for

from user.login import errors
from user.forms import LoginForm
from user.models import User
from utils.security.passwd import Password
from utils.security.secure import Session
from user.decorators import is_user_already_logged_in
from utils.security.secure import is_safe_url

login_app = Blueprint('login_app', __name__)


@login_app.route("/login", methods=["GET", "POST"])
@is_user_already_logged_in
def login():
    """The login function allow the user entry into the application
       depending on whether their password is correct or not.
    """

    form = LoginForm()
    error = None

    _set_next_variable_to_session_if_found()

    if form.validate_on_submit():

        user = User.objects.filter(email=form.email.data).first()

        if not user:
            error = errors.INCORRECT_CREDENTIALS
        else:
            if not _is_email_address_confirmed(user):
                error = errors.EMAIL_VERIFICATION
            elif Password.check_password(form.password.data, user.password):

                Session.add(session_name="username", session_value=user.username.lower())
                return redirect(url_for("home_app.home"))
            else:
                error = errors.INCORRECT_CREDENTIALS
    return render_template("users/login/login.html", error=error, form=form)


def _set_next_variable_to_session_if_found():
    """A private function that checks if there is a referral url
       link and sets it to session if found.
    """

    if request.method == "GET" and request.args.get("next"):
        Session.add("next", session_value=request.args.get("next"))


def _redirect_page_to_referral_url_if_found():
    """A private helper function that redirects the current page to referral url page"""
    url = Session.remove_session_by_name("next")

    if url and is_safe_url(url):
        return redirect(url)
    return "user logged in"


def _is_email_address_confirmed(user):
    """A helper function that checks whether the user has successful verified
       their email address
    """
    return user.email_confirmed is True
