import urllib
from pathlib import Path
from urllib.request import urlopen


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
            res = urllib.request.urlopen(url)
            if res.getcode():
                urllib.request.urlretrieve(url, address)
        except Exception as e:
            pass

    def get_project_root(self) -> Path:
        """Returns project root folder."""
        return Path(__file__).parent.parent


def get_instance():
    if Util.instance is None:
        Util.instance = Util()
    return Util.instance
