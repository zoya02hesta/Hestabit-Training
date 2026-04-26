# 🚀 Local LLM API Deployment (Day 5 Capstone)

## 📌 Overview

This project implements a **production-ready local LLM system** with:

* FastAPI backend for inference
* Fine-tuned TinyLlama model (LoRA)
* Quantized + optimized inference
* Chat + Generate endpoints
* Streamlit UI (ChatGPT-like interface)

---

## 🏗️ Architecture

```
Streamlit UI  →  FastAPI API  →  Local LLM Model
```

* UI handles user interaction
* FastAPI serves inference requests
* Model is loaded once (cached) for efficiency

---

## ⚙️ Features

✔ `/generate` endpoint (single prompt)
✔ `/chat` endpoint (conversation + memory)
✔ System + user prompts
✔ Chat history support
✔ Token controls (temperature, top-k, top-p)
✔ Request ID + latency tracking
✔ Model caching (fast inference)
✔ Streaming UI (typing effect)
✔ Production-ready API design

---

## 📁 Project Structure

```
Day-5/
│
├── deploy/
│   ├── app.py
│   ├── model_loader.py
│   ├── config.py
│   ├── schemas.py
│   ├── utils.py
│   └── requirements.txt
│
├── app_ui.py
├── cli.py (optional)
├── README.md
├── FINAL-REPORT.md
```

---

## 🚀 Setup & Run

### 🔹 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 🔹 2. Install Dependencies

```bash
pip install -r deploy/requirements.txt
```

---

### 🔹 3. Run FastAPI Server

```bash
cd deploy
uvicorn app:app --reload
```

👉 API will run at:

```
http://127.0.0.1:8000
```

---

### 🔹 4. Run Streamlit UI

```bash
streamlit run app_ui.py
```

👉 UI will run at:

```
http://localhost:8501
```

---

## 🔌 API Endpoints

### 🔹 POST `/generate`

**Request:**

```json
{
  "prompt": "Explain AI",
  "max_tokens": 200,
  "temperature": 0.7,
  "top_k": 50,
  "top_p": 0.9
}
```

---

### 🔹 POST `/chat`

**Request:**

```json
{
  "system_prompt": "You are a helpful assistant",
  "user_prompt": "Tell me a joke",
  "history": []
}
```

---

## 🧠 Model Details

* Base Model: TinyLlama-1.1B-Chat
* Fine-tuning: LoRA (PEFT)
* Quantization: INT8, INT4, GGUF
* Deployment: FP16 (fallback) / INT4 (if supported)

---

## 📊 Benchmark Insights (Day 4)

| Mode | Tokens/sec | Latency | VRAM    |
| ---- | ---------- | ------- | ------- |
| FP16 | ~32        | ~3s     | ~2.25GB |
| INT8 | ~9         | ~11s    | ~2.23GB |
| INT4 | ~22        | ~4–5s   | ~2.28GB |

---

## 🐳 Docker (Optional)

```bash
docker build -t llm-api .
docker run -p 8000:8000 llm-api
```

---

## 💡 Future Improvements

* Real-time streaming (SSE/WebSockets)
* RAG (chat with PDFs)
* Multi-user session handling
* Cloud deployment

---

## 👨‍💻 Author

Built as part of Week 8 LLM Engineering Capstone 🚀
