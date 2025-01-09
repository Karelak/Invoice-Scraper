# filepath: /path/to/your/file.py

import sqlite3
import os

class DatabaseHandler:
    def __init__(self, db_path):
        self.db_path = db_path
        # Ensure the directory for the database file exists
        db_dir = os.path.dirname(db_path)
        os.makedirs(db_dir, exist_ok=True)
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS invoices (
                    invoice_number TEXT,
                    booking_reference TEXT,
                    booking_date TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    date TEXT,
                    departure_time TEXT,
                    arrival_time TEXT,
                    route TEXT,
                    fare TEXT,
                    taxes TEXT,
                    fuel_surcharge TEXT,
                    ticketing_service TEXT,
                    total TEXT
                )
            ''')

    def insert_records(self, records):
        """Insert parsed invoice records directly into database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for record in records:
                cursor.execute('''
                    INSERT INTO invoices VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    record['invoice_number'],
                    record['booking_reference'],
                    record['booking_date'],
                    record['first_name'],
                    record['last_name'],
                    record['date'],
                    record['departure_time'],
                    record['arrival_time'],
                    record['route'],
                    record['fare'],
                    record['taxes'],
                    record['fuel_surcharge'],
                    record['ticketing_service'],
                    record['total']
                ))
            conn.commit()
