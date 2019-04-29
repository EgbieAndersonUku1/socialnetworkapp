from flask import Blueprint

from utils.security.secure import Session, redirect_to_referred_url_if_safe

logout_app = Blueprint("logout_app", __name__)


@logout_app.route("/logout", methods=["GET", "POST"])
def logout():
    """"""
    username = Session.get_session_by_name("username")
    Session.clear_all()
    return redirect_to_referred_url_if_safe(username)

