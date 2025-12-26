import joblib

vectorizer = joblib.load("ml/artifacts/tfidf_vectorizer_v2.pkl")
tfidf_matrix = joblib.load("ml/artifacts/tfidf_matrix_v2.pkl")