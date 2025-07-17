# services/LogService.py
import sqlite3
import os
from datetime import datetime

class LogService:
    DB_PATH = os.path.join(os.environ.get('USERPROFILE', os.environ.get('HOME')), 'Documents', 'CaseManager', 'logs.db')

    def __init__(self):
        os.makedirs(os.path.dirname(LogService.DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(LogService.DB_PATH)
        self._ensure_schema()

    def _ensure_schema(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS file_log (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                case_id TEXT,
                action TEXT,
                filepath TEXT,
                hash TEXT
            )
        ''')
        self.conn.commit()

    def write_entry(self, case_id, action, filepath, file_hash=None):
        c = self.conn.cursor()
        c.execute(
            'INSERT INTO file_log (timestamp, case_id, action, filepath, hash) VALUES (?, ?, ?, ?, ?)',
            (datetime.utcnow().isoformat(), case_id, action, filepath, file_hash)
        )
        self.conn.commit()

    def get_recent_logs(self, case_id, limit=50):
        c = self.conn.cursor()
        c.execute(
            'SELECT timestamp, action, filepath FROM file_log WHERE case_id = ? ORDER BY timestamp DESC LIMIT ?',
            (case_id, limit)
        )
        return c.fetchall()