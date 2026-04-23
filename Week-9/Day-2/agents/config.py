import os

LOCAL_MODEL_CONFIG = [
    {
        "model": "qwen2.5:1.5b", 
        "base_url": os.environ.get("LOCAL_MODEL_BASE_URL", "http://localhost:11434/v1"),
        "api_key": "not-needed",
        "temperature": 0.2,
    }
]

llm_config = {
    "config_list": LOCAL_MODEL_CONFIG,
    "seed": 42,
    "cache_seed": None,
    "timeout": 120,
}
