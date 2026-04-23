from autogen import AssistantAgent
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.config import llm_config

def get_orchestrator() -> AssistantAgent:
    return AssistantAgent(
        name="Orchestrator_Agent",
        system_message="""You are the Orchestrator (Planner).
ROLE: When given a user query, your job is to decompose the goal into 2 to 3 distinct, parallelizable sub-tasks.
CONSTRAINTS:
1. Break down the task logically into 2 or 3 distinct sub-tasks.
2. DO NOT SOLVE THE PROBLEM YOURSELF.
3. You MUST output your plan as a raw, valid JSON array of strings. 
4. DO NOT wrap the output in markdown code blocks like ```json. Do not include any conversational text.
Example format:
["Investigate the core mechanism of X", "Compare X to Y and define differences"]
""",
        llm_config=llm_config,
    )
