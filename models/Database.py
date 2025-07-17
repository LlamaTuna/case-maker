# models/Database.py
import sqlite3
import os

class Database:
    DB_FILE = os.path.join(os.environ.get('USERPROFILE', os.environ.get('HOME')), 'Documents', 'CaseManager', 'cases.db')

    def __init__(self):
        os.makedirs(os.path.dirname(Database.DB_FILE), exist_ok=True)
        self.conn = sqlite3.connect(Database.DB_FILE)
        self._ensure_schema()

    def _ensure_schema(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                investigator TEXT,
                base_path TEXT,
                created_on TEXT
            )
        ''')
        self.conn.commit()

    def add_case(self, case):
        c = self.conn.cursor()
        c.execute(
            'INSERT INTO cases (case_id, investigator, base_path, created_on) VALUES (?, ?, ?, CURRENT_TIMESTAMP)',
            (case.case_id, case.investigator, case.base_path)
        )
        self.conn.commit()

    def list_cases(self):
        c = self.conn.cursor()
        c.execute('SELECT case_id, investigator, base_path, created_on FROM cases')
        return c.fetchall()
