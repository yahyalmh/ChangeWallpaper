import os
import random
import urllib
from pathlib import Path
from urllib.request import urlopen

from Constants import Constants


def request_url(url, address):
    try:
        res = urllib.request.urlopen(url)
        if res.getcode():
            urllib.request.urlretrieve(url, address)
    except Exception as e:
        pass


def get_project_root() -> Path:
    """Returns project root folder."""
    return Path(__file__).parent.parent


def choose_rand_image():
    if os.path.exists(Constants.project_dir) and len(os.listdir(Constants.project_dir)) > 2:
        listdir = os.listdir(Constants.project_dir)
        random_image = listdir.__getitem__(random.randint(0, len(listdir) - 1))
        image_address = Constants.project_dir + os.sep + random_image
    elif os.path.exists(Constants.default_picture_path) and len(os.listdir(Constants.default_picture_path)) > 2:
        os_listdir = os.listdir(Constants.default_picture_path)
        random_image = os_listdir.__getitem__(random.randint(0, len(os_listdir) - 1))
        image_address = Constants.default_picture_path + os.sep + random_image
    else:
        image_address = str(get_project_root()) + os.sep + "image" + os.sep + "def_wall.png"

    return image_address
