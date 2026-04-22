# === Dockerfile for the Core AGS Python Orchestrator ===
FROM python:3.11-slim

# Prevent python from writing bytecode 
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure console output is unbuffered
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies (build-essential for C extensions like ChromaDB SQLite)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Assuming you freeze requirements (pip install sqlmodel chromadb pydantic sentence-transformers litellm fastmcp redis sse-starlette uvicorn fastapi)
# Here we mock it inline since we generated it directly in standard format:
RUN pip install --no-cache-dir \
    sqlmodel \
    chromadb \
    pydantic \
    sentence-transformers \
    litellm \
    fastmcp \
    redis \
    sse-starlette \
    fastapi \
    uvicorn

COPY . /app/

# Port exposing the FastAPI SSE Stream endpoint
EXPOSE 8000

# Entrypoint booting the SSE API stream
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
