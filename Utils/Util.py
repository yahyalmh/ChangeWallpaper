import hashlib
import os
import urllib
from pathlib import Path
from urllib.request import urlopen
import ssl


class Util:
    instance = None
    project_dir = ""

    def set_project_dir(self, path):
        self.project_dir = path

    def get_project_dir(self):
        return self.project_dir

    def request_url(self, url, address):
        """Download a url to given address"""
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            res = urllib.request.urlopen(url, timeout=10)
            if res.getcode():
                urllib.request.urlretrieve(url, address)
        except Exception as e:
            raise e

    def get_project_root(self):
        """Returns project root folder."""
        return str(Path(__file__).parent.parent)

    def get_wall_dir_size(self):
        """
        this method return overall size of default app path in kilobyte
        :return: Int as size
        """
        size = 0
        for file in os.listdir(self.get_project_dir()):
            file = self.get_project_dir() + os.sep + file
            if os.path.exists(file) and os.path.isfile(file):
                size += os.path.getsize(file)

        size /= (1024 * 1024)
        return round(size, 2)

    @staticmethod
    def md5(address):
        sha_hash = hashlib.sha1()  # use SHA1
        with open(address, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                sha_hash.update(chunk)
        return sha_hash.hexdigest()


def get_instance():
    if Util.instance is None:
        Util.instance = Util()
    return Util.instance
