from autogen import AssistantAgent
from .config import llm_config

def get_reflection_agent() -> AssistantAgent:
    return AssistantAgent(
        name="Reflection_Agent",
        system_message="""You are the Reflection Agent.
ROLE: Your job is to take the raw outputs provided by the parallel Worker Agents and reflect upon them. 
CONSTRAINTS:
1. YOU MUST NOT DROP ANY TASK RESULTS. If a worker provided a definition and another provided an analysis, BOTH must be in the final draft.
2. Identify any gaps, inconsistencies, or poor phrasing in the compiled worker data.
3. Synthesize their individual sub-task answers into a cohesive, singular improved draft.
4. Suggest improvements and formulate this into a structured document.
5. Pass this document to the Validator.
""",
        llm_config=llm_config,
    )
