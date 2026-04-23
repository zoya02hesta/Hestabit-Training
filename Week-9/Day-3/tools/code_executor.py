import os
import subprocess
import re
import tempfile
import sys
from groq import Groq
from dotenv import load_dotenv
from .utils import call_groq_with_retry

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """You are a Python Code Generation Agent.
Output ONLY valid Python code inside a single ```python ... ``` block.
Rules:
- No explanations outside the code block.
- Use stdlib, pandas, or numpy.
- Always print() the final result.
- DATA_PATH is provided as an environment variable.
"""

def _extract_code(llm_output: str) -> str:
    pattern = r"```python\s*([\s\S]+?)```"
    match = re.search(pattern, llm_output)
    if match:
        return match.group(1).strip()
    return llm_output.strip().strip("`").strip()

def _run_code(code: str, data_path: str = "") -> dict:
    env = os.environ.copy()
    env["DATA_PATH"] = data_path
    env["PYTHONPATH"] = os.pathsep.join(sys.path)
    
    # Pre-inject common imports and the DATA_PATH variable
    header = (
        "import os, sys\n"
        "try: import pandas as pd\nexcept: pass\n"
        "try: import numpy as np\nexcept: pass\n\n"
        f'DATA_PATH = r"""{data_path}"""\n'
    )
    full_code = header + code

    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as tmp:
        tmp.write(full_code)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True, text=True,
            timeout=30, env=env
        )
        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Execution timed out.", "returncode": -1}
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def code_agent(task: str, data_path: str = "") -> dict:
    """
    Generate and execute Python code for a specific task.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Task: {task}\nData path: {data_path}"}
    ]
    response = call_groq_with_retry(
        client,
        model=MODEL, messages=messages, temperature=0.1, max_tokens=1024
    )
    code = _extract_code(response.choices[0].message.content)

    exec_result = _run_code(code, data_path)
    success = exec_result["returncode"] == 0

    return {
        "agent": "CodeAgent",
        "success": success,
        "code": code,
        "stdout": exec_result["stdout"],
        "stderr": exec_result["stderr"],
    }
