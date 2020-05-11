import os
import sqlite3
from datetime import datetime

from Constants import Constants


class Database:
    db_name = "wallpaperDB.db"

    def __init__(self):
        self.DB_address = Constants.project_dir + os.sep + self.db_name
        self.date = ""

    def create_database(self):
        if not os.path.isfile(self.DB_address):
            conn = sqlite3.connect(self.DB_address)
            cur = conn.cursor()
            cur.execute("create table wallpaper (date text)")
            cur.execute("insert into wallpaper values('')")
            conn.commit()
        return self

    def insert_data(self, date):
        conn = sqlite3.connect(self.DB_address)
        cur = conn.cursor()
        values = (date,)
        cur.execute("update wallpaper set date=?;", values)
        conn.commit()
        conn.close()

    def get_data(self):
        conn = sqlite3.connect(self.DB_address)
        cur = conn.cursor()
        cur.execute("select * from wallpaper;")
        result = cur.fetchall()
        return result

    def get_date(self):
        old_date = (self.get_data()[0])[0]
        if old_date is not None and old_date != "":
            self.date = old_date
        return self.date

    def inset_today_date(self):
        self.insert_data(datetime.date(datetime.now()))
