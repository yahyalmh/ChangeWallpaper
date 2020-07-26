import os
import time
from abc import abstractmethod

from Utils import Util


class Page:
    tmp_file_name = "tmp"

    def __init__(self):
        self.page_url = ""
        self.image_url = ""
        self.image_name = ""
        self.image_local_address = ""

    def fetch_image(self):
        tmp_page_address = Util.get_instance().get_project_dir() + os.sep + self.tmp_file_name
        try:
            Util.get_instance().request_url(self.page_url, tmp_page_address)

            if not os.path.exists(tmp_page_address):
                return
            elif os.path.getsize(tmp_page_address) <= 0:
                os.remove(tmp_page_address)
                return

            file = open(tmp_page_address, "r+")
            page_content = file.read()
            file.close()

            self.parse_page(page_content)

            self.create_image_name()

            self.download_image()

            return True
        except Exception as e:
            return False
        finally:
            if os.path.exists(tmp_page_address):
                os.remove(tmp_page_address)

    def download_image(self):
        self.image_local_address = Util.get_instance().get_project_dir()\
                                   + os.sep \
                                   + self.image_name
        Util.get_instance().request_url(self.image_url, self.image_local_address)

    def create_image_name(self):
        second = int(round(time.time()))
        image_name = str(second) + ".jpg"
        self.image_name = image_name

    @abstractmethod
    def parse_page(self, page_content):
        pass
