"""
orchestrator.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Day 3 — Tool-Calling Agents | Week 9 Agentic AI

Usage:
  python orchestrator.py                                        # default sales.csv
  python orchestrator.py --file organizations-100.csv           # any file in data/
  python orchestrator.py --file organizations-100.csv "task"    # custom task
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os, sys, json, csv
from groq import Groq
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))
from tools.code_executor import code_agent
from tools.db_agent       import db_agent
from tools.file_agent     import file_agent
from tools.utils          import call_groq_with_retry

# ── Config ───────────────────────────────────────────────
load_dotenv()
client   = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL    = "llama-3.3-70b-versatile"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_DB  = os.path.join(DATA_DIR, "sales.db")
OUT_DIR  = DATA_DIR

# ── Dynamic file resolver ─────────────────────────────────
def resolve_data_file(filename: str = "sales.csv") -> str:
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        available = [f for f in os.listdir(DATA_DIR) if f.endswith((".csv", ".txt"))]
        print(f"\n❌ File '{filename}' not found in data/")
        print(f"📂 Available files: {available}")
        sys.exit(1)
    return path

# ── Prompts ───────────────────────────────────────────────
PLANNER_PROMPT = """You are an Orchestrator Planner for a multi-agent AI system.
You have three specialist agents:

1. FileAgent  — reads/analyses any .csv or .txt file from disk
2. CodeAgent  — writes and executes Python code for computation/statistics on the file
3. DBAgent    — queries a SQLite sales database (ONLY use when the file is sales.csv)

Rules:
- Use FileAgent and CodeAgent for ANY file.
- All three agents work with ANY file — use all three for every task.

Given the user's request and the active filename, output a JSON plan.
Each step must have:
  - "agent":       "FileAgent" | "CodeAgent" | "DBAgent"
  - "instruction": exact task string to pass to that agent

Output ONLY valid JSON with key "steps": [...].
"""

VALIDATOR_PROMPT = """You are a Validator and Report Synthesiser.
You receive the user's question and outputs from multiple specialist agents.
Your job:
  1. Synthesise all outputs into ONE clear, structured final answer.
  2. Use bullet points and numbers for insights.
  3. Highlight any conflicts or missing data.
  4. End with a one-line executive summary.
