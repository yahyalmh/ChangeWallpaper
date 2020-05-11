import os
import time
from abc import abstractmethod

import Utils
from Constants import Constants


class Page:
    def __init__(self):
        # self.page_url = url
        self.page_url = ""
        self.image_url = ""
        self.image_name = ""
        self.image_local_address = ""

    def fetch_image_address(self, tmp_page_address):
        Utils.request_url(self.page_url, tmp_page_address)

        if not os.path.exists(tmp_page_address):
            return
        elif os.path.getsize(tmp_page_address) <= 0:
            os.remove(tmp_page_address)
            return

        file = open(tmp_page_address, "r+")
        page_content = file.read()
        file.close()

        self.parse_page(page_content)

        self.crete_image_name()

        self.download_image()

    def download_image(self):
        self.image_local_address = Constants.project_dir + os.sep + self.image_name
        Utils.request_url(self.image_url, self.image_local_address)

    def crete_image_name(self):
        second = int(round(time.time()))
        image_name = str(second) + ".jpg"
        self.image_name = image_name

    @abstractmethod
    def parse_page(self, page_content):
        pass
