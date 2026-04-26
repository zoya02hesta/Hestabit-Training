import torch

# 🔥 Use relative path (portable)
MODEL_PATH = "../model-fp16"

# 🔥 Auto device detection
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# 🔥 Generation settings
MAX_NEW_TOKENS = 200
TEMPERATURE = 0.7
TOP_K = 50
TOP_P = 0.9