from flask import Blueprint, render_template, abort, redirect, url_for

from user.models import User
from user.password.forms.forgotten_password import ForgottenPasswordForm, NewPasswordForm
from user.password.forms.reset_password import ResetPasswordForm
from utils.common import gen_code
from utils.emailer.sender import EmailSender
from utils.security.passwd import Password
from utils.security.secure import Session
from user.password import constants

password_app = Blueprint("password_app", __name__)


@password_app.route("/forgotten/password", methods=["GET", "POST"])
def forgotten_password():
    """The function allows the user to reset their forgotten password"""

    message = None
    form = ForgottenPasswordForm()

    if form.validate_on_submit():
        user = User.objects.filter(email=form.email.data.lower()).first()

        if user:
            password_reset_code = gen_code()
            user.change_configuration["password_reset_code"] = password_reset_code
            user.save()
            _email_user_password_reset_code(user)

        message = constants.SUCCESS

    return render_template("users/password/forgotten_password.html", form=form, message=message)


@password_app.route("/password/reset/<username>/<code>", methods=["GET", "POST"])
def reset_password(username, code):
    """reset_password(str, str) -> returns template_obj

       The function takes in a username and code and if the code
       and username match the user's account the user is able to
       reset their password.

       :param
            username: The username associated with the user's account
            code: A code sent to the user's email account
            return: template obj
    """

    user = User.objects.filter(username=username.lower()).first()
    error = None

    if user and user.change_configuration.get("password_reset_code") != code:
        abort(404)

    form = ResetPasswordForm()

    if form.validate_on_submit():

        if user.email_confirmed:
            user.password = Password.hash_password(plain_text_password=form.password.data)
            user.change_configuration.clear()
            user.save()

            _email_user_about_password_changed(user)
            return _logout_user()

        error = constants.EMAIL_VERIFICATION

    return render_template("users/password/reset_password.html", user=user, username=username, code=code, error=error,
                           form=form)


@password_app.route("/password/new", methods=["GET", "POST"])
def change_password():
    """Displays a new password form that enables the user to change their password"""

    form = NewPasswordForm()
    error = None
    user = User.objects.filter(username=Session.get_session_by_name("username").lower()).first()

    if not user:
        abort(404)

    elif form.validate_on_submit():
        if Password.check_password(form.current_password.data, user.password):
            user.password = Password.hash_password(form.password.data)
            user.save()

            _email_user_about_password_changed(user)
            return _logout_user()
        error = constants.INCORRECT_CREDENTIALS
    return render_template("users/password/new_password.html", form=form, error=error)


@password_app.route("/password/changed_password_successful")
def password_successful_changed():
    """A static function that displays a static template which informs the user that
       there have successfully changed their password
     """
    return render_template("users/password/reset_password_success.html")


def _email_user_password_reset_code(user):
    """_email_user_password_reset_code(user_obj) -> returns None

      The function allows the application to email the user a reset code.

      :param
          user: A user objects that contains all the users details e.g username, etc
    """
    _email_helper(user, subject="Re: reset your password", html_link=constants.RESET_PASSWORD_TEMPLATE_LINK)


def _email_user_about_password_changed(user):
    """_email_user_about_password(user_obj) -> returns None

       The function emails the user once there have successful changed their password
    """
    _email_helper(user, subject="re: password changed", html_link=constants.PASSWORD_SUCCESSFUL_TEMPLATE_LINK)


def _email_helper(user, subject, html_link):
    """_email_helper(obj, str, str) -> returns None

        A helper email function that allows the caller of the function to
        send emails

       :param
            user: The user objects which contains all the details pertaining to the user
            subject: The subject for the email
            html_link: The link to render the the user's email
    """
    body = render_template(html_link, user=user)
    subject = subject

    email = EmailSender(recipient=user.email, subject=subject, content=body)
    email.send()


def _logout_user():
    """logs the user out of the application"""
    if Session.get_session_by_name("username"):
        Session.clear_all()
    return redirect(url_for('password_app.password_successful_changed'))
