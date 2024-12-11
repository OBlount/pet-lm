import re
import sqlite3

class DBManager():
    def __init__(self):
        self.conn = sqlite3.connect("data/chatbot.db")
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.username_constraint = r"[^a-zA-z\s]'"

    def __del__(self):
        self.conn.close()

    def create_tables(self):
        # Create table for users and favourite animal
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS usernames (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            pet_name TEXT NULL,
            favourite_animal TEXT NULL
        )
        ''')
        # Create table for booking ids
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS booking_ids (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL
        )
        ''')
        # Create table for booking slots
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS booking_slots (
            slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            specialist_name TEXT NOT NULL,
            booking_type TEXT NOT NULL,
            customer_name TEXT NULL,
            customer_id INTEGER NULL,
            FOREIGN KEY (customer_id) REFERENCES booking_ids(customer_id)
        )
        ''')
        self.conn.commit()

    def insert_username(self, name):
        sql = """
        INSERT INTO usernames (user_name)
        VALUES (?);
        """
        cleaned_username = re.sub(self.username_constraint, "", name)
        self.cursor.execute(sql, (cleaned_username,))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_username(self, name, user_id):
        sql = """
        UPDATE usernames
        SET user_name = ?
        WHERE user_id = ?;
        """
        self.cursor.execute(sql, (name.lower(), user_id,))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_pet_name(self, name, user_id):
        sql = """
        UPDATE usernames
        SET pet_name = ?
        WHERE user_id = ?;
        """
        self.cursor.execute(sql, (name.lower(), user_id,))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_favourite_animal(self, animal, user_id):
        sql = """
        UPDATE usernames
        SET favourite_animal = ?
        WHERE user_id = ?;
        """
        self.cursor.execute(sql, (animal.lower(), user_id,))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_username(self, user_id) -> str:
        sql = """
        SELECT user_name FROM usernames WHERE user_id = ?;
        """
        self.cursor.execute(sql, (user_id,))
        res = self.cursor.fetchone()
        return res[0] if res else "USER"

    def get_pet_name(self, user_id) -> str:
        sql = """
        SELECT pet_name FROM usernames WHERE user_id = ?;
        """
        self.cursor.execute(sql, (user_id,))
        res = self.cursor.fetchone()
        return res[0] if res else "PET"
