import re
import sqlite3
import random

from datetime import datetime, timedelta

class DBManager():
    def __init__(self):
        self.conn = sqlite3.connect("data/chatbot.db")
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.populate_booking_slots()
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
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            slot_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES usernames(user_id),
            FOREIGN KEY (slot_id) REFERENCES booking_slots(slot_id)
        )
        ''')
        # Create table for booking slots
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS booking_slots (
            slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            specialist_name TEXT NOT NULL,
            booking_type TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def populate_booking_slots(self):
        self.cursor.execute("SELECT COUNT(*) FROM booking_slots")
        existing_slots = self.cursor.fetchone()[0]

        # Skip adding booking slots. It's already populated
        if existing_slots > 0:
            return

        specialists = [
            "Aisha",
            "Lila",
            "Mei-Ling",
            "Carlos",
                ]
        today = datetime.now()
        for day in range(31):
            date = (today + timedelta(days=day)).strftime("%d/%m/%Y")

            for time in ["10:00", "12:00", "14:00"]:
                specialist = random.choice(specialists)
                self.cursor.execute('''
                INSERT INTO booking_slots (appointment_date, appointment_time, specialist_name, booking_type)
                VALUES (?, ?, ?, ?)
                ''', (date, time, specialist, "Grooming"))

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

    def get_favourite_animal(self, user_id) -> str:
        sql = """
        SELECT favourite_animal FROM usernames WHERE user_id = ?;
        """
        self.cursor.execute(sql, (user_id,))
        res = self.cursor.fetchone()
        return res[0] if res else "PET"

    def get_booking_slots(self, date):
        sql = """
        SELECT slot_id, appointment_time, specialist_name, booking_type
        FROM booking_slots
        WHERE appointment_date = ?
        """
        self.cursor.execute(sql, (date,))
        slots = self.cursor.fetchall()
        return slots

    def insert_booking(self, user_id, slot_id):
        sql = """
        INSERT INTO booking_ids (user_id, slot_id)
        VALUES (?, ?)
        """
        self.cursor.execute(sql, (user_id, slot_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_user_bookings(self, user_id):
        sql = """
        SELECT slot_id
        FROM booking_ids
        WHERE user_id = ?
        """
        self.cursor.execute(sql, (user_id,))
        slot_ids = [row[0] for row in self.cursor.fetchall()]

        if not slot_ids:
            return []

        sql = """
        SELECT appointment_date, appointment_time, specialist_name, booking_type
        FROM booking_slots
        WHERE slot_id IN ({})
        """.format(','.join('?'*len(slot_ids)))

        self.cursor.execute(sql, slot_ids)
        bookings = self.cursor.fetchall()

        return [
            {
                "appointment_date": row[0],
                "appointment_time": row[1],
                "specialist_name": row[2],
                "booking_type": row[3]
            } for row in bookings
        ]
