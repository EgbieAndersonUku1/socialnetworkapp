from flask import render_template, abort, Blueprint
from os.path import join

from user.decorators import login_required
from user.edit import constants
from user.edit.form import EditForm
from user.models import User

from utils.common import gen_code as gen_email_verification_code
from utils.emailer.sender import EmailSender
from utils.security.secure import Session
from utils.cropper.image_cropper import ImageCropper
from utils.security.uploader import upload_image_securely_to_server
from settings import UPLOADED_FOLDER


edit_app = Blueprint("edit_app", __name__)

# change height or width for image here not in line 45
_HEIGHT = 100
_WIDTH = 100
IMAGE_SIZE = ("{}x{}".format(_WIDTH, _HEIGHT))


@edit_app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():

    errors = []
    message = None
    email_changed = False
    image_time_stamp = None

    user = User.objects.filter(username=Session.get_session_by_name("username")).first()
   
    if not user:
        abort(404)

    form = EditForm(obj=user)

    if form.validate_on_submit():

        if form.image.data:

            try:
                image_time_stamp, img_path = upload_image_securely_to_server(form, save_to_path=join(UPLOADED_FOLDER, 'users'))
            except FileNotFoundError:
                pass
            else:
                ImageCropper(img_path, path_to_save=_create_img_path(image_time_stamp, user)).crop_from_centre(_WIDTH, _HEIGHT)

        if _has_user_changed_their_username(user, form):
            _if_username_does_not_exist_update_session(form, errors)

        if _has_user_changed_their_email_address(user, form):
            message = constants.EMAIL_CONFIRMATION_MSG
            email_changed = _if_email_not_exists_update_session(errors, form, user)
        
        if not errors:
            form.populate_obj(user)
            
            if image_time_stamp:
                user.profile_image = image_time_stamp
            if not message:
                message = constants.PROFILE_UPDATE_MSG
            if email_changed:
                _email_user_new_confirmation_code_for_changed_email(user)
            user.save()

    return render_template("users/edit/edit.html", form=form, errors=errors, message=message,
                           user=user, image_size=IMAGE_SIZE)


def _if_email_not_exists_update_session(errors, form, user):
    if not _does_email_already_exists(form):
        _update_user_object_with_new_email_and_confirmation_code(form, user)
        return True

    errors.append("The email address already exists")
    return False


def _create_img_path(image_ts, user):

    img_template = "{}.{}.{}.png".format(str(user.id), image_ts, IMAGE_SIZE)
    return join(UPLOADED_FOLDER, 'users', '{}'.format(img_template))


def _has_user_changed_their_username(user, form):
    return user.username != form.username.data


def _has_user_changed_their_email_address(user, form):
    return user.email != form.email.data.lower()


def _does_username_already_exists(form):
    return User.objects.filter(username=form.username.data.lower()).first()


def _does_email_already_exists(form):
    return User.objects.filter(email=form.email.data.lower()).first()


def _update_session_cookie(form):
    Session.remove_session_by_name("username")
    Session.add(session_name="username", session_value=form.username.data.lower())


def _update_user_object_with_new_email_and_confirmation_code(form, user):

    form.email.data = form.email.data.lower()
    user.change_configuration = {
        "new_email": form.email.data.lower(),
        "confirmation_code": str(gen_email_verification_code())
    }

    user.email_confirmed = False
    form.email.data = user.email


def _email_user_new_confirmation_code_for_changed_email(user):
    """"""

    body_html = render_template("users/mail/email/change_email.html", user=user)
    subject = "re: Please confirm your new email address"

    email = EmailSender(user.change_configuration.get("new_email"), subject, content=body_html)
    email.send()


def _if_username_does_not_exist_update_session(form, errors):

    if not _does_username_already_exists(form):
        _update_session_cookie(form)
        form.username.data = form.username.data.lower()
    else:
        errors.append("Username already exists")
