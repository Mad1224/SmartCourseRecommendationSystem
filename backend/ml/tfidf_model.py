from sklearn.feature_extraction.text import TfidfVectorizer
from ml.preprocessing import preprocess_text
import joblib
import os

def build_tfidf(corpus):
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),        # ✅ Unigrams + Bigrams
        max_df=0.85,               # ignore very common terms
        min_df=2,                  # ignore rare noise
        sublinear_tf=True,         # log scaling
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(corpus)
    return vectorizer, tfidf_matrix


if __name__ == "__main__":
    # Example dataset (replace with Mongo later)
    texts = [
        "Introduction to data science",
        "Machine learning for beginners",
        "Advanced artificial intelligence",
        "Python programming basics",
        "Deep learning and neural networks"
    ]

    cleaned = [preprocess_text(t) for t in texts]
    vectorizer, tfidf = build_tfidf(cleaned)

    os.makedirs("ml/artifacts", exist_ok=True)
    joblib.dump(vectorizer, "ml/artifacts/tfidf_vectorizer_v2.pkl")
    joblib.dump(tfidf, "ml/artifacts/tfidf_matrix_v2.pkl")

    print("Improved TF-IDF (bigrams + tuning) built successfully")
