import sys
import logging
import warnings
import os
from dotenv import load_dotenv

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Silence secondary loggers
logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)
logging.getLogger("autogen").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from .orchestrator import NexusOrchestrator

def main():
    load_dotenv()
    
    if not os.environ.get("GROQ_API_KEY"):
        print("\n[ERROR] GROQ_API_KEY not found in environment.")
        print("Please export it or add it to your .env file.")
        return

    print("\nNEXUS AI - Multi-Agent Framework")
    print("-" * 35 + "\n")

    goal = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    
    if not goal:
        print("[TIP] You can pass your goal as a command line argument.")
        print("Example: python3 -m nexus_ai.main 'Design a futuristic city plan'")
        goal = input("\n[Nexus AI] Enter your goal: ")

    orchestrator = NexusOrchestrator()
    orchestrator.run(goal)

if __name__ == "__main__":
    main()
