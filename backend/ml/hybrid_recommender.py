import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from bson import ObjectId

# ---------------- ADAPTIVE ALPHA ----------------
def adaptive_alpha(num_feedback, min_alpha=0.3, max_alpha=0.8):
    if num_feedback <= 0:
        return max_alpha
    alpha = max_alpha - (num_feedback * 0.05)
    return max(min_alpha, alpha)

# ---------------- CONTENT ----------------
def compute_content_similarity(tfidf_matrix, query_vector):
    return cosine_similarity(query_vector, tfidf_matrix).flatten()

# ---------------- FEEDBACK ----------------
def compute_feedback_scores(course_ids, feedback_docs):
    # Initialize feedback score vector with zeros
    scores = {cid: 0.0 for cid in course_ids}
    counts = {cid: 0 for cid in course_ids}

    for fb in feedback_docs:
        cid = fb.get("course_id")

        if cid in scores:
            scores[cid] += fb.get("rating", 1)
            counts[cid] += 1

    # Average ratings where feedback exists
    for cid in scores:
        if counts[cid] > 0:
            scores[cid] /= counts[cid]

    # IMPORTANT: return scores in SAME ORDER as course_ids
    return np.array([scores[cid] for cid in course_ids])


# ---------------- HYBRID ----------------
def hybrid_score(content_scores, feedback_scores, num_feedback):
    alpha = adaptive_alpha(num_feedback)

    feedback_scores = feedback_scores / (np.max(feedback_scores) + 1e-6)
    final_scores = alpha * content_scores + (1 - alpha) * feedback_scores
    return final_scores
