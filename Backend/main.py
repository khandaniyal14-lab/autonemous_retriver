from fastapi import FastAPI
import time
from fastapi.middleware.cors import CORSMiddleware
from data_loader import load_documents
from embedding import build_faiss_index, model
from hybrid import build_bm25, hybrid_search
from cache import get_cache, set_cache

app = FastAPI()
origins = [
    "http://localhost:3000",  # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],        # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],        # Allow all headers
)

chunks = load_documents()
index, embeddings = build_faiss_index(chunks)
bm25 = build_bm25(chunks)

@app.post("/search")
async def search(query: str):
    cached = get_cache(query)
    if cached:
        # Map indices to text
        text_results = [[chunks[i], score] for i, score in cached]
        return {"cached": True, "results": text_results}

    start = time.time()
    results = hybrid_search(query, index, bm25, chunks, model)
    latency = time.time() - start

    set_cache(query, results)

    # Map indices to text
    text_results = [[chunks[i], score] for i, score in results]

    seen = set()
    unique_results = []
    for text, score in text_results:
        if text not in seen:
            unique_results.append([text, score])
            seen.add(text)

    return {
        "cached": False,
        "latency": latency,
        "results": unique_results
    }