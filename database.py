
import sqlite3
import uuid
import re
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS grievances (
                complaint_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                email TEXT NOT NULL,
                complaint_details TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL
            )
            """)

    def create_complaint(self, name, phone, email, details):
        if not re.match(r"^[\w\.\+\-]+@[\w]+\.[a-z]{2,3}$", email):
            raise ValueError("Invalid email format")
        if not re.match(r"^\d{10}$", phone):
            raise ValueError("Invalid phone number format")

        complaint_id = f"XYZ{uuid.uuid4().hex[:5].upper()}"
        status = "In Progress"
        created_at = datetime.now()

        with self.conn:
            self.conn.execute("""
            INSERT INTO grievances (complaint_id, name, phone_number, email, complaint_details, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (complaint_id, name, phone, email, details, status, created_at))
        
        return complaint_id

    def get_complaint(self, complaint_id):
        with self.conn:
            cursor = self.conn.execute("SELECT * FROM grievances WHERE complaint_id = ?", (complaint_id,))
            return cursor.fetchone()