"""

# ── Planner ───────────────────────────────────────────────
def plan(user_request: str, filename: str, columns: list) -> list[dict]:
    print("\n🧠 [Planner] Deciding which agents to invoke...")

    # Give the planner full context: filename + live columns
    context = (
        f"Active file: {filename}\n"
        f"Columns in file: {columns}\n"
        f"User request: {user_request}"
    )

    response = call_groq_with_retry(
        client,
        model=MODEL,
        messages=[
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user",   "content": context},
        ],
        temperature=0.0, max_tokens=512,
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        steps = json.loads(raw).get("steps", [])
        print(f"📋 [Planner] Plan: {[s['agent'] for s in steps]}")
        return steps
    except json.JSONDecodeError:
        print("⚠️  [Planner] Could not parse plan. Using default.")
        return [
            {"agent": "FileAgent", "instruction": user_request},
            {"agent": "CodeAgent", "instruction": user_request},
        ]

# ── Executor ──────────────────────────────────────────────
def execute(steps: list[dict], data_csv: str, columns: list) -> list[dict]:
    results = []
    for i, step in enumerate(steps, 1):
        agent_name  = step["agent"]
        instruction = step["instruction"]
        print(f"\n⚙️  [Executor] Step {i}/{len(steps)}: {agent_name}")

        if agent_name == "FileAgent":
            result = file_agent("analyse", data_csv, instruction=instruction)
            results.append({
                "agent":   "FileAgent",
                "output":  result.get("analysis", result.get("error", "")),
                "success": result["success"],
            })

        elif agent_name == "CodeAgent":
            # Inject live schema so LLM uses correct column names
            dynamic_instruction = (
                f"{instruction}\n\n"
                f"[SCHEMA] The CSV columns are: {columns}. "
                f"Use only these exact column names."
            )
            result = code_agent(dynamic_instruction, data_path=data_csv)
            results.append({
                "agent":   "CodeAgent",
                "output":  result["stdout"] if result["success"] else result["stderr"],
                "code":    result["code"],
                "success": result["success"],
            })

        elif agent_name == "DBAgent":
            result = db_agent(instruction, csv_path=data_csv)
            rows_preview = json.dumps(result.get("rows", [])[:5], indent=2)
            results.append({
                "agent":   "DBAgent",
                "output":  result.get("summary", "") + "\n\nSample rows:\n" + rows_preview,
                "sql":     result.get("sql", ""),
                "success": result.get("success", False),
            })

        else:
            results.append({"agent": agent_name,
                            "output": f"Unknown agent: {agent_name}", "success": False})

    return results

# ── Validator ─────────────────────────────────────────────
def validate_and_synthesise(user_request: str, results: list[dict]) -> str:
    print("\n✅ [Validator] Synthesising final answer...")
    agent_outputs = ""
    for r in results:
        agent_outputs += f"\n\n### {r['agent']} Output ###\n{r['output']}"
        if not r["success"]:
            agent_outputs += "\n⚠️ This agent reported an error."

    response = call_groq_with_retry(
        client,
        model=MODEL,
        messages=[
            {"role": "system", "content": VALIDATOR_PROMPT},
            {"role": "user",   "content":
                f"User request: {user_request}\n\nAgent outputs:{agent_outputs}"},
        ],
        temperature=0.3, max_tokens=1024,
    )
    return response.choices[0].message.content.strip()

# ── Orchestrate ───────────────────────────────────────────
def orchestrate(user_request: str, data_csv: str) -> str:
    filename = os.path.basename(data_csv)

    # Sniff columns once — passed to both Planner and Executor
    with open(data_csv, newline="") as f:
        columns = csv.DictReader(f).fieldnames or []

    print("\n" + "━"*60)
    print("🚀 ORCHESTRATOR — New Request")
    print("━"*60)
    print(f"📩 User    : {user_request}")
    print(f"📂 File    : {filename}")
    print(f"📋 Columns : {columns}\n")

    steps        = plan(user_request, filename, columns)
    results      = execute(steps, data_csv, columns)
    final_answer = validate_and_synthesise(user_request, results)
    return final_answer

# ── CLI ───────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═"*60)
    print("  MULTI-AGENT ORCHESTRATOR — Day 3, Week 9")
    print("  Agents: FileAgent | CodeAgent | DBAgent")
    print("═"*60)

    # Parse --file flag
    args, filename, task_parts = sys.argv[1:], "sales.csv", []
    i = 0
    while i < len(args):
        if args[i] == "--file" and i + 1 < len(args):
            filename = args[i + 1]; i += 2
        else:
            task_parts.append(args[i]); i += 1

    DATA_CSV  = resolve_data_file(filename)
    available = [f for f in os.listdir(DATA_DIR) if f.endswith((".csv", ".txt"))]

    print(f"\n📂 Files available in data/ : {available}")
    print(f"📄 Using                     : {filename}")

    user_input = " ".join(task_parts) if task_parts else (
        f"Analyze {filename} and generate top 5 insights "
        f"about the data including patterns, totals, and key metrics."
    )

    # Seed DB if needed
    if not os.path.exists(DATA_DB):
        print("\n⚠️  Database not found. Seeding...")
        import importlib.util, pathlib
        spec   = importlib.util.spec_from_file_location(
            "seed_db", pathlib.Path(__file__).parent / "seed_db.py")
        seeder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(seeder)
        seeder.seed()

    answer = orchestrate(user_input, DATA_CSV)

    print("\n" + "═"*60)
    print("🏁 FINAL ANSWER")
    print("═"*60)
    print(answer)

    report_name = f"report_{os.path.splitext(filename)[0]}.txt"
    out_path    = os.path.join(OUT_DIR, report_name)
    with open(out_path, "w") as f:
        f.write(f"File   : {filename}\nRequest: {user_input}\n\n{'='*60}\n\n{answer}")
    print(f"\n📄 Report saved → {out_path}")