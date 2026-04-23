"""
tools/db_agent.py

DB Agent (SQLite)
- Queries SQLite databases (sales.db) or CSV files via in-memory SQL.
- Uses natural language to SQL generation.
- Provides plain-English summaries of findings.
"""

import os
import sqlite3
import csv
import re
import json
from groq import Groq
from dotenv import load_dotenv
from .utils import call_groq_with_retry

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"
DEFAULT_DB = os.path.join(os.path.dirname(__file__), "..", "data", "sales.db")

SYSTEM_PROMPT_TEMPLATE = """You are a SQL Expert.
Given the following database schema, write a SQLite-compliant SQL query that answers the user's question.

Schema:
{schema}

Rules:
- Output ONLY the raw SQL (no markdown fences, no explanation).
- Use only SELECT statements.
- ALWAYS double-quote table and column names (e.g., SELECT "Column" FROM "Table").
- Alias computed columns clearly.
- Limit results to 20 rows unless asked otherwise.
- Use the EXACT table name and column names from the schema above.
"""

SUMMARY_PROMPT = """You are a data analyst. Given SQL query results as JSON,
write a concise plain-English summary of the key findings.
Include specific numbers where relevant."""

def _load_csv_to_sqlite(csv_path: str) -> tuple[sqlite3.Connection, str, str]:
    table_name = os.path.splitext(os.path.basename(csv_path))[0]
    table_name = re.sub(r"[^a-zA-Z0-9_]", "_", table_name)

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        rows = list(reader)

    if not columns:
        raise ValueError(f"No columns found in {csv_path}")

    def infer_type(col):
        samples = [r[col] for r in rows[:20] if r.get(col, "").strip()]
        for val in samples:
            try:
                float(val)
                return "REAL"
            except:
                pass
        return "TEXT"

    col_defs = ", ".join(f'"{c}" {infer_type(c)}' for c in columns)
    schema_str = (
        f"TABLE: {table_name}\n"
        f"COLUMNS:\n" +
        "\n".join(f"  {c} ({infer_type(c)})" for c in columns)
    )

    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(f'CREATE TABLE "{table_name}" ({col_defs})')

    placeholders = ", ".join("?" for _ in columns)
    for row in rows:
        values = [row.get(c, "") for c in columns]
        conn.execute(f'INSERT INTO "{table_name}" VALUES ({placeholders})', values)
    conn.commit()

    return conn, table_name, schema_str

def _load_permanent_db() -> tuple[sqlite3.Connection, str, str]:
    conn = sqlite3.connect(DEFAULT_DB)
    conn.row_factory = sqlite3.Row
    cur = conn.execute("PRAGMA table_info(sales)")
    cols = cur.fetchall()
    schema_str = (
        "TABLE: sales\nCOLUMNS:\n" +
        "\n".join(f"  {c['name']} ({c['type']})" for c in cols)
    )
    return conn, "sales", schema_str

def _extract_sql(raw: str) -> str:
    raw = re.sub(r"```(?:sql)?\s*", "", raw)
    return raw.replace("```", "").strip()

def _is_safe(sql: str) -> bool:
    forbidden = re.compile(
        r"\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|PRAGMA|ATTACH)\b",
        re.IGNORECASE
    )
    return not forbidden.search(sql)

def _run_query(conn: sqlite3.Connection, sql: str) -> dict:
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = [dict(r) for r in cur.fetchall()]
        columns = [d[0] for d in cur.description] if cur.description else []
        return {"columns": columns, "rows": rows, "count": len(rows)}
    except sqlite3.Error as e:
        return {"error": str(e)}

def _summarise(question: str, sql: str, result: dict) -> str:
    if "error" in result:
        return f"Query failed: {result['error']}"
    payload = json.dumps(result["rows"][:10], indent=2)
    prompt = (
        f"User question: {question}\n"
        f"SQL executed: {sql}\n"
        f"Results (JSON):\n{payload}\n\n"
        "Summarise the findings concisely."
    )
    response = call_groq_with_retry(
        client,
        model=MODEL,
        messages=[
            {"role": "system", "content": SUMMARY_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3, max_tokens=256,
    )
    return response.choices[0].message.content.strip()

def db_agent(question: str, csv_path: str = "") -> dict:
    """
    Query any CSV file or the permanent sales.db using natural language.
    """
    if csv_path and os.path.exists(csv_path):
        conn, table_name, schema_str = _load_csv_to_sqlite(csv_path)
    else:
        conn, table_name, schema_str = _load_permanent_db()

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(schema=schema_str)
    response = call_groq_with_retry(
        client,
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.0, max_tokens=512,
    )
    sql = _extract_sql(response.choices[0].message.content)

    if not _is_safe(sql):
        conn.close()
        return {"agent": "DBAgent", "success": False, "error": "Unsafe SQL rejected."}

    result = _run_query(conn, sql)
    conn.close()

    if "error" in result:
        return {"agent": "DBAgent", "success": False, "error": result["error"], "sql": sql}

    summary = _summarise(question, sql, result)

    return {
        "agent": "DBAgent",
        "success": True,
        "sql": sql,
        "columns": result["columns"],
        "rows": result["rows"],
        "count": result["count"],
        "summary": summary,
    }