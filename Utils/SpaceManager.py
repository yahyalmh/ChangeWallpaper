import os
from pathlib import Path

from Constants import Constants


class SpaceManager:
    """
    If overall size of all downloaded image in app dir was more that 2G then remove oldest file in order.
    """
    space_limit = 2  # 2 gigabyte, change it to mange space limit

    def manage(self):
        overall_size = self.get_wall_dir_size()
        if overall_size > self.space_limit:
            self.remove_oldest_files(overall_size - self.space_limit)

    def remove_oldest_files(self, overflow_size):
        """delete oldest file base on modified time"""
        paths = sorted(Path(Constants.project_dir).iterdir(), key=os.path.getmtime)
        tmp_size = 0
        index = 0
        for file in paths:
            print(file)
            if file.exists() and file.is_file():
                tmp_size += (os.path.getsize(file) / (1024 * 1024 * 1024))
                index = paths.index(file)
            if tmp_size >= overflow_size:
                break
        for i in range(len(paths) - 1):
            if i <= index:
                file = paths.__getitem__(i)
                if file.exists() and file.is_file():
                    os.remove(file)
            else:
                break

    def get_wall_dir_size(self):
        """
        this method return overall size of default app path in gigabyte
        :return: Int as size
        """
        size = 0
        for file in os.listdir(Constants.project_dir):
            file = Constants.project_dir + os.sep + file
            if os.path.exists(file) and os.path.isfile(file):
                size += os.path.getsize(file)

        size /= (1024 * 1024 * 1024)
        return round(size, 2)
