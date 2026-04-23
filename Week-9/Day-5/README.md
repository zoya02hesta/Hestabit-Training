# NEXUS AI - Multi-Agent System

An autonomous multi-agent pipeline built on the AutoGen framework for complex task execution and long-term memory persistence.

## Project Structure
```text
.
├── nexus_ai/             # Core package containing logic
│   ├── main.py           # Entry point and CLI handler
│   ├── config.py         # LLM and directory configuration
│   ├── orchestrator.py   # Pipeline orchestration logic
│   ├── agents/           # AutoGen specialist definitions
│   └── memory/           # Persistent memory implementations
├── logs/                 # Execution and debug logs
├── reports/              # Final output deliverables
├── README.md             # Project documentation
└── ARCHITECTURE.md       # Technical design overview
```

## Quick Start
Execute the system from the root directory:
```bash
python3 -m nexus_ai.main "Enter your task here"
```

## Key Capabilities
- **Resilient Execution**: Managed retry logic for third-party API rate limits.
- **Semantic Memory**: Persistent factual recall using SQLite and FAISS vector indices.
- **Specialized Workforce**: Eight distinct agent roles covering planning, research, coding, and quality assurance.
- **Framework Integration**: Built leveraging AutoGen for robust multi-agent communication.
