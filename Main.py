import imghdr
import os
import random
import subprocess
from datetime import datetime
from os.path import expanduser

from Constants import Constants
from Utils import Utils
from pages import *
from Utils.SpaceManager import SpaceManager
from db.Database import Database
from pages.Page import Page


class Main:
    tmp_page_address = ""
    project_dir = ""
    all_pages = []

    def __init__(self):
        self.setup_files()
        self.db = Database().create_database()

    def main(self):
        old_date = self.db.get_date()
        today_date = datetime.date(datetime.now())

        if old_date != str(today_date):
            self.all_pages = [cls() for cls in Page.__subclasses__()]
            for page in self.all_pages:
                page.fetch_image_address(self.tmp_page_address)
            self.db.inset_today_date()

            image_address = self.get_today_rand_image()
            if image_address is None or not os.path.exists(image_address):
                image_address = self.get_default_random_image()

            SpaceManager().check_space()  # reduce space tacked by app limit is 2G if necessary
        else:
            image_address = self.get_default_random_image()

        self.run_change_wallpaper_script(image_address)
        if os.path.exists(self.tmp_page_address):
            os.remove(self.tmp_page_address)

    def run_change_wallpaper_script(self, image_address):
        try:
            bash_abs_path = str(Utils.get_project_root()) + os.sep + "bash" + os.sep + "changeWall.sh"
            subprocess.check_call([str(bash_abs_path), str(image_address)])
        except Exception as e:
            pass

    def get_default_random_image(self):
        while True:
            rand_image = Utils.choose_rand_image()
            if imghdr.what(rand_image) is not None:
                image_address = rand_image
                break
        return image_address

    def get_today_rand_image(self):
        image_address = None

        if not self.all_pages:
            return image_address

        while True:
            randint = random.randint(0, len(self.all_pages) - 1)
            rand_page = self.all_pages.__getitem__(randint)

            if rand_page and rand_page.image_name != "" and os.path.exists(rand_page.image_local_address):
                image_address = rand_page.image_local_address
                break

        return image_address

    def setup_files(self):
        home = expanduser("~")
        dir_name = "wallpaper"
        self.project_dir = home + os.sep + dir_name
        if not os.path.exists(self.project_dir):
            os.makedirs(self.project_dir)

        Constants.project_dir = self.project_dir
        tmp_file_name = "tmp.html"
        self.tmp_page_address = self.project_dir + os.sep + tmp_file_name


if __name__ == '__main__':
    Main().main()
