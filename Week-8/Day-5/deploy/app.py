from fastapi import FastAPI
from model_loader import load_model
from schemas import GenerateRequest, ChatRequest
from utils import build_chat_prompt
import torch
import uuid
import time
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

tokenizer, model = load_model()

@app.get("/")
def home():
    return {"message": "LLM API is running 🚀"}


# 🔹 GENERATE (Single prompt)
@app.post("/generate")
def generate(req: GenerateRequest):
    request_id = str(uuid.uuid4())
    start = time.time()

    inputs = tokenizer(req.prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=req.max_tokens,
            temperature=req.temperature,
            top_k=req.top_k,
            top_p=req.top_p,
            eos_token_id=tokenizer.eos_token_id
        )

    # 🔥 Remove prompt from output
    input_length = inputs["input_ids"].shape[1]
    generated_tokens = outputs[0][input_length:]

    response = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    # 🔥 Clean garbage patterns
    response = response.split("extract:")[0]
    response = response.split("response:")[0]
    response = response.strip()

    logging.info(f"[GENERATE] {request_id} | Prompt: {req.prompt}")

    return {
        "request_id": request_id,
        "response": response,
        "latency": round(time.time() - start, 2)
    }


# 🔹 CHAT (Conversation mode)
@app.post("/chat")
def chat(req: ChatRequest):
    request_id = str(uuid.uuid4())
    start = time.time()

    prompt = build_chat_prompt(
        req.system_prompt,
        req.user_prompt,
        req.history
    )

    logging.info(f"[CHAT] {request_id} | Prompt: {req.user_prompt}")

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=req.max_tokens,
            temperature=req.temperature,
            top_k=req.top_k,
            top_p=req.top_p,
            eos_token_id=tokenizer.eos_token_id
        )

    # 🔥 Remove prompt tokens
    input_length = inputs["input_ids"].shape[1]
    generated_tokens = outputs[0][input_length:]

    response = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    # 🔥 Clean unwanted tokens/patterns
    if "<|user|>" in response:
        response = response.split("<|user|>")[0]

    if "<|assistant|>" in response:
        response = response.split("<|assistant|>")[0]

    response = response.split("extract:")[0]
    response = response.split("response:")[0]

    response = response.strip()

    return {
        "request_id": request_id,
        "response": response,
        "latency": round(time.time() - start, 2)
    }