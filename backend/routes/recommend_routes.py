from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.mongo import mongo
import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ml.preprocessing import preprocess_text
from ml.hybrid_recommender import compute_content_similarity, compute_feedback_scores, hybrid_score
import os

recommend_routes = Blueprint(
    "recommend_routes",
    __name__,
    url_prefix="/recommend"
)

# Load AI models
ARTIFACTS_PATH = "ml/artifacts"
try:
    vectorizer = joblib.load(os.path.join(ARTIFACTS_PATH, "tfidf_vectorizer.pkl"))
    tfidf_matrix = joblib.load(os.path.join(ARTIFACTS_PATH, "course_tfidf_matrix.pkl"))
    print("✓ AI models loaded successfully")
except Exception as e:
    print(f"⚠ Warning: Could not load AI models: {e}")
    vectorizer = None
    tfidf_matrix = None

@recommend_routes.route("/", methods=["POST", "GET"])
@jwt_required()
def recommend():
    user_id = get_jwt_identity()
    
    # Get user preferences
    prefs = mongo.db.preferences.find_one(
        {"user_id": user_id},
        sort=[("created_at", -1)]
    )
    
    # Get all courses from database FIRST (before filtering)
    all_courses = list(mongo.db.courses.find({}))
    
    if not all_courses:
        return jsonify([]), 200
    
    # Get courses already taken by the user
    academic_data = mongo.db.academic_data.find_one({"user_id": user_id})
    taken_course_codes = set()
    if academic_data and academic_data.get("courses_taken"):
        taken_course_codes = {c.get("course_code") for c in academic_data.get("courses_taken", [])}
    
    # Also check enrollments
    enrollments = list(mongo.db.enrollments.find({"user_id": user_id}))
    for enrollment in enrollments:
        course = mongo.db.courses.find_one({"_id": enrollment.get("course_id")})
        if course:
            taken_course_codes.add(course.get("course_code"))
    
    # Get user feedback for collaborative filtering
    feedback_docs = list(mongo.db.feedback.find({"user_id": user_id}))
    num_feedback = len(feedback_docs)
    
    # Build user query from preferences
    user_interests = []
    if prefs:
        if prefs.get("kulliyyah"):
            user_interests.append(prefs.get("kulliyyah"))
        if prefs.get("preferredTypes"):
            user_interests.extend(prefs.get("preferredTypes"))
        if prefs.get("topics"):
            user_interests.extend(prefs.get("topics"))
        if prefs.get("goals"):
            user_interests.extend(prefs.get("goals"))
        # Add generic programming and computer science keywords for better matching
        user_interests.extend(["programming", "computer", "software", "data", "algorithm"])
        user_query = " ".join(user_interests) if user_interests else "computer science programming data software"
    else:
        user_query = "computer science programming data software algorithm"
    
    print(f"User query for recommendations: {user_query}")
    
    recommendations = []
    
    # Use AI models if available
    if vectorizer is not None and tfidf_matrix is not None:
        try:
            # Content-based scoring using TF-IDF (compute for ALL courses)
            user_text = preprocess_text(user_query)
            user_vector = vectorizer.transform([user_text])
            all_content_scores = compute_content_similarity(tfidf_matrix, user_vector)
            
            print(f"Content scores (top 5): {sorted(all_content_scores, reverse=True)[:5]}")
            
            # Collaborative filtering based on feedback (for ALL courses)
            all_course_ids = [str(c.get("_id")) for c in all_courses]
            all_feedback_scores = compute_feedback_scores(all_course_ids, feedback_docs)
            
            print(f"Feedback scores (top 5): {sorted(all_feedback_scores, reverse=True)[:5]}")
            
            # Hybrid recommendation (for ALL courses)
            all_final_scores = hybrid_score(all_content_scores, all_feedback_scores, num_feedback)
            
            print(f"Final scores (top 5): {sorted(all_final_scores, reverse=True)[:5]}")
            
            # Build recommendations - only include courses NOT taken
            for i, course in enumerate(all_courses):
                course_code = course.get("course_code")
                
                # Skip courses already taken
                if course_code in taken_course_codes:
                    continue
                    
                score = float(all_final_scores[i]) * 100  # Convert to percentage
                
                recommendations.append({
                    "_id": str(course.get("_id")),  # Add course ID for enrollment
                    "course_code": course_code,
                    "course_name": course.get("course_name"),
                    "description": course.get("description", ""),
                    "credit_hours": course.get("credit_hours", 3),
                    "level": course.get("level", 1),
                    "skills": course.get("skills", []),
                    "score": min(score, 99),
                    "reason": f"AI-matched based on your interests in {user_query} and past feedback"
                })
        except Exception as e:
            print(f"Error in AI recommendation: {e}")
            # Fallback to simple scoring
            available_courses = [c for c in all_courses if c.get("course_code") not in taken_course_codes]
            return fallback_recommend(available_courses, prefs, user_id)
    else:
        # Fallback if models not loaded
        available_courses = [c for c in all_courses if c.get("course_code") not in taken_course_codes]
        return fallback_recommend(available_courses, prefs, user_id)
    
    # Sort by score
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    
    return jsonify(recommendations[:10]), 200

def fallback_recommend(courses, prefs, user_id):
    """Simple recommendation without AI models"""
    import random
    recommendations = []
    
    for course in courses:
        base_score = 70 + random.randint(0, 25)
        
        if prefs:
            if prefs.get("preferredTime") == "Morning":
                base_score += 5
            if course.get("level", 0) <= prefs.get("semester", 8):
                base_score += 5
        
        recommendations.append({
            "course_code": course.get("course_code"),
            "course_name": course.get("course_name"),
            "description": course.get("description", ""),
            "credit_hours": course.get("capacity", 3),
            "level": course.get("level", 1),
            "skills": course.get("skills", []),
            "score": min(base_score, 99),
            "reason": f"Recommended based on your preferences"
        })
    
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(recommendations[:10]), 200
