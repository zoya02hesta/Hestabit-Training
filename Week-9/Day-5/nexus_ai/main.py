import os
import sys
import logging
import warnings

# Absolute Silence: Must happen before other imports
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("autogen").setLevel(logging.ERROR)

import argparse
from dotenv import load_dotenv
from .orchestrator import NexusOrchestrator

def main():
    load_dotenv()
    
    if not os.environ.get("GROQ_API_KEY"):
        print("\n[ERROR] GROQ_API_KEY not found in environment.")
        print("Please export it or add it to your .env file.")
        return

    print("\nNEXUS AI - Multi-Agent Framework")
    print("-" * 35 + "\n")

    # Get goal from CLI or default
    goal = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    
    if not goal:
        print("[TIP] You can pass your goal as a command line argument.")
        print("Example: python3 -m nexus_ai.main 'Design a futuristic city plan'")
        goal = input("\n[Nexus AI] Enter your goal: ")

    orchestrator = NexusOrchestrator()
    orchestrator.run(goal)

if __name__ == "__main__":
    main()
