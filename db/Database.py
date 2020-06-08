import os
import sqlite3
from datetime import datetime

from Utils import Util


class Database:
    db_name = "wallpaperDB.db"

    def __init__(self):
        self.DB_address = os.path.dirname(os.path.realpath(__file__)) + os.sep + self.db_name

    def get_instance(self):
        if not os.path.isfile(self.DB_address):
            self.create_db()
        return self

    def create_db(self):
        conn = sqlite3.connect(self.DB_address)
        cur = conn.cursor()
        cur.execute("create table wallpaper (date text, space_size int)")
        conn.commit()
        cur.close()
        conn.close()

        wall_dir_size = Util.get_instance().get_wall_dir_size()
        self.insert_data('', wall_dir_size)

    def insert_data(self, date, dir_size):
        conn = sqlite3.connect(self.DB_address)
        cur = conn.cursor()
        values = (date, dir_size)
        cur.execute("insert into wallpaper (date, space_size) values(?,?)", values)
        conn.commit()
        cur.close()
        conn.close()

    def update_data(self, date, dir_size):
        conn = sqlite3.connect(self.DB_address)
        cur = conn.cursor()
        values = (date, dir_size)
        cur.execute("update wallpaper set date = ?, space_size = ?", values)
        conn.commit()
        cur.close()
        conn.close()

    def read_data(self):
        conn = sqlite3.connect(self.DB_address)
        cur = conn.cursor()
        cur.execute("select * from wallpaper;")
        result = cur.fetchall()
        conn.close()
        return result

    def get_date(self):
        old_date = (self.read_data()[0])[0]
        if old_date is not None and old_date != "":
            return old_date
        return ""

    def get_dir_size(self):
        dir_size = (self.read_data()[0])[1]
        if dir_size is not None and dir_size != "":
            return dir_size
        return 0

    def update_dir_size(self, size):
        conn = sqlite3.connect(self.DB_address)
        cur = conn.cursor()
        values = (size,)
        cur.execute("update wallpaper set space_size=?;", values)
        conn.commit()
        cur.close()
        conn.close()

    def update_db(self, pages_list):
        if not pages_list or len(pages_list) - 1 <= 0:
            return

        overall_size = self.calc_overall_size(pages_list)

        self.update_data(datetime.date(datetime.now()), overall_size)

    def calc_overall_size(self, pages_list):
        size = 0
        for page in pages_list:
            if page and os.path.exists(page.image_local_address) and os.path.isfile(page.image_local_address):
                size += os.path.getsize(page.image_local_address)
        size /= (1024 * 1024)
        overall_size = self.get_dir_size() + size
        return round(overall_size, 2)
