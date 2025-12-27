"""
Rebuild TF-IDF models from MongoDB courses
"""
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from ml.preprocessing import preprocess_text
import joblib
import os

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['fyp2']

# Get all courses
courses = list(db.courses.find({}))

if not courses:
    print("❌ No courses found in database!")
    exit(1)

print(f"Found {len(courses)} courses")

# Prepare corpus (course descriptions)
corpus = []
course_codes = []

for course in courses:
    # Combine relevant text fields
    text_parts = []
    
    if course.get('course_name'):
        text_parts.append(course['course_name'])
    
    if course.get('description'):
        text_parts.append(course['description'])
    
    if course.get('skills'):
        text_parts.extend(course['skills'])
    
    # Join and preprocess
    full_text = " ".join(text_parts)
    cleaned_text = preprocess_text(full_text)
    
    corpus.append(cleaned_text)
    course_codes.append(course.get('course_code'))
    
    print(f"  {course.get('course_code')}: {full_text[:50]}...")

# Build TF-IDF
print("\nBuilding TF-IDF model...")
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),        # Unigrams + Bigrams
    max_df=0.85,               
    min_df=1,                  # Lower for small dataset
    sublinear_tf=True,         
    stop_words="english"
)

tfidf_matrix = vectorizer.fit_transform(corpus)

print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")
print(f"Vocabulary size: {len(vectorizer.vocabulary_)}")

# Save models
os.makedirs("ml/artifacts", exist_ok=True)
joblib.dump(vectorizer, "ml/artifacts/tfidf_vectorizer.pkl")
joblib.dump(tfidf_matrix, "ml/artifacts/course_tfidf_matrix.pkl")

print("\n✓ TF-IDF models saved successfully!")
print("  - ml/artifacts/tfidf_vectorizer.pkl")
print("  - ml/artifacts/course_tfidf_matrix.pkl")
