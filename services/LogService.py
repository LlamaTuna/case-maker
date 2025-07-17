# services/LogService.py
import sqlite3
from pathlib import Path

class LogService:
    """
    Handles logging of folder and case creation events into a SQLite database.
    """
    DB_PATH = Path.home() / ".case_manager_logs.sqlite"

    def __init__(self):
        self.conn = sqlite3.connect(str(self.DB_PATH))
        self._ensure_tables()

    def _ensure_tables(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS folder_logs (
          id INTEGER PRIMARY KEY,
          case_id TEXT,
          folder_path TEXT,
          ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        c.execute("""
        CREATE TABLE IF NOT EXISTS case_logs (
          id INTEGER PRIMARY KEY,
          case_id TEXT,
          root_path TEXT,
          ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        self.conn.commit()

    def log_folder_creation(self, case_id: str, folder_path: str):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO folder_logs (case_id, folder_path) VALUES (?, ?)",
            (case_id, folder_path)
        )
        self.conn.commit()

    def log_case_created(self, case_id: str, root_path: str):
        c = self.conn.cursor()
        c.execute(
            "INSERT INTO case_logs (case_id, root_path) VALUES (?, ?)",
            (case_id, root_path)
        )
        self.conn.commit()
