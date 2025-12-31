"""
Evaluate recommendation system accuracy
Tests Precision@K, Recall@K, and Hit Rate@K
"""
from app import create_app
from database.mongo import mongo
from ml.recommendation_engine import recommendation_engine
from ml.preprocessing import preprocess_text
import numpy as np

# Configuration
K_VALUES = [3, 5, 10]
RELEVANCE_THRESHOLD = 4  # Rating >= 4 is considered relevant

# Initialize Flask app
app = create_app()

def run_evaluation():
    """Run evaluation on all users with feedback"""
    
    with app.app_context():
        # Load models
        if not recommendation_engine.load_models():
            print("❌ Failed to load models. Run rebuild_models.py first.")
            return
        
        print("\n" + "="*60)
        print("RECOMMENDATION SYSTEM EVALUATION")
        print("="*60)
        
        # Get all users
        users = list(mongo.db.users.find({"role": "student"}))
        print(f"Found {len(users)} student users")
        
        # Store evaluation results
        all_results = {k: {"precision": [], "recall": [], "hit_rate": []} for k in K_VALUES}
        evaluated_users = 0
        
        for user in users:
            user_id = str(user["_id"])
            user_name = user.get("name", "Unknown")
            
            # Get user's feedback
            feedback = list(mongo.db.feedback.find({"user_id": user_id}))
            
            if not feedback:
                continue  # Skip users with no feedback
            
            # Identify relevant courses (rating >= RELEVANCE_THRESHOLD)
            relevant_course_codes = [
                fb["course_code"]
                for fb in feedback
                if fb.get("rating", 0) >= RELEVANCE_THRESHOLD
            ]
            
            if not relevant_course_codes:
                continue  # Skip users with no relevant courses
            
            evaluated_users += 1
            
            # Build user query from feedback comments
            query_text = " ".join([fb.get("comment", "") for fb in feedback])
            if not query_text.strip():
                query_text = "computer science programming"  # Fallback
            
            # Get all courses
            all_courses = list(mongo.db.courses.find({}))
            course_codes = [c["course_code"] for c in all_courses]
            
            # Generate recommendations
            try:
                final_scores, alpha, _, _ = recommendation_engine.hybrid_recommend(
                    user_query=query_text,
                    course_codes=course_codes,
                    feedback_docs=feedback
                )
                
                # Get ranked course codes
                ranked_indices = np.argsort(final_scores)[::-1]
                recommended_codes = [course_codes[i] for i in ranked_indices]
                
                # Evaluate for each K
                for k in K_VALUES:
                    precision = recommendation_engine.precision_at_k(
                        recommended_codes, relevant_course_codes, k
                    )
                    recall = recommendation_engine.recall_at_k(
                        recommended_codes, relevant_course_codes, k
                    )
                    hit_rate = recommendation_engine.hit_rate_at_k(
                        recommended_codes, relevant_course_codes, k
                    )
                    
                    all_results[k]["precision"].append(precision)
                    all_results[k]["recall"].append(recall)
                    all_results[k]["hit_rate"].append(hit_rate)
                
                print(f"✓ Evaluated {user_name}: {len(relevant_course_codes)} relevant courses")
                
            except Exception as e:
                print(f"✗ Error evaluating {user_name}: {e}")
                continue
        
        # Calculate and display results
        print("\n" + "="*60)
        print("EVALUATION RESULTS")
        print("="*60)
        print(f"Evaluated Users: {evaluated_users}")
        print(f"Relevance Threshold: {RELEVANCE_THRESHOLD} stars\n")
        
        if evaluated_users == 0:
            print("⚠️  No users with sufficient feedback to evaluate")
            return
        
        for k in K_VALUES:
            precision_scores = all_results[k]["precision"]
            recall_scores = all_results[k]["recall"]
            hit_rate_scores = all_results[k]["hit_rate"]
            
            avg_precision = np.mean(precision_scores) if precision_scores else 0
            avg_recall = np.mean(recall_scores) if recall_scores else 0
            avg_hit_rate = np.mean(hit_rate_scores) if hit_rate_scores else 0
            
            print(f"K = {k}:")
            print(f"  Precision@{k}: {avg_precision:.3f}")
            print(f"  Recall@{k}:    {avg_recall:.3f}")
            print(f"  Hit Rate@{k}:  {avg_hit_rate:.3f}")
            print()
        
        print("="*60)
        print("\n✅ Evaluation complete!\n")


if __name__ == "__main__":
    run_evaluation()