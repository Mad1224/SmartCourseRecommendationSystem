def precision_at_k(recommended, relevant, k=3):
    recommended_k = recommended[:k]
    relevant_set = set(relevant)
    hits = sum(1 for r in recommended_k if r in relevant_set)
    return hits / k
