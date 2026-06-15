import sqlite3
import uuid
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
from tabula_ai.db.connection import get_connection


def get_credentials_hash(creds_path: Path) -> str:
    """Unique identity key derived from credentials.json content."""
    content = Path(creds_path).read_bytes()
    return hashlib.sha256(content).hexdigest()[:16]


# ── Table setup ───────────────────────────────────────────────────────────────

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            creds_hash TEXT NOT NULL,
            spreadsheet_id TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    """)
    conn.commit()
    conn.close()


# ── Conversations ─────────────────────────────────────────────────────────────

def get_or_create_conversation(creds_hash: str, spreadsheet_id: str) -> str:
    """Returns existing active conversation id or creates a new one."""
    conn = get_connection()
    row = conn.execute("""
        SELECT id FROM conversations
        WHERE creds_hash = ? AND spreadsheet_id = ?
        ORDER BY created_at DESC LIMIT 1
    """, (creds_hash, spreadsheet_id)).fetchone()

    if row:
        conn.close()
        return row["id"]

    conversation_id = str(uuid.uuid4())
    conn.execute("""
        INSERT INTO conversations (id, creds_hash, spreadsheet_id, created_at)
        VALUES (?, ?, ?, ?)
    """, (conversation_id, creds_hash, spreadsheet_id, datetime.now(timezone.utc).isoformat()))
    conn.commit()
    conn.close()
    return conversation_id


# ── Messages ──────────────────────────────────────────────────────────────────

def save_message(conversation_id: str, role: str, content: str):
    conn = get_connection()
    conn.execute("""
        INSERT INTO messages (id, conversation_id, role, content, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (str(uuid.uuid4()), conversation_id, role, content, datetime.now(timezone.utc).isoformat()))
    conn.commit()
    conn.close()


def get_recent_messages(conversation_id: str, limit: int = 20) -> list[dict]:
    conn = get_connection()
    rows = conn.execute("""
        SELECT role, content, created_at FROM messages
        WHERE conversation_id = ?
        ORDER BY created_at ASC
    """, (conversation_id,)).fetchall()
    conn.close()
    return [{"role": r["role"], "content": r["content"], "created_at": r["created_at"]} for r in rows[-limit:]]