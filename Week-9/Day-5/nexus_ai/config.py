import os

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR    = os.path.join(BASE_DIR, "logs")
MEMORY_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

for d in [LOGS_DIR, REPORTS_DIR]:
    os.makedirs(d, exist_ok=True)

TOP_K_RECALL = 3
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

config_list_unified = [
    {
        "model": "llama-3.1-8b-instant",
        "api_key": GROQ_API_KEY,
        "base_url": "https://api.groq.com/openai/v1",
    }
]

llm_config_high = {
    "config_list": config_list_unified,
    "temperature": 0.3,
    "cache_seed": 42,
}

llm_config_efficient = {
    "config_list": config_list_unified,
    "temperature": 0.1,
    "cache_seed": 42,
}
