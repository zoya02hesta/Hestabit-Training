
# 🚀 Deployment Notes — GenAI Retrieval System (Day 5)

## 📌 Overview
This project is a multi-modal GenAI system supporting:
- Text-based retrieval (semantic search)
- Image search using embeddings
- SQL query handling
- Hallucination detection
- Confidence scoring
- Memory + refinement loop
- Streamlit UI

---

## 🏗️ Architecture

### Components
- **Frontend**: Streamlit (`streamlit_app.py`)
- **Backend Core**: `src/deployment/app.py`
- **Retrieval Layer**:
  - TextRetriever (Sentence Transformers)
  - ImageSearch (CLIP / embeddings)
- **Memory**: In-memory (last 5 interactions)
- **Refinement Loop**: Improves low-confidence responses
- **SQL Engine**: LLM-based query execution

---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone <repo-url>
cd <project-folder>
````

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables (if applicable)

Create `.env` file:

```env
HF_TOKEN=your_huggingface_token
GROQ_API_KEY=your_groq_key
```

---

## ▶️ Run the Application

### Start Streamlit UI

```bash
streamlit run streamlit_app.py
```

---

## 📁 Project Structure

```
Week-7/
│── streamlit_app.py
│── src/
│   ├── deployment/
│   │   ├── app.py
│   ├── retrieval/
│   │   ├── text_retriever.py
│   │   ├── image_search.py
│   ├── data/
│   │   ├── images/
│   │   ├── documents/
```

---

## 🧠 Features

### ✔ Text Retrieval

* Uses `sentence-transformers/all-MiniLM-L6-v2`
* Semantic similarity search

### ✔ Image Search

* Embedding-based image matching
* Query → vector → similarity search

### ✔ Memory (Last 5 interactions)

* Uses `collections.deque`
* Stores:

  * Query
  * Response

### ✔ Refinement Loop

* Triggered when confidence < threshold (e.g., 0.5)
* Improves response quality using refined query

### ✔ Hallucination Detection

* Based on confidence score
* If confidence is low → marked as hallucinated

### ✔ Confidence Score

* Derived from cosine similarity scores
* Used to evaluate response quality

---

## 🛠️ Debugging & Logging

Logs include:

* Incoming query
* Retrieved results
* Confidence scores
* Hallucination flag

---

## ⚠️ Known Limitations

* Memory is not persistent (resets on restart)
* Image search depends on embedding quality
* Confidence threshold is heuristic-based
* SQL queries depend on LLM accuracy

---

## 🚀 Deployment Options

### 1. Streamlit Cloud

* Push code to GitHub
* Connect repo to Streamlit Cloud
* Set environment variables

### 2. Docker (Optional)

```bash
docker build -t genai-app .
docker run -p 8501:8501 genai-app
```

### 3. Cloud Deployment

* AWS EC2 / GCP VM / Azure VM
* Run using:

```bash
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 🔐 Security Considerations

* Do not expose API keys in code
* Use `.env` for sensitive credentials
* Enable input validation for SQL queries

---

## 📈 Future Improvements

* Persistent memory (vector DB like FAISS / Chroma)
* Advanced hallucination detection using LLMs
* Better image-text multimodal search
* Authentication & user sessions
* Scalable API backend (FastAPI)

---


