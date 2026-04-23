import os, sys, json, sqlite3, pickle
from datetime import datetime

from ..config import MEMORY_DIR, TOP_K_RECALL

# Long-term SQLite memory
DB_PATH = os.path.join(MEMORY_DIR, "nexus_memory.db")

class NexusMemory:
    """
    Unified memory for NEXUS AI.
    Stores agent outputs, facts, and task history in SQLite.
    Optionally uses FAISS for semantic recall if available.
    """

    def __init__(self):
        os.makedirs(MEMORY_DIR, exist_ok=True)
        self._init_db()
        self._init_vector_store()
        print(f" [NexusMemory] Initialised - {self.stats()['total_tasks']} tasks in memory")

    def _init_db(self):
        conn = self._conn()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT,
                goal        TEXT,
                status      TEXT,
                timestamp   TEXT
            );
            CREATE TABLE IF NOT EXISTS agent_outputs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT,
                agent       TEXT,
                task        TEXT,
                output      TEXT,
                success     INTEGER,
                elapsed     REAL,
                timestamp   TEXT
            );
            CREATE TABLE IF NOT EXISTS facts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT,
                fact        TEXT,
                source      TEXT,
                timestamp   TEXT
            );
        """)
        conn.commit()
        conn.close()

    def _init_vector_store(self):
        """Try to load FAISS. Gracefully degrade if not installed."""
        self.vector_enabled = False
        self.index          = None
        self.meta           = []
        index_path = os.path.join(MEMORY_DIR, "nexus.index")
        meta_path  = os.path.join(MEMORY_DIR, "nexus_meta.pkl")
        try:
            import faiss
            import numpy as np
            from sentence_transformers import SentenceTransformer
            self._faiss  = faiss
            self._np     = np
            self._model  = SentenceTransformer("all-MiniLM-L6-v2")
            self._dim    = 384
            if os.path.exists(index_path) and os.path.exists(meta_path):
                self.index = faiss.read_index(index_path)
                with open(meta_path, "rb") as f:
                    self.meta = pickle.load(f)
            else:
                self.index = faiss.IndexFlatL2(self._dim)
            self.vector_enabled = True
            self._index_path = index_path
            self._meta_path  = meta_path
            print(f" [NexusMemory] FAISS enabled - {self.index.ntotal} vectors")
        except ImportError:
            print("  [NexusMemory] FAISS not installed - vector memory disabled")

    def _conn(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def _now(self):
        return datetime.now().isoformat()

    # Storage Methods
    def save_task(self, session_id: str, goal: str, status: str = "running"):
        conn = self._conn()
        conn.execute(
            "INSERT INTO tasks (session_id, goal, status, timestamp) VALUES (?,?,?,?)",
            (session_id, goal, status, self._now())
        )
        conn.commit(); conn.close()

    def update_task_status(self, session_id: str, status: str):
        conn = self._conn()
        conn.execute(
            "UPDATE tasks SET status=? WHERE session_id=?", (status, session_id)
        )
        conn.commit(); conn.close()

    def save_agent_output(self, session_id: str, result: dict):
        conn = self._conn()
        conn.execute(
            "INSERT INTO agent_outputs (session_id, agent, task, output, success, elapsed, timestamp) VALUES (?,?,?,?,?,?,?)",
            (session_id, result["agent"], result["task"][:200],
             result["output"][:3000], int(result["success"]),
             result.get("elapsed", 0), self._now())
        )
        conn.commit(); conn.close()

        # Also embed into FAISS
        if self.vector_enabled and result["success"]:
            self._embed_and_store(
                f"[{result['agent']}] {result['output'][:400]}",
                {"agent": result["agent"], "session": session_id}
            )

    def save_fact(self, session_id: str, fact: str, source: str = ""):
        conn = self._conn()
        conn.execute(
            "INSERT INTO facts (session_id, fact, source, timestamp) VALUES (?,?,?,?)",
            (session_id, fact, source, self._now())
        )
        conn.commit(); conn.close()

    # Recall methods
    def recall(self, query: str) -> str:
        """Search all memory layers and return context string."""
        parts = []

        # Vector recall
        if self.vector_enabled and self.index.ntotal > 0:
            results = self._vector_search(query, top_k=TOP_K_RECALL)
            if results:
                lines = ["=== Semantic Memory Recall ==="]
                for r in results:
                    lines.append(f"- {r['text'][:200]}")
                parts.append("\n".join(lines))

        # SQLite fact recall
        conn  = self._conn()
        facts = conn.execute(
            "SELECT fact, source FROM facts ORDER BY id DESC LIMIT 5"
        ).fetchall()
        conn.close()
        if facts:
            lines = ["=== Long-Term Facts ==="]
            for f in facts:
                lines.append(f"• {f['fact']}")
            parts.append("\n".join(lines))

        return "\n\n".join(parts)

    def get_past_tasks(self, limit: int = 5) -> list[dict]:
        conn  = self._conn()
        rows  = conn.execute(
            "SELECT goal, status, timestamp FROM tasks ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    # FAISS Internals
    def _embed_and_store(self, text: str, metadata: dict):
        vec = self._model.encode([text]).astype(self._np.float32)
        self.index.add(vec)
        self.meta.append({"text": text, **metadata})
        self._faiss.write_index(self.index, self._index_path)
        with open(self._meta_path, "wb") as f:
            pickle.dump(self.meta, f)

    def _vector_search(self, query: str, top_k: int = 3) -> list[dict]:
        vec = self._model.encode([query]).astype(self._np.float32)
        top_k = min(top_k, self.index.ntotal)
        dists, idxs = self.index.search(vec, top_k)
        return [
            {"text": self.meta[i]["text"], "score": float(d)}
            for d, i in zip(dists[0], idxs[0]) if i >= 0
        ]

    def stats(self) -> dict:
        conn = self._conn()
        return {
            "total_tasks":   conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0],
            "total_outputs": conn.execute("SELECT COUNT(*) FROM agent_outputs").fetchone()[0],
            "total_facts":   conn.execute("SELECT COUNT(*) FROM facts").fetchone()[0],
            "vector_count":  self.index.ntotal if self.vector_enabled else 0,
        }
