# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (important for torch, etc.)
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (for caching)
COPY deploy/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

# Move into deploy folder (where app.py is)
WORKDIR /app/deploy

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]