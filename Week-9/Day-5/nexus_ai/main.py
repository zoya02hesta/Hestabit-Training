import sys
import logging
import warnings
import os
from dotenv import load_dotenv

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

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
        print("\n[ERROR] GROQ_API_KEY not found.")
        return

    print("\nNEXUS AI")
    print("-" * 10 + "\n")

    goal = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    
    if not goal:
        goal = input("\n[Nexus AI] Enter goal: ")

    orchestrator = NexusOrchestrator()
    orchestrator.run(goal)

if __name__ == "__main__":
    main()
