import sqlite3
import os

class DatabaseHandler:
    def __init__(self, db_path):
        self.db_path = db_path
        # Ensure the directory for the database file exists
        db_dir = os.path.dirname(db_path)
        if db_dir:
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
            print("Table created or already exists.")

    def insert_records(self, record):
        """Insert a single record into the database."""
        sql = '''INSERT INTO invoices (
            invoice_number, booking_reference, booking_date, 
            first_name, last_name, date, departure_time, arrival_time,
            route, fare, taxes, fuel_surcharge, ticketing_service, total
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (
                    record.get('invoice_number', ''),
                    record.get('booking_reference', ''),
                    record.get('booking_date', ''),
                    record.get('first_name', ''),
                    record.get('last_name', ''),
                    record.get('date', ''),
                    record.get('departure_time', ''),
                    record.get('arrival_time', ''),
                    record.get('route', ''),
                    record.get('fare', ''),
                    record.get('taxes', ''),
                    record.get('fuel_surcharge', ''),
                    record.get('ticketing_service', ''),
                    record.get('total', '')
                ))
                conn.commit()
                print(f"Inserted record: {record}")
        except sqlite3.Error as e:
            print(f"Error inserting record: {e}")
            print(f"Failed record: {record}")
