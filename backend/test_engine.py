"""
Test recommendation engine with new models directly
"""
from pymongo import MongoClient
from ml.recommendation_engine import RecommendationEngine

# Initialize engine
engine = RecommendationEngine()

# Load models
success = engine.load_models()

if success:
    print("✅ Models loaded successfully!")
    print(f"   TF-IDF matrix shape: {engine.tfidf_matrix.shape}")
    print(f"   Expected: (106, ...)")
    
    # Test recommendation
    print("\n🔍 Testing recommendation...")
    test_query = "I want to learn about machine learning and artificial intelligence"
    
    try:
        scores = engine.compute_content_similarity(test_query)
        print(f"✅ Recommendation works!")
        print(f"   Generated {len(scores)} scores")
        print(f"   Score range: [{scores.min():.3f}, {scores.max():.3f}]")
        
        # Get top 5 courses
        client = MongoClient('mongodb://localhost:27017/')
        db = client['fyp2']
        courses = list(db.courses.find({}))
        
        # Sort by score
        course_scores = [(courses[i]['course_code'], courses[i]['course_name'], scores[i]) 
                        for i in range(len(courses))]
        course_scores.sort(key=lambda x: x[2], reverse=True)
        
        print("\n🎯 Top 5 recommended courses:")
        for code, name, score in course_scores[:5]:
            print(f"   {code}: {name} (score: {score:.3f})")
            
    except Exception as e:
        print(f"❌ Error testing recommendation: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ Failed to load models")
