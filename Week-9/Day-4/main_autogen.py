import os
import logging
import warnings

# Silence third-party noise (must be before other imports)
warnings.filterwarnings("ignore", category=UserWarning, module="flaml")
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("autogen.oai.client").setLevel(logging.ERROR)

import autogen
from dotenv import load_dotenv
from nexus_memory_manager import NexusMemoryManager

load_dotenv()

# Configuration for Groq
config_list = [
    {
        "model": "llama-3.3-70b-versatile",
        "api_key": os.environ.get("GROQ_API_KEY"),
        "base_url": "https://api.groq.com/openai/v1",
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.2,
}

def run_memory_agent():
    # 1. Initialize Memory
    memory = NexusMemoryManager(session_window=6, top_k_recall=3)
    
    # 2. Define Agents
    assistant = autogen.AssistantAgent(
        name="Memory_Assistant",
        llm_config=llm_config,
        system_message="You are a helpful AI assistant with access to a 3-layer memory system (Session, SQLite, and FAISS). Use the provided context to answer accurately."
    )
    
    user_proxy = autogen.UserProxyAgent(
        name="User",
        human_input_mode="NEVER",  # Use NEVER because we are handling the input loop manually
        max_consecutive_auto_reply=1,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
    )

    # 3. Chat Loop
    print("\n[NEXUS] AutoGen Memory Session Started.")
    print("[INFO] Type 'exit' to end the session.\n")
    
    while True:
        user_input = input("USER: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        # Perform memory recall
        context = memory.recall(user_input)
        if context:
            assistant.update_system_message(
                f"You are a memory-aware assistant. Use this context if relevant:\n\n{context}"
            )
        
        # Initiate chat with max_turns=1 for immediate response
        user_proxy.initiate_chat(
            assistant,
            message=user_input,
            clear_history=False,
            max_turns=1,
            silent=True
        )
        
        # Retrieve and display the response
        last_msg = assistant.last_message()["content"]
        print(f"\nASSISTANT: {last_msg}\n")
        
        # Synchronize memory
        memory.store(user_input, last_msg)

if __name__ == "__main__":
    run_memory_agent()
