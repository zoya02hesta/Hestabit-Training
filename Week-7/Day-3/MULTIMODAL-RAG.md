# Multimodal RAG System

## Overview
This system supports retrieval using both text and images.

## Features
- OCR extraction using Tesseract
- Image captioning using BLIP
- CLIP embeddings for similarity search
- Supports text-to-image and image-to-image retrieval

## Pipeline
1. Input image
2. Extract text (OCR)
3. Generate caption
4. Generate embeddings
5. Store in vector DB

## Query Modes
- Text → Image
- Image → Image
- Image → Text

## Benefits
- Better retrieval accuracy
- Handles scanned documents
- Reduces hallucination