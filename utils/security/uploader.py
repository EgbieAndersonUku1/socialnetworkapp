from os.path import join
from werkzeug.utils import secure_filename
from time import time as time_stamp


def upload_image_securely_to_server(form, save_to_path):

    image_ts = str(time_stamp())

    try:
        filename = secure_filename(form.image.data.filename)
    except AttributeError:
        raise Exception("Form must be a flask web form and not a different type")

    img_path = join(save_to_path, filename)
    form.image.data.save(img_path)

    return image_ts, img_path