import sqlite3
from pathlib import Path

DB_DIR = Path.home() / ".tabula_ai"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "tabula_memory.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets you access columns by name
    return conn