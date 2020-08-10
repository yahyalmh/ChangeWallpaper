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
        self.vbs_file_name = "changeWall.vbs"

        self.setup_files()
        self.all_pages = []
        self.spaceManager = SpaceManager()
        self.db = Database().get_instance()
        self.pictureManager = PictureManager()

    def main(self):
        try:
            image_downloaded_count = self.download_new_wall()

            if image_downloaded_count > 0:
                self.spaceManager.remove_duplicate_image(self.all_pages)
                self.spaceManager.check_space()
                self.db.update_db(self.all_pages)

            image_address = self.pictureManager.choose_wallpaper(image_downloaded_count, self.all_pages)
            self.set_wallpaper(image_address)

        except Exception as e:
            pass

    def download_new_wall(self):
        image_downloaded_count = 0

        old_date = self.db.get_date()
        today_date = datetime.date(datetime.now())

        if old_date != str("today_date"):

            self.all_pages = [cls() for cls in Page.__subclasses__()]

            for page in self.all_pages:
                is_successful = page.fetch_image()

                if is_successful:
                    image_downloaded_count += 1

        return image_downloaded_count

    def set_wallpaper(self, image_address):
        if image_address is None or not os.path.exists(image_address):
            return

        try:
            os_platform = sys.platform
            script_path_dir = Util.get_instance().get_project_root() + os.sep + self.bash_proj_dir

            if os_platform.__contains__("linux"):
                linux_bash_path = script_path_dir + os.sep + self.bash_file_name
                subprocess.check_call([str(linux_bash_path), str(image_address)])

            elif os_platform.__contains__("win32"):
                win_bat_path = script_path_dir + os.sep + self.bat_file_name
                vbs_path = script_path_dir + os.sep + self.vbs_file_name
                subprocess.run([str(vbs_path), str(win_bat_path), str(image_address)], shell=True)
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
