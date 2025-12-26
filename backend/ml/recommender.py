import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from ml.preprocessing import preprocess_text

# Load once (important for performance)
courses = pd.read_csv("ml/data/courses.csv")
vectorizer = joblib.load("ml/artifacts/tfidf_vectorizer.pkl")
tfidf_matrix = joblib.load("ml/artifacts/course_tfidf_matrix.pkl")

def content_based_recommend(user_interests, top_k=5):
    user_text = preprocess_text(user_interests)
    user_vector = vectorizer.transform([user_text])

    similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()
    courses["content_score"] = similarity_scores

    return courses.sort_values(
        by="content_score", ascending=False
    ).head(top_k)
