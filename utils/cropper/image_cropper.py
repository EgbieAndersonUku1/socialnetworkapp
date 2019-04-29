from PIL import Image
import os
from time import time as time_stamp
from os.path import dirname
from os.path import join



class ImageCropper(object):

    def __init__(self, img_full_path, path_to_save):
        self.img_path = img_full_path
        self.save_as = path_to_save
        self._image = None
        self.image_time_stamp = None

        self._does_image_path_exists(self.img_path)
        self._does_directory_for_image_path_exist(self.save_as)

        self._image = Image.open(self.img_path)

    def create_thumb_nail(self, height=50, width=50):
        self._image.thumbnail((height, width))
        self._image.save(self.save_as)

    def crop_from_centre(self, height=None, width=None):
        """"""
        landscape = 1 > self._image.width / self._image.height
        width_height = self._image.width if landscape else self._image.height

        left = int((self._image.width - width_height) / 2)
        upper = int((self._image.height - width_height) / 2)
        right = int(width_height)
        lower = right

        self._image.crop((left, upper, right, lower))

        if height and width:
            self.resize_image(width, height, save_as_default_name=False)
        self._image.save(self.save_as)

    def resize_image(self, width, height, save_as_default_name=True):
        """"""
        assert (width and height) is not None

        self._image.resize((int(width), int(height)))

        if save_as_default_name:
            img_name = "{}x{}.{}.png".format(width, height, str(time_stamp()))
            img_path = join(dirname(self.img_path), img_name)
        else:
            img_path = self.save_as

        self._image.save(img_path)

    def _does_image_path_exists(self, file_path):
        """"""
        if not self._does_directory_exists_helper(file_path):
            raise FileExistsError("Image path ({}) was not found!!".format(file_path))

    def _does_directory_for_image_path_exist(self, file_path):
        """"""
        if not self._does_directory_exists_helper(directory_path=os.path.dirname(file_path)):
            raise FileExistsError("The directory path ({}) for the file was not found".format(file_path))

    def _does_directory_exists_helper(self, directory_path):
        return os.path.exists(directory_path)




