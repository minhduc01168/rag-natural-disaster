FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the model during build time so it doesn't download on every start
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('microsoft/harrier-oss-v1-0.6b')"

COPY . .

EXPOSE 8002

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
