import os
import sqlite3
from datetime import datetime

from Utils import Util


class Database:
    db_name = "wallpaperDB.db"
    config_table_name = "config"
    wall_table_name = "wallpaper"

    def __init__(self):
        self.DB_address = os.path.dirname(os.path.realpath(__file__)) + os.sep + self.db_name

    def get_instance(self):
        if not self.is_last_db_version():
            if os.path.isfile(self.DB_address):
                os.remove(self.DB_address)
            self.create_db()

        return self

    def create_db(self):
        conn = sqlite3.connect(self.DB_address)
        cur = conn.cursor()
        cur.execute("create table {config_table_name} (date text, space_size int)".format(
            config_table_name=self.config_table_name))
        cur.execute(
            "create table {wall_table_name} (image_name text, hash text)".format(wall_table_name=self.wall_table_name))
        conn.commit()
        cur.close()
        conn.close()

        wall_dir_size = Util.get_instance().get_wall_dir_size()
        self.insert_config_data('', wall_dir_size)

    def update_db(self, pages_list):
        if not pages_list or len(pages_list) - 1 <= 0:
            return

        overall_size = self.calc_overall_size(pages_list)

        self.update_config_data(datetime.date(datetime.now()), overall_size)

        for page in pages_list:
            if not self.is_duplicate_entry(page.image_name, page.image_hash):
                self.insert_wall_data(page.image_name, page.image_hash)

    def insert_config_data(self, date, dir_size):
        conn = sqlite3.connect(self.DB_address)
        cur = conn.cursor()
        values = (date, dir_size)
        cur.execute("insert into {config_table_name}  (date, space_size) values(?,?)".format(
            config_table_name=self.config_table_name), values)
        conn.commit()
        cur.close()
        conn.close()

    def update_config_data(self, date, dir_size):
        conn = sqlite3.connect(self.DB_address)
        cur = conn.cursor()
        values = (date, dir_size)
        cur.execute("update {config_table_name} set date = ?, space_size = ?".format(
            config_table_name=self.config_table_name), values)
        conn.commit()
        cur.close()
        conn.close()

    def read_config_data(self):
        conn = sqlite3.connect(self.DB_address)
        cur = conn.cursor()
        cur.execute("select * from {config_table_name};".format(config_table_name=self.config_table_name))
        result = cur.fetchall()
        cur.close()
        conn.close()
        return result

    def get_date(self):
        old_date = (self.read_config_data()[0])[0]
        if old_date is not None and old_date != "":
            return old_date
        return ""

    def get_dir_size(self):
        dir_size = (self.read_config_data()[0])[1]
        if dir_size is not None and dir_size != "":
            return dir_size
        return 0

    def update_dir_size(self, size):
        conn = sqlite3.connect(self.DB_address)
        cur = conn.cursor()
        values = (size,)
        cur.execute("update config set space_size=?;", values)
        conn.commit()
        cur.close()
        conn.close()

    def insert_wall_data(self, file_name, file_hash):
        conn = sqlite3.connect(self.DB_address)
        cursor = conn.cursor()
        values = (file_name, file_hash)
        cursor.execute("insert into {wall_table_name} values(?,?)".format(wall_table_name=self.wall_table_name), values)
        conn.commit()
        cursor.close()
        conn.close()

    def is_duplicate_file(self, file_name, file_hash):
        conn = sqlite3.connect(self.DB_address)
        cursor = conn.cursor()
        values = (file_hash,)
        cursor.execute("select * from {wall_table_name} where hash=?;".format(wall_table_name=self.wall_table_name),
                       values)
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if result is None or result == "" or len(result) <= 0:
            return False

        item_list = [item for tup in result for item in tup]
        if item_list[0] != file_name and item_list[1] == file_hash:
            return True

        return False

    def is_duplicate_entry(self, file_name, file_hash):
        conn = sqlite3.connect(self.DB_address)
        cursor = conn.cursor()
        values = (file_hash,)
        cursor.execute("select * from {wall_table_name} where hash=?;".format(
            wall_table_name=self.wall_table_name),
                       values)
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        if result is not None and result != "" and len(result) > 0:
            return True
        return False

    def calc_overall_size(self, pages_list):
        size = 0
        for page in pages_list:
            if page and os.path.exists(page.image_local_address) and os.path.isfile(page.image_local_address):
                size += os.path.getsize(page.image_local_address)
        size /= (1024 * 1024)
        overall_size = self.get_dir_size() + size
        return round(overall_size, 2)

    def is_last_db_version(self):
        if not os.path.isfile(self.DB_address):
            return False
        conn = sqlite3.connect(self.DB_address)
        cursor = conn.cursor()
        cursor.execute("select name from sqlite_master where type='table'")
        result = cursor.fetchall()
        cursor.close()
        conn.cursor()
        if result is None or result == "" or len(result) < 2:
            return False

        table_name_list = [item for tup in result for item in tup]

        if not table_name_list.__contains__(self.config_table_name) or not table_name_list.__contains__(
                self.wall_table_name):
            return False
        return True
