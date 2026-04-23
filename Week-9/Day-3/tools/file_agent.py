"""
tools/file_agent.py

File Analysis Agent
- Reads and analyzes .csv or .txt files.
- Can write or append content to files.
- Uses LLM for intelligent file content analysis.
"""

import os
import csv
from pathlib import Path
from typing import Literal
from groq import Groq
from dotenv import load_dotenv
from .utils import call_groq_with_retry

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """You are a File Analysis Agent.
Analyze the provided content and fulfill the instruction.
If it is CSV data, treat columns as labeled fields.
Be concise and factual."""

def _read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def _read_csv(path: str, max_rows: int = 50) -> tuple[str, dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        for i, row in enumerate(reader):
            if i >= max_rows:
                break
            rows.append(row)

    lines = [",".join(columns)]
    for r in rows:
        lines.append(",".join(str(r.get(c, "")) for c in columns))
    text = "\n".join(lines)

    meta = {
        "columns": columns,
        "row_count": len(rows),
        "truncated": len(rows) == max_rows,
    }
    return text, meta

def _write_txt(path: str, content: str, mode: str = "w") -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, mode, encoding="utf-8") as f:
        f.write(content)

def _analyse(file_content: str, instruction: str) -> str:
    if len(file_content) > 6000:
        file_content = file_content[:6000] + "\n... [truncated]"

    response = call_groq_with_retry(
        client,
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"File content:\n{file_content}\n\nInstruction: {instruction}"},
        ],
        temperature=0.2,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()

def file_agent(
    action: Literal["read", "write", "append", "analyse"],
    path: str,
    instruction: str = "",
    write_content: str = "",
) -> dict:
    """
    Unified file agent interface.
    """
    abs_path = os.path.abspath(path)
    file_type = "csv" if abs_path.endswith(".csv") else \
                "txt" if abs_path.endswith(".txt") else "unknown"

    if action == "read":
        if not os.path.exists(abs_path):
            return {"agent": "FileAgent", "success": False, "error": "File not found."}
        try:
            if file_type == "csv":
                content, meta = _read_csv(abs_path)
            else:
                content, meta = _read_txt(abs_path), {}
            return {"agent": "FileAgent", "success": True, "file_type": file_type, "content": content, "metadata": meta}
        except Exception as e:
            return {"agent": "FileAgent", "success": False, "error": str(e)}

    elif action == "analyse":
        if not os.path.exists(abs_path):
            return {"agent": "FileAgent", "success": False, "error": "File not found."}
        try:
            if file_type == "csv":
                content, meta = _read_csv(abs_path)
            else:
                content, meta = _read_txt(abs_path), {}
            analysis = _analyse(content, instruction or "Summarise this file.")
            return {"agent": "FileAgent", "success": True, "analysis": analysis, "file_type": file_type}
        except Exception as e:
            return {"agent": "FileAgent", "success": False, "error": str(e)}

    elif action in ("write", "append"):
        try:
            mode = "w" if action == "write" else "a"
            _write_txt(abs_path, write_content, mode=mode)
            return {"agent": "FileAgent", "success": True, "written": len(write_content.encode())}
        except Exception as e:
            return {"agent": "FileAgent", "success": False, "error": str(e)}

    return {"agent": "FileAgent", "success": False, "error": f"Unknown action: {action}"}
