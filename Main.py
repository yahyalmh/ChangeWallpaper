import os
import random
import subprocess
from datetime import datetime
from os.path import expanduser

import Utils
from Constants import Constants
from db.Database import Database
from pages import *
from pages.Page import Page
import imghdr


class Main:
    tmp_page_address = ""
    project_dir = ""

    def __init__(self):
        self.setup_files()
        self.db = Database().create_database()

    def main(self):
        old_date = self.db.get_date()
        today_date = datetime.date(datetime.now())

        if old_date != str(today_date):
            all_pages = [cls() for cls in Page.__subclasses__()]
            for page in all_pages:
                page.fetch_image_address(self.tmp_page_address)
            self.db.inset_today_date()

            rand_page = all_pages.__getitem__(random.randint(0, len(all_pages)-1))
            if rand_page.image_name != "" and os.path.exists(rand_page.image_local_address):
                image_address = rand_page.image_local_address
            else:
                image_address = self.get_random_image()
        else:
            image_address = self.get_random_image()

        self.run_change_wallpaper_script(image_address)
        if os.path.exists(self.tmp_page_address):
            os.remove(self.tmp_page_address)

    def run_change_wallpaper_script(self, image_address):
        try:
            bash_abs_path = str(Utils.get_project_root()) + os.sep + "changeWall.sh"
            subprocess.check_call([str(bash_abs_path), str(image_address)])
        except Exception as e:
            pass

    def get_random_image(self):
        while True:
            rand_image = Utils.choose_rand_image()
            if imghdr.what(rand_image) is not None:
                image_address = rand_image
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
