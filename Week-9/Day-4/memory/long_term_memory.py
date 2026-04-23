"""
memory/long_term_memory.py

Long-Term Memory (SQLite)
- Persists facts and conversation history across sessions.
- Stores structured records with metadata.
"""

import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "memory", "long_term.db")

class LongTermMemory:
    """
    SQLite-backed persistent memory store.
    """

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()
        print(f"[INFO] LongTermMemory connected to: {db_path}")

    def _init_db(self):
        conn = self._conn()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS conversations (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT    NOT NULL,
                role       TEXT    NOT NULL,
                content    TEXT    NOT NULL,
                timestamp  TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS facts (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT    NOT NULL,
                fact       TEXT    NOT NULL,
                source     TEXT,
                tag        TEXT,
                timestamp  TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS agent_outputs (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT    NOT NULL,
                agent      TEXT    NOT NULL,
                task       TEXT,
                output     TEXT    NOT NULL,
                timestamp  TEXT    NOT NULL
            );
        """)
        conn.commit()
        conn.close()

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _now(self) -> str:
        return datetime.now().isoformat()

    def save_turn(self, session_id: str, role: str, content: str):
        """Persist a single conversation turn."""
        conn = self._conn()
        conn.execute(
            "INSERT INTO conversations (session_id, role, content, timestamp) VALUES (?,?,?,?)",
            (session_id, role, content, self._now())
        )
        conn.commit()
        conn.close()

    def get_conversation(self, session_id: str) -> list[dict]:
        """Retrieve full conversation for a session."""
        conn = self._conn()
        rows = conn.execute(
            "SELECT role, content, timestamp FROM conversations WHERE session_id=? ORDER BY id",
            (session_id,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_all_sessions(self) -> list[str]:
        """List all unique session IDs."""
        conn = self._conn()
        rows = conn.execute(
            "SELECT DISTINCT session_id FROM conversations ORDER BY session_id DESC"
        ).fetchall()
        conn.close()
        return [r["session_id"] for r in rows]

    def save_fact(self, session_id: str, fact: str, source: str = "", tag: str = ""):
        """Store a distilled fact."""
        conn = self._conn()
        conn.execute(
            "INSERT INTO facts (session_id, fact, source, tag, timestamp) VALUES (?,?,?,?,?)",
            (session_id, fact, source, tag, self._now())
        )
        conn.commit()
        conn.close()

    def save_facts(self, session_id: str, facts: list[str], source: str = "", tag: str = ""):
        """Batch store multiple facts."""
        for fact in facts:
            self.save_fact(session_id, fact, source, tag)

    def search_facts(self, keyword: str = "", tag: str = "", limit: int = 20) -> list[dict]:
        """Search facts by keyword (LIKE) or tag."""
        conn = self._conn()
        query = "SELECT * FROM facts WHERE 1=1"
        params = []
        if keyword:
            query += " AND fact LIKE ?"
            params.append(f"%{keyword}%")
        if tag:
            query += " AND tag = ?"
            params.append(tag)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)

        rows = conn.execute(query, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def save_agent_output(self, session_id: str, agent: str, task: str, output: str):
        """Store a raw agent output for audit/recall."""
        conn = self._conn()
        conn.execute(
            "INSERT INTO agent_outputs (session_id, agent, task, output, timestamp) VALUES (?,?,?,?,?)",
            (session_id, agent, task, output[:2000], self._now())
        )
        conn.commit()
        conn.close()

    def stats(self) -> dict:
        conn = self._conn()
        return {
            "total_turns": conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0],
            "total_facts": conn.execute("SELECT COUNT(*) FROM facts").fetchone()[0],
            "total_outputs": conn.execute("SELECT COUNT(*) FROM agent_outputs").fetchone()[0],
            "sessions": conn.execute("SELECT COUNT(DISTINCT session_id) FROM conversations").fetchone()[0],
        }

    def clear_all(self):
        """Wipe all tables."""
        conn = self._conn()
        conn.executescript("""
            DELETE FROM conversations;
            DELETE FROM facts;
            DELETE FROM agent_outputs;
        """)
        conn.commit()
        conn.close()
        print("[INFO] LongTermMemory cleared.")
