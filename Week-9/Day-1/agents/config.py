import os

# Using local open-source models as mandated (TinyLlama / Phi-3 / Mistral / Qwen)
# Ensure an API server (e.g. Ollama, LM Studio, vLLM) is running locally at the specified base_url
LOCAL_MODEL_CONFIG = [
    {
        "model": "tinyllama", # Replace with phi3, qwen, etc. depending on local environment
        "base_url": os.environ.get("LOCAL_MODEL_BASE_URL", "http://localhost:11434/v1"),
        "api_key": "not-needed", # Local models generally do not require API keys
        "temperature": 0.2,
    }
]

llm_config = {
    "config_list": LOCAL_MODEL_CONFIG,
    "seed": 42,
    "cache_seed": None # Disable caching for active development mapping
}
