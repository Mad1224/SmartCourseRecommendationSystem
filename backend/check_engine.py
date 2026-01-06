"""Check if recommendation engine is loaded"""
from ml.recommendation_engine import recommendation_engine

print(f"Engine is_loaded: {recommendation_engine.is_loaded}")
print(f"Vectorizer: {recommendation_engine.vectorizer}")
print(f"Matrix: {recommendation_engine.tfidf_matrix}")

# Try loading
print("\nAttempting to load models...")
success = recommendation_engine.load_models()
print(f"Load successful: {success}")
print(f"Engine is_loaded after: {recommendation_engine.is_loaded}")
