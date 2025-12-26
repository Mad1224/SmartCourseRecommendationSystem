import numpy as np

def precision_at_k(recommended_ids, relevant_ids, k):
    recommended_k = recommended_ids[:k]
    relevant_set = set(relevant_ids)

    if not recommended_k:
        return 0.0

    hit_count = sum(1 for cid in recommended_k if cid in relevant_set)
    return hit_count / k
##def precision_at_k(recommended, relevant, k):
    ##if k == 0:
      ##  return 0.0
    ##return len(set(recommended[:k]) & set(relevant)) / k


##def recall_at_k(recommended, relevant, k):
    ##if not relevant:
       ## return 0.0
    ##return len(set(recommended[:k]) & set(relevant)) / len(relevant)

def hit_rate_at_k(recommended_ids, relevant_ids, k):
    recommended_k = recommended_ids[:k]
    relevant_set = set(relevant_ids)

    for cid in recommended_k:
        if cid in relevant_set:
            return 1.0
    return 0.0