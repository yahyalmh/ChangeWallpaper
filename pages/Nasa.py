from lib.bs4 import BeautifulSoup

from pages.Page import Page


class Nasa(Page):

    def __init__(self):
        super(Nasa, self).__init__()
        self.page_url = "https://apod.nasa.gov/apod/astropix.html"

    def parse_page(self, page_content):

        try:
            parsed_html = BeautifulSoup(page_content, "html.parser")
            # html = list(parsed_html.children)[2]
            # body = list(html.children)[3]

            images_tag = parsed_html.find_all('img')
            for tag in images_tag:
                url = tag.get('src')
                if url is not None:
                    self.image_url = self.page_url.split("astropix")[0] + url
                    break
        except Exception as e:
            # print(e)
            pass

    def create_image_name(self):
        temp = self.image_url.split("/")
        image_name = temp[len(temp) - 1]
        self.image_name = image_name
