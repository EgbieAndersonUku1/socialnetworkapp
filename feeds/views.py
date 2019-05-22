from time import time as time_stamp
from flask import Blueprint, request, abort, render_template, url_for
from os.path import join, dirname
from werkzeug.utils import secure_filename, redirect

from settings import UPLOADED_FOLDER
from utils.cropper.image_cropper import ImageCropper
from user.decorators import login_required
from user.models import User
from feeds.models import Feed
from messages.models import Message, POST, COMMENT, LIKE
from feeds.forms import FeedPostForm
from messages.message_processer import MessageProcessor
from utils.security.secure import Session, redirect_to_referred_url_if_safe
from user.edit.views import IMAGE_SIZE


feed_app = Blueprint("feed_app", __name__)

_HEIGHT, _WIDTH = 200, 200


@feed_app.route("/message/add", methods=["GET", "POST"])
@login_required
def add_message():
    """The add message function allows the user to add message to the application"""

    form = FeedPostForm()

    if request.method == "POST":

        logged_user, to_user = _get_requesting_user_and_logged_in_user_obj()

        if form.validate_on_submit():

            uploaded_post_images_path_list = _upload_all_uploaded_images_securely_to_server()

            if to_user == logged_user:  # if this is a self post
                to_user = None

            message_obj = _process_post_form_messages(form, logged_user, to_user)
            _process_post_form_images(message_obj, uploaded_post_images_path_list)

            return redirect_to_referred_url_if_safe(redirect_page_to_url="home_app.home")


@feed_app.route("/message/edit/<message_id>", methods=["GET", "POST"])
@login_required
def edit_message(message_id):
    """edit_message(str) -> render tmp object

       The function allows the user edit their message.

       :param
          message_id: The message id allows the user to edit the message
                      associated with that id.
    """

    message_obj = Message.objects.filter(id=message_id).first()

    form = FeedPostForm(obj=message_obj)

    if form.validate_on_submit():
        form.populate_obj(message_obj)
        message_obj.save()
        return redirect_to_referred_url_if_safe(redirect_page_to_url="home_app.home")
    return render_template("feeds/message.html", message=message_obj, form=form)


@feed_app.route("/message/<message_id>", methods=["GET", "POST"])
def message(message_id):

    form = FeedPostForm()
    message = Message.objects.filter(id=message_id).first()

    if not message:
        abort(404)

    if message and message.parent:
        abort(404)

    if form.validate_on_submit() and Session.get_session_by_name("username"):

        from_user = User.objects.get(username=Session.get_session_by_name("username"))
        Message(from_user=from_user, post=form.post.data, message_type=COMMENT, parent=message_id).save()
        return redirect(url_for("feed_app.message", message_id=message.id))

    return render_template("feeds/message.html", message=message, form=form)


@feed_app.route("/like/<message_id>", methods=["GET", "POST"])
@login_required
def like_message(message_id):

    message = Message.objects.filter(id=message_id).first()

    if not message:
        abort(404)

    if message and message.parent:
        abort(404)

    from_user = User.objects.get(username=Session.get_session_by_name("username"))
    existing_like = Message.objects.filter(parent=message_id, message_type=LIKE, from_user=from_user).count()

    if not existing_like:
        Message(from_user=from_user, to_user=message.from_user, message_type=LIKE, parent=message_id).save()
    return redirect(url_for('feed_app.message', message_id=message.id))


def _upload_all_uploaded_images_securely_to_server():

    post_images_path_list = []
    uploaded_files = request.files.getlist('images')

    if uploaded_files and uploaded_files[0].filename != "":

        for file in uploaded_files:

            filename = secure_filename(file.filename)
            file_path = join(UPLOADED_FOLDER, "posts", filename)
            file.save(file_path)
            post_images_path_list.append(file_path)

    return post_images_path_list


def _process_post_form_images(message_obj, post_images_list):

    if len(post_images_list):
        images = []

        for file_path in post_images_list:
            file_name_path, timestamp = _create_img_path(file_path, message_id=message_obj.id)

            ImageCropper(file_path, file_name_path).resize_image(width=_WIDTH, height=_HEIGHT, save_as_default_name=False)
            images.append({"time_stamp": timestamp, "w": str(_WIDTH)})

        message_obj.images = images
        message_obj.save()


def _process_post_form_messages(form, logged_user, to_user):

    msg = Message(from_user=logged_user, to_user=to_user, post=form.post.data, message_type=POST).save()
    Feed(user=logged_user, message=msg).save()
    MessageProcessor(message_obj=msg).post_message_to_all_friends_feeds()

    return msg


def _get_requesting_user_and_logged_in_user_obj():

    logged_user = User.objects.filter(username=Session.get_session_by_name("username")).first()
    to_user = User.objects.filter(username=request.values.get("to_user")).first()

    return logged_user, to_user


def _create_img_path(img_path, message_id):

    timestamp = time_stamp()
    directory_path = dirname(img_path) # get the directory path from the image path
    img_template = "{}.{}.{}.png".format(str(message_id), timestamp, IMAGE_SIZE)

    return join(directory_path, '{}'.format(img_template)), timestamp