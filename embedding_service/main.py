from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from contextlib import asynccontextmanager

# Global variable to hold the model
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    # Load the model on startup
    print("Loading embedding model 'microsoft/harrier-oss-v1-270m'...")
    model = SentenceTransformer("microsoft/harrier-oss-v1-270m")
    print("Model loaded successfully.")
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
        print(f"[EmbedService] Encoding {n} texts với batch_size=32...")
        # batch_size=32: xử lý 32 chunks/lần → tránh OOM trên CPU
        # show_progress_bar=True: in progress ra log để dễ debug
        embeddings = model.encode(
            request.texts,
            batch_size=32,
            show_progress_bar=(n > 10),  # chỉ hiện progress khi nhiều chunk
            convert_to_numpy=True,
        )
        print(f"[EmbedService] ✅ Done {n} texts.")
        return EmbedResponse(embeddings=embeddings.tolist())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}
