import imghdr
import os
import random

from Utils import Util


class PictureManager:
    os_default_picture_path = "/usr/share/backgrounds"

    def choose_wallpaper(self, is_download_occur, pages_list):
        image_address = None
        if is_download_occur:
            image_address = self.choose_today_images(pages_list)

        if image_address is None or not os.path.exists(image_address):
            image_address = self.choose_default_images()

        return image_address

    def choose_today_images(self, pages_list):
        image_address = None

        if not pages_list or len(pages_list) - 1 <= 0:
            return image_address

        pages_count = len(pages_list) - 1

        for page in pages_list:
            if page and page.image_url != "" and os.path.exists(page.image_local_address):
                break
            if pages_list.index(page) == pages_count:
                return

        while True:
            randint = random.randint(0, pages_count)
            rand_page = pages_list.__getitem__(randint)

            if rand_page and rand_page.image_url != "" and os.path.exists(rand_page.image_local_address):
                image_address = rand_page.image_local_address
                break

        return image_address

    def choose_default_images(self):
        while True:
            rand_image = self.get_rand_image()
            if imghdr.what(rand_image) is not None:
                image_address = rand_image
                break
        return image_address

    def get_rand_image(self):
        def_project_dir = Util.get_instance().get_project_dir()

        if os.path.exists(def_project_dir) and len(os.listdir(def_project_dir)) > 1:
            listdir = os.listdir(def_project_dir)
            random_image = listdir.__getitem__(random.randint(0, len(listdir) - 1))
            image_address = def_project_dir + os.sep + random_image

        elif os.path.exists(self.os_default_picture_path) and len(os.listdir(self.os_default_picture_path)) > 2:
            os_listdir = os.listdir(self.os_default_picture_path)
            random_image = os_listdir.__getitem__(random.randint(0, len(os_listdir) - 1))
            image_address = self.os_default_picture_path + os.sep + random_image

        else:
            def_proj_image_dir = "image"
            def_proj_image_name = "def_wall.jpg"

            image_address = Util.get_instance().get_project_root() \
                            + os.sep \
                            + def_proj_image_dir \
                            + os.sep \
                            + def_proj_image_name

        return image_address
