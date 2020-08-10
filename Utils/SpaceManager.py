import os
from pathlib import Path

from Utils import Util
from db.Database import Database


class SpaceManager:
    """
    If overall size of all downloaded image in app dir was more that 2G then remove oldest file in order.
    """

    def __init__(self):
        self.space_limit = 2048  # 2 gigabyte(2048 MB), change it to mange space limit
        self.db = Database().get_instance()

    def check_space(self):
        """reduce space tacked by app limit is 2G if necessary"""
        overall_size = self.db.get_dir_size()
        if overall_size > self.space_limit:
            self.remove_oldest_files(overall_size - self.space_limit)
            size = Util.get_instance().get_wall_dir_size()
            self.db.update_dir_size(size)

    def remove_oldest_files(self, overflow_size):
        """delete oldest file base on modified time"""
        paths = sorted(Path(Util.get_instance().project_dir).iterdir(), key=os.path.getmtime)
        tmp_size = 0
        index = 0
        for file in paths:
            print(file)
            if file.exists() and file.is_file():
                tmp_size += (os.path.getsize(Path(file)) / (1024 * 1024))
                index = paths.index(file)
            if tmp_size >= overflow_size:
                break
        for i in range(len(paths) - 1):
            if i <= index:
                file = paths.__getitem__(i)
                if file.exists() and file.is_file():
                    os.remove(Path(file))
            else:
                break

    def remove_duplicate_image(self, page_list):
        for page in page_list:
            if os.path.exists(page.image_local_address):
                if self.db.is_duplicate_file(page.image_name, page.image_hash):
                    os.remove(page.image_local_address)
