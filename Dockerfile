# Use a stable, slim Python base image
FROM python:3.12.12-slim

## 1. Environment Variables for Stability
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=1000 \
    # Ensure HuggingFace models are stored in a specific directory
    HF_HOME=/app/cache/huggingface

## 2. Set Work Directory
WORKDIR /app

## 3. Install System Dependencies (Optimized)
# Added libgomp1: Essential for faiss-cpu and many math libraries to run
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

## 4. Install Heavy Dependencies First (Caching Strategy)
# We copy ONLY requirements first. This ensures that if you change 
# your Python code, Docker skips this 10-minute install step.
COPY requirements.txt .

# Fault-Tolerant Pip Install:
# We use a high timeout and retries to handle large AI library downloads
RUN pip install --upgrade pip && \
    pip install --retries 3 --timeout 1000 -r requirements.txt

## 5. Copy Application Code
# We do this LAST because your code changes most frequently.
COPY . .

# Create cache directory for HuggingFace models
RUN mkdir -p /app/cache/huggingface && chmod -R 777 /app/cache

## 6. Runtime Configuration
EXPOSE 5000

# Use a healthcheck to ensure the container is truly "alive"
# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#     CMD curl -f http://localhost:5000/ || exit 1

## 7. Run the Flask app
CMD ["python", "app/application.py"]