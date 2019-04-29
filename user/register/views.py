from werkzeug.utils import redirect

from utils.common import gen_code as gen_register_confirmation_code
from flask import Blueprint, render_template, abort, url_for

from user.models import User
from user.register.form import RegisterForm
from utils.security.passwd import Password
from utils.emailer.sender import EmailSender
from user.decorators import is_user_already_logged_in
from utils.security.secure import is_safe_url

registration_app = Blueprint("registration_app", __name__)


@registration_app.route("/register", methods=["GET", "POST"])
@is_user_already_logged_in
def register():
    """"""

    form = RegisterForm()

    if form.validate_on_submit():
        user = _save_form_data_to_database(form, registration_code=str(gen_register_confirmation_code()))
        # _email_user_registration_confirmation_code(recipient_email=form.email.data, user=user)
        if is_safe_url("login_app.login"):
            return redirect(url_for("login_app.login"))
    return render_template("users/register/register.html", form=form)


def _email_user_registration_confirmation_code(recipient_email, user):
    """"""
    subject = "Welcome to the social network"
    body_html = render_template("users/mail/register/register.html", user=user)

    email = EmailSender(recipient=recipient_email, subject=subject, content=body_html)
    email.send()


def _save_form_data_to_database(form, registration_code):
    """"""

    user = User(
        username=form.username.data.lower(),
        password=Password.hash_password(form.password.data),
        email=form.email.data.lower(),
        first_name=form.username.data,
        last_name=form.last_name.data,
        change_configuration={

        }
    )

    # delete for testing purpose
    user.email_confirmed = True
    user.save()
    return user

    # user = User(
    #     username=form.username.data.lower(),
    #     password=Password.hash_password(form.password.data),
    #     email=form.email.data.lower(),
    #     first_name=form.username.data,
    #     last_name=form.last_name.data,
    #     change_configuration = {
    #         "new_email": form.email.data.lower(),
    #         "confirmation_code": registration_code,
    #     }
    # )

    user.save()
    return user


@registration_app.route("/confirm/<username>/<code>", methods=["GET", "POST"])
def confirm_registration_code(username, code):
    """"""

    user = User.objects.filter(username=username.lower()).first()

    # if user and user.change_configuration and user.change_configuration.get("confirmation_code") == code:
    #
    #     user.email = user.change_configuration.get("new_email")
    #     user.email_confirmed = True
    #     del user.change_configuration['confirmation_code']
    #     del user.change_configuration["new_email"]
    #     user.save()
    #     return render_template("users/mail/email/email_confirmed.html")
    #
    # abort(404)
