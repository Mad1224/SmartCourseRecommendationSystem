import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

from app import create_app
from database.mongo import mongo
from ml.preprocessing import preprocess_text

# Create Flask app context
app = create_app()

with app.app_context():
    courses = list(mongo.db.courses.find())

    texts = []

for c in courses:
    title = c.get("title", "")
    desc = c.get("description", "")

    # Force meaningful content
    combined = f"{title} course {desc}".strip().lower()

    if not combined:
        combined = "general course"

    texts.append(combined)


print("=== RAW COURSE TEXTS ===")
for i, t in enumerate(texts):
    print(i, repr(t))

    vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    token_pattern=r"(?u)\b\w+\b",
    min_df=1
)



    tfidf_matrix = vectorizer.fit_transform(texts)

    joblib.dump(vectorizer, "ml/artifacts/tfidf_vectorizer_v2.pkl")
    joblib.dump(tfidf_matrix, "ml/artifacts/tfidf_matrix_v2.pkl")

    print("TF-IDF rebuilt successfully!")
    print("Number of courses:", len(courses))
    print("TF-IDF shape:", tfidf_matrix.shape)
