import os
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from contextlib import asynccontextmanager

# Global variable to hold the model
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    # Set PyTorch threads to utilize all CPU cores efficiently
    num_threads = min(os.cpu_count() or 4, 8)
    torch.set_num_threads(num_threads)
    
    # Load the model on startup
    print(f"Loading embedding model 'microsoft/harrier-oss-v1-270m' with {num_threads} CPU threads...")
    model = SentenceTransformer("microsoft/harrier-oss-v1-270m")
    
    # Model warm-up to ensure instant execution on first query
    print("Warming up embedding model...")
    _ = model.encode(["Cảnh báo lũ quét sạt lở đất khẩn cấp"], convert_to_numpy=True)
    print("✅ Model loaded and warmed up successfully.")
    yield
    # Clean up resources on shutdown
    model = None
    print("Model unloaded.")

app = FastAPI(title="Embedding Service", lifespan=lifespan)

class EmbedRequest(BaseModel):
    texts: list[str]

class EmbedResponse(BaseModel):
    embeddings: list[list[float]]

@app.post("/embed", response_model=EmbedResponse)
async def embed_texts(request: EmbedRequest):
    if not request.texts:
        return EmbedResponse(embeddings=[])
    
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded yet.")

    try:
        n = len(request.texts)
        # Tối ưu batch_size: n <= 4 (query chat đơn lẻ) dùng batch_size=n; nhiều chunks dùng 64
        batch_size = 64 if n > 4 else n
        embeddings = model.encode(
            request.texts,
            batch_size=batch_size,
            show_progress_bar=(n > 20),
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return EmbedResponse(embeddings=embeddings.tolist())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

