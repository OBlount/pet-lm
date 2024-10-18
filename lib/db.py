import sqlite3

class DBManager():
    def __init__(self):
        self.conn = sqlite3.connect("data/chatbot.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def __del__(self):
        self.conn.close()

    def create_tables(self):
        # Create table for users and favourite animal
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS usernames (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
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
