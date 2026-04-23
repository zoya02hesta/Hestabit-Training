from autogen import AssistantAgent
from .config import llm_config

def get_research_agent() -> AssistantAgent:
    return AssistantAgent(
        name="Research_Agent",
        system_message="""You are a dedicated Research Agent.
ROLE: Your sole responsibility is to extract raw factual information, statistics, and verifiable data regarding the query.
CONSTRAINTS: 
- Do NOT generate summaries. 
- Do NOT answer the final question conversationally.
- Simply present the raw, unfiltered data clearly. 
- If you lack information, explicitly list what is unknown.
Strict job separation ensures you focus ONLY on gathering information.""",
        llm_config=llm_config,
        max_consecutive_auto_reply=10, # Memory window/interaction cap
    )
