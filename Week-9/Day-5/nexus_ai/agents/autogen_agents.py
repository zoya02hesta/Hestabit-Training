import os
import sys
from autogen import AssistantAgent, UserProxyAgent
from ..config import llm_config_high, llm_config_efficient
from ..memory.nexus_memory import NexusMemory

memory = NexusMemory()

def get_specialist_agents():
    planner = AssistantAgent(
        name="Planner",
        llm_config=llm_config_high,
        system_message="You are the Planner. Create a strict, concrete step-by-step action plan for the goal. Be concise."
    )

    researcher = AssistantAgent(
        name="Researcher",
        llm_config=llm_config_efficient,
        system_message="You are the Researcher. Provide 5-7 concrete, factual insights about the goal. Be factual and brief."
    )

    coder = AssistantAgent(
        name="Coder",
        llm_config=llm_config_high,
        system_message="You are the Coder. ONLY provide content if the goal explicitly requires software or math automation. If the goal is non-technical (e.g., workouts, plans, essays), you MUST say 'Technical implementation not required for this goal' and providing nothing else. No dummy scripts!"
    )

    analyst = AssistantAgent(
        name="Analyst",
        llm_config=llm_config_efficient,
        system_message="You are the Analyst. Provide a SWOT and 3 clear recommendations. Be data-driven."
    )

    critic = AssistantAgent(
        name="Critic",
        llm_config=llm_config_efficient,
        system_message="You are the Critic. Identify the 2 biggest gaps in the current work and suggest fixes."
    )

    optimizer = AssistantAgent(
        name="Optimizer",
        llm_config=llm_config_high,
        system_message="You are the Optimizer. Rewrite the outputs to address the critic's gaps. Always preserve and improve any code blocks provided by the Coder."
    )

    validator = AssistantAgent(
        name="Validator",
        llm_config=llm_config_efficient,
        system_message="You are the Validator. Confirm if the output meets the goal on a scale of 1-100."
    )

    reporter = AssistantAgent(
        name="Reporter",
        llm_config=llm_config_efficient,
        system_message="You are the Reporter. Combine all findings into a comprehensive report. If the Coder or Optimizer states that 'Technical implementation not required', do NOT include a code or technical section in your report."
    )

    return {
        "Planner": planner,
        "Researcher": researcher,
        "Coder": coder,
        "Analyst": analyst,
        "Critic": critic,
        "Optimizer": optimizer,
        "Validator": validator,
        "Reporter": reporter
    }
