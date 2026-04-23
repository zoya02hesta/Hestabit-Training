import os
import sys
import logging
import warnings
import autogen
from dotenv import load_dotenv

# Silence third-party noise
warnings.filterwarnings("ignore", category=UserWarning, module="flaml")
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)

# Add current directory to path for tool imports
sys.path.insert(0, os.path.dirname(__file__))
from tools.code_executor import code_agent
from tools.db_agent import db_agent
from tools.file_agent import file_agent

load_dotenv()

# Configuration for Groq
config_list = [
    {
        "model": "llama-3.1-8b-instant",
        "api_key": os.environ.get("GROQ_API_KEY"),
        "base_url": "https://api.groq.com/openai/v1",
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.1,
}

# --- Tool Wrappers for AutoGen ---

def run_db_query(question: str, csv_path: str = "") -> str:
    """Query a database or CSV file using natural language."""
    result = db_agent(question, csv_path=csv_path)
    if not result["success"]:
        return f"Error: {result.get('error', 'Unknown error')}"
    return f"SQL: {result['sql']}\nSummary: {result['summary']}"

def run_file_analysis(action: str, path: str, instruction: str = "", write_content: str = "") -> str:
    """Read, write, or analyze files (.csv or .txt)."""
    result = file_agent(action, path, instruction=instruction, write_content=write_content)
    if not result["success"]:
        return f"Error: {result.get('error', 'Unknown error')}"
    
    if action == "read":
        return f"Content (truncated): {result['content'][:500]}"
    elif action == "analyse":
        return f"Analysis: {result['analysis']}"
    elif action in ("write", "append"):
        return f"Success: Wrote {result['written']} bytes to {result.get('path', 'file')}."
    return "Action completed successfully."

def run_python_task(task: str, data_path: str = "") -> str:
    """Generate and execute Python code for data processing or statistics."""
    result = code_agent(task, data_path=data_path)
    if not result["success"]:
        return f"CRITICAL_FAILURE: Subprocess error.\nSTDERR: {result.get('stderr', 'Unknown error')}\nDEBUG_CODE: {result.get('code', '')}"
    return f"SUCCESS: Output from execution:\n{result['stdout']}\n\nGENERATED_CODE:\n{result['code']}"

# --- Agent setup ---

def run_orchestrator():
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    default_file = os.path.join(data_dir, "sales.csv")
    
    # Get actual files in data directory to provide as context
    try:
        files = os.listdir(data_dir)
        file_list_str = "\n".join([f"- {f}" for f in files])
    except:
        file_list_str = "None found"

    orchestrator = autogen.AssistantAgent(
        name="Orchestrator",
        llm_config=llm_config,
        system_message=f"""You are a Master Orchestrator for the Nexus AI Tool-Chain.
You have access to specialized tools for Database querying, File operations, and Python execution.

FILES AVAILABLE IN {data_dir}:
{file_list_str}

Default Data File: {default_file}

Rules:
1. CSV FILES: For any request involving a .csv file, ALWAYS prefer 'run_db_query'. It is the most precise tool for tabular data.
2. ONE TOOL AT A TIME: Suggest exactly ONE tool call. NEVER suggest multiple calls in one turn.
3. DISCOVERY: Use the list of available files above. If a user asks for a file that isn't listed, check if a similarly named file exists.
4. No Conversational Filler: When calling a tool, provide ONLY the structured tool call.
5. Final Answer: Only provide your final response after the tool completes.
6. Termination: End your final response with 'TERMINATE'.
"""
    )

    user_proxy = autogen.UserProxyAgent(
        name="User_Proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=2,
        is_termination_msg=lambda x: (x.get("content") or "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
    )

    # Register tools
    autogen.register_function(
        run_db_query,
        caller=orchestrator,
        executor=user_proxy,
        name="run_db_query",
        description="Query the sales database or any CSV file using natural language questions.",
    )
    autogen.register_function(
        run_file_analysis,
        caller=orchestrator,
        executor=user_proxy,
        name="run_file_analysis",
        description="Perform file operations: read, write, append, or analyse .txt and .csv files.",
    )
    autogen.register_function(
        run_python_task,
        caller=orchestrator,
        executor=user_proxy,
        name="run_python_task",
        description="Execute complex data processing or mathematical tasks using Python code.",
    )

    print("=" * 60)
    print("  NEXUS TOOL-CHAIN: AutoGen Orchestrator Started")
    print("  Tools: DB Query | File Analysis | Python Executor")
    print("=" * 60)
    print("[INFO] Type 'exit' to quit.\n")

    while True:
        user_input = input("USER: ")
        if user_input.lower() in ["exit", "error", "quit"]:
            break
        
        user_proxy.initiate_chat(
            orchestrator,
            message=user_input,
            clear_history=False,
        )

if __name__ == "__main__":
    run_orchestrator()
