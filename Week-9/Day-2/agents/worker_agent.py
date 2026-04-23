from autogen import AssistantAgent
from .config import llm_config

def get_worker_agent(worker_id: int) -> AssistantAgent:
    return AssistantAgent(
        name=f"Worker_Agent_{worker_id}",
        system_message=f"""You are Worker Agent {worker_id}, part of a parallel execution pool.
ROLE: You execute a specific sub-task delegated to you by the Orchestrator. 
CONSTRAINTS:
1. ONLY attempt to solve your assigned sub-task.
2. Provide a clear, concise, self-contained response based only on your findings.
3. If no task is directed at Worker {worker_id}, simply reply 'No task assigned.'
""",
        llm_config=llm_config,
    )
