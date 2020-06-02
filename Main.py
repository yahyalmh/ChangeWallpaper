import os
import subprocess
import sys
from datetime import datetime
from os.path import expanduser

from Utils import Util
from Utils.PictureManager import PictureManager
from pages import *
from Utils.SpaceManager import SpaceManager
from cron.Scheduler import Scheduler
from bash import *
from db.Database import Database
from pages.Page import Page


class Main:

    def __init__(self):
        self.bash_proj_dir = "bash"
        self.default_dir_name = "wallpaper"
        self.bash_file_name = "changeWall.sh"
        self.bat_file_name = "changeWall.bat"

        self.setup_files()
        self.all_pages = []
        self.spaceManager = SpaceManager()
        self.db = Database().create_database()
        self.pictureManager = PictureManager()

    def main(self):
        try:
            old_date = self.db.get_date()
            today_date = datetime.date(datetime.now())

            if old_date != str(today_date):
                self.all_pages = [cls() for cls in Page.__subclasses__()]
                print(len(self.all_pages))
                for page in self.all_pages:
                    page.fetch_image()

                self.db.inset_today_date()

                image_address = self.pictureManager.get_random_image(self.all_pages)

                if image_address is None or not os.path.exists(image_address):
                    image_address = self.pictureManager.get_default_random_image()

                self.spaceManager.check_space()  # reduce space tacked by app limit is 2G if necessary
            else:
                image_address = self.pictureManager.get_default_random_image()

            self.set_wallpaper_with_bash(image_address)

        except Exception as e:
            print(e)
            pass

    def set_wallpaper_with_bash(self, image_address):
        try:
            os_platform = sys.platform
            script_path = Util.get_instance().get_project_root() \
                          + os.sep \
                          + self.bash_proj_dir
            if os_platform.__contains__("linux"):
                script_path += os.sep + self.bash_file_name
            elif os_platform.__contains__("win32"):
                script_path += os.sep + self.bat_file_name

            subprocess.check_call([str(script_path), str(image_address)])

        except Exception as e:
            print(e)
            pass

    def setup_files(self):
        home = expanduser("~")
        project_dir = home + os.sep + self.default_dir_name
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        Util.get_instance().set_project_dir(project_dir)


if __name__ == '__main__':
    Main().main()
    Scheduler().schedule()
