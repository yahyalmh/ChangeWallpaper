import re

from lib.bs4 import BeautifulSoup

from pages.Page import Page


class Bing(Page):

    def __init__(self):
        super(Bing, self).__init__()
        self.extract_image_name = ""
        self.page_url = "https://www.bing.com/"

    def parse_page(self, page_content):
        try:
            parsed_html = BeautifulSoup(page_content, "html.parser")
            html = list(parsed_html.children)[1]
            body = list(html.children)[1]

            # for link in body.find_all('div'):

            wall_tag = body.find('div', class_='img_cont')
            style = wall_tag.get('style')
            if style is not None and "background-image" in style:
                image_address = style.split("/")[1].split("jpg")[0]
                self.image_url = self.page_url + image_address + "jpg"

            # image_name_id = "iotd_title"
            self.extract_image_name = body.find('a', class_='title').getText()

        except Exception as e:
            pass

    def create_image_name(self):
        if self.extract_image_name != "":
            self.extract_image_name = re.sub('[^\w\-_\. ]', '', self.extract_image_name)
            # self.extract_image_name = re.sub(r"\s+", '_', self.extract_image_name)

            if len(self.extract_image_name) > 150:
                self.image_name = self.extract_image_name[:150]
            else:
                self.image_name = self.extract_image_name

            self.image_name += ".jpg"
        else:
            super(Bing, self).create_image_name()
