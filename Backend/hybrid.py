from rank_bm25 import BM25Okapi
import numpy as np
import faiss


def build_bm25(chunks):
    tokenized = [c.split() for c in chunks]
    return BM25Okapi(tokenized)

def hybrid_search(query, index, bm25, chunks, model, alpha=0.6, top_k=5):

    # Dense
    query_vec = model.encode([query])
    faiss.normalize_L2(query_vec)
    D, I = index.search(query_vec, top_k)

    dense_scores = {idx: score for score, idx in zip(D[0], I[0])}

    # Sparse
    sparse_scores = bm25.get_scores(query.split())

    combined = []
    for i in range(len(chunks)):
        d = dense_scores.get(i, 0)
        s = sparse_scores[i]
        score = alpha * d + (1 - alpha) * s
        combined.append((i, score))

    combined.sort(key=lambda x: x[1], reverse=True)

    return combined[:top_k]