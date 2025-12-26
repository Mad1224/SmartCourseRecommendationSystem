from sklearn.metrics.pairwise import cosine_similarity

def cosine_sim(matrix, query_vec):
    return cosine_similarity(query_vec, matrix).flatten()