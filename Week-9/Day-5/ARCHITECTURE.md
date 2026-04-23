# NEXUS AI - System Architecture

This document outlines the technical design and data flow of the NEXUS AI autonomous multi-agent system.

## Layered Architecture

### 1. Orchestration Layer (`nexus_ai/orchestrator.py`)
- **Framework**: AutoGen.
- **Pattern**: Sequential Pipeline orchestration.
- **Implementation**: Manages state transfer between eight specialist agents, passing the output of the preceding agent as context for the next.

### 2. Specialist Agent Layer (`nexus_ai/agents/`)
- **Roles**: Planner, Researcher, Coder, Analyst, Critic, Optimizer, Validator, Reporter.
- **Inference**: Orchestrated via Groq endpoints using centralized LLM configurations.
- **Configuration**: Defined in `nexus_ai/config.py`.

### 3. Memory Architecture (`nexus_ai/memory/`)
- **Semantic Retrieval**: Uses FAISS for vector search based on `all-MiniLM-L6-v2` embeddings.
- **Persistent Storage**: SQLite database tracks session history, task logs, and extracted factual entities.
- **Context Injection**: Each task initialization includes a semantic recall phase to pull relevant history into the prompt.

### 4. Output Generation (`reports/`)
- **Synthesis**: The Reporter agent consolidates specialist outputs into a single deliverable.
- **Quality Control**: Includes a validation score and confidence metric from the Validator agent.

## System Workflow
1. **Request Intake**: `nexus_ai/main.py` processes the initial user goal.
2. **Context Recall**: `NexusMemory` queries indices for relevant historical data.
3. **Strategic Planning**: The Planner generates a multi-phase execution roadmap.
4. **Core Execution**: Researcher, Analyst, and Coder execute specific plan steps.
5. **Quality Review**: The Critic identifies omissions; the Optimizer refines the outputs.
6. **Final Validation**: The Validator ensures the output meets the original goal criteria.
7. **Consolidation**: The Reporter generates the finalized Markdown report.


commands - 
cd "/home/zoyafatima/Desktop/Hestabit Training /Week-9/Day-5"
./venv/bin/streamlit run main_ui.py
./venv/bin/python3 -m nexus_ai.main "Your goal description here"
./venv/bin/pip install -r requirements.txt
