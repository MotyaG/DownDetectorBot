import sqlite3
import os

class Database:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_db(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS sites (
            site TEXT PRIMARY KEY
        );""")
            conn.commit()
            print("Database created!")

    def add_site(self, site):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO sites(site) VALUES (?)""", (site,))
            conn.commit()
            print(f"Site {site} added!")

    def check_site(self, site):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            if cursor.execute("SELECT site FROM sites WHERE site = (?)", (site,)).fetchone():
                return True
            else:
                return False

    def remove_db(self):
        os.remove(self.db_file)
        print("Database removed!")
