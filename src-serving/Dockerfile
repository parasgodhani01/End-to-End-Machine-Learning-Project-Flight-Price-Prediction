# src_serving/Dockerfile
FROM python:3.10-slim

WORKDIR /workspace

# Install system dependencies needed for compiling tracking packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python engineering packages directly
RUN pip install --no-cache-dir \
    fastapi==0.110.0 \
    uvicorn==0.28.0 \
    pydantic==1.10.14 \
    scikit-learn==1.3.2 \
    pandas==2.1.4 \
    sqlalchemy==2.0.28 \
    psycopg2-binary==2.9.9 \
    joblib==1.3.2 \
    prometheus_client==0.20.0

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]