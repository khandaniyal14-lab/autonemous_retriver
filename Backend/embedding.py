from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Tuple
model_name = "all-MiniLM-L6-v2"
    # Load embedding model
model = SentenceTransformer(model_name)

def build_faiss_index(
    chunks: List[str],
    model_name: str = "all-MiniLM-L6-v2",
    batch_size: int = 32,
    use_hnsw: bool = True
) -> Tuple[faiss.Index, np.ndarray]:
    """
    Build a FAISS vector index from text chunks.

    Parameters
    ----------
    chunks : List[str]
        List of document chunks.
    model_name : str
        SentenceTransformer model name.
    batch_size : int
        Batch size for embedding generation.
    use_hnsw : bool
        If True, uses HNSW index for faster search.

    Returns
    -------
    index : faiss.Index
        FAISS search index.
    embeddings : np.ndarray
        Generated embedding vectors.
    """
    

    # Generate embeddings in batches
    embeddings = model.encode(
        chunks,
        batch_size=batch_size,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]

    # Choose index type
    if use_hnsw:
        index = faiss.IndexHNSWFlat(dim, 32)
        index.hnsw.efConstruction = 40
    else:
        index = faiss.IndexFlatIP(dim)

    # Add embeddings to index
    index.add(embeddings)

    return index, embeddings