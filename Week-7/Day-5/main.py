import os
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from src.deployment.app import App
from PIL import Image
import io

app_api = FastAPI(title="Multi-Modal RAG API", description="Production-ready API for RAG application")

# Initialize central RAG app globally so it's loaded once in the worker
rag_app = App()

class QueryRequest(BaseModel):
    query: str

class FeedbackRequest(BaseModel):
    query: str
    feedback: str

@app_api.get("/")
def health_check():
    return {"status": "ok", "message": "Multi-Modal RAG API is running"}

@app_api.post("/ask/text")
def ask_text(request: QueryRequest):
    """
    Standard QA using Text Retriever, MMR, and Reranker
    """
    result = rag_app.ask(request.query)
    return result

@app_api.post("/ask/image")
async def ask_image(query: Optional[str] = Form(None), file: Optional[UploadFile] = File(None)):
    """
    Multimodal image retrieval. Can accept image-to-image or text-to-image
    """
    if file:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        result = rag_app.ask_image(query=None, image_input=image)
    elif query:
        result = rag_app.ask_image(query=query)
    else:
        return {"error": "Must provide query or image file"}
    
    return result

@app_api.post("/ask/sql")
def ask_sql(request: QueryRequest):
    """
    Text-to-SQL functionality querying the pre-loaded DB
    """
    result = rag_app.ask_sql(request.query)
    return result

@app_api.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    """
    Log human feedback to continuous improvement
    """
    result = rag_app.feedback(request.query, request.feedback)
    return result

if __name__ == "__main__":
    import uvicorn
    # Make sure to run this via `uvicorn main:app_api --reload`
    uvicorn.run(app_api, host="0.0.0.0", port=8000)
