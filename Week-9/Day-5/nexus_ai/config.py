import os


BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR    = os.path.join(BASE_DIR, "logs")
MEMORY_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

for d in [LOGS_DIR, REPORTS_DIR]:
    os.makedirs(d, exist_ok=True)


TOP_K_RECALL = 4

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

config_list = [
    {
        "model": "llama-3.3-70b-versatile",
        "api_key": GROQ_API_KEY,
        "base_url": "https://api.groq.com/openai/v1",
    }
]


config_list_fast = [
    {
        "model": "llama-3.1-8b-instant",
        "api_key": GROQ_API_KEY,
        "base_url": "https://api.groq.com/openai/v1",
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.3,
    "timeout": 120, 
}

llm_config_fast = {
    "config_list": config_list_fast,
    "temperature": 0.1,
    "timeout": 60,
}
