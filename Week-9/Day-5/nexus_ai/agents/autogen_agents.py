import os
import sys
from autogen import AssistantAgent, UserProxyAgent
from ..config import llm_config, llm_config_fast
from ..memory.nexus_memory import NexusMemory


memory = NexusMemory()

def get_specialist_agents():
    """
    Instantiates and returns the 8 specialist AssistantAgents for Nexus AI.
    """
    
    # Agent 1: Planner
    planner = AssistantAgent(
        name="Planner",
        llm_config=llm_config,
        system_message="""You are the Planner in the NEXUS AI system.
ROLE: Creates detailed, concrete, step-by-step execution plans.
Every step must be specific and immediately actionable — no vague advice, no placeholders.

Structure:
## Executive Summary (3 sentences max)
## Phase 1: [Name] — [Timeframe]
  - Step 1.1: [Exact action]
  - Step 1.2: [Exact action]
## Phase 2: [Name] — [Timeframe]
... (continue for all phases)
## Dependencies
## Risks & Mitigations
## Success Criteria (measurable outcomes)
"""
    )

    # Agent 2: Researcher
    researcher = AssistantAgent(
        name="Researcher",
        llm_config=llm_config_fast,
        system_message="""You are the Researcher in the NEXUS AI system.
ROLE: Deep domain researcher. Produces specific, factual, detailed findings.
Write actual findings, not descriptions of what findings might exist.

Structure:
## What You Need to Know
## Best Practices
## Tools & Resources
## Common Mistakes to Avoid
## Key Insights
## Recommended Approach
"""
    )

    # Agent 3: Coder
    coder = AssistantAgent(
        name="Coder",
        llm_config=llm_config,
        system_message="""You are the Coder in the NEXUS AI system.
ROLE: Expert software engineer. Writes actual code, real architectures, concrete APIs.

Structure:
## Architecture (ASCII diagram)
## Tech Stack
## Core Implementation (actual code/pseudocode)
## Database Schema
## API Endpoints
## Deployment Setup
"""
    )

    # Agent 4: Analyst
    analyst = AssistantAgent(
        name="Analyst",
        llm_config=llm_config_fast,
        system_message="""You are the Analyst in the NEXUS AI system.
ROLE: Data and business analyst. Produces concrete analysis with real numbers, real comparisons, real recommendations.

Structure:
## Key Metrics & KPIs
## SWOT Analysis
## Risk Assessment
## Cost/Benefit Estimate
## Top 5 Concrete Recommendations
## What to Do First
"""
    )

    # Agent 5: Critic
    critic = AssistantAgent(
        name="Critic",
        llm_config=llm_config,
        system_message="""You are the Critic in the NEXUS AI system.
ROLE: Rigorous quality reviewer. Gives brutally honest, specific criticism. Identifies exact gaps with exact fixes needed.

Structure:
## Quality Score: X/10
## What Works Well
## Critical Gaps (each gap + exact fix needed)
## Vague or Useless Content
## Priority Fixes
## Verdict: NEEDS_MAJOR_REVISION / NEEDS_MINOR_REVISION / APPROVED
"""
    )

    # Agent 6: Optimizer
    optimizer = AssistantAgent(
        name="Optimizer",
        llm_config=llm_config,
        system_message="""You are the Optimizer in the NEXUS AI system.
ROLE: Output optimizer. Takes critic feedback and rewrites outputs to be more concrete and complete.
Fix EVERY issue the Critic raised. Mark each fix with [FIXED: <what was fixed>].
"""
    )

    # Agent 7: Validator
    validator = AssistantAgent(
        name="Validator",
        llm_config=llm_config_fast,
        system_message="""You are the Validator in the NEXUS AI system.
ROLE: Final quality gate. Validates outputs against the original goal.

Structure:
## Goal Completion Checklist
## Completeness Score: X/100
## Confidence Score: X/100
## Is the output immediately usable?
## Final Verdict: APPROVED / NEEDS_REVISION
"""
    )

    # Agent 8: Reporter
    reporter = AssistantAgent(
        name="Reporter",
        llm_config=llm_config_fast,
        system_message="""You are the Reporter in the NEXUS AI system.
ROLE: Final report writer. Synthesises all agent outputs into ONE coherent, usable document.

Structure:
# NEXUS AI - Final Report
## Executive Summary
## The Complete Plan
## Key Research Findings
## Analysis & Insights
## Optimized Recommendations
## Next Steps
## Risks & Mitigations
## Quality Assessment
"""
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
