def precision_at_k(retrieved, relevant, k):
    retrieved_k = retrieved[:k]
    relevant_set = set(relevant)
    hits = len([r for r in retrieved_k if r in relevant_set])
    return hits / k