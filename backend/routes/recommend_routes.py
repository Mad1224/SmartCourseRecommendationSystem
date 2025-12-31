from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.mongo import mongo
from ml.recommendation_engine import recommendation_engine

recommend_routes = Blueprint(
    "recommend_routes",
    __name__,
    url_prefix="/recommend"
)

# Initialize engine on module load
recommendation_engine.load_models()

@recommend_routes.route("/", methods=["GET", "POST"])
@jwt_required()
def recommend():
    """
    Generate personalized course recommendations for the user
    Uses hybrid approach: content-based + collaborative filtering
    """
    user_id = get_jwt_identity()
    
    # Check if AI models are loaded
    if not recommendation_engine.is_loaded:
        return jsonify({
            "error": "AI models not loaded",
            "message": "Please contact administrator to rebuild AI models",
            "instructions": "Run: python rebuild_models.py"
        }), 503
    
    # ========== GET USER PREFERENCES ==========
    prefs = mongo.db.preferences.find_one(
        {"user_id": user_id},
        sort=[("created_at", -1)]
    )
    
    # ========== GET ALL COURSES FROM DATABASE ==========
    all_courses = list(mongo.db.courses.find({}))
    
    if not all_courses:
        return jsonify([]), 200
    
    # ========== GET COURSES ALREADY TAKEN ==========
    academic_data = mongo.db.academic_data.find_one({"user_id": user_id})
    taken_course_codes = set()
    
    if academic_data and academic_data.get("courses_taken"):
        taken_course_codes = {c.get("course_code") for c in academic_data.get("courses_taken", [])}
    
    # Also check current enrollments
    enrollments = list(mongo.db.enrollments.find({"user_id": user_id}))
    for enrollment in enrollments:
        course = mongo.db.courses.find_one({"_id": enrollment.get("course_id")})
        if course:
            taken_course_codes.add(course.get("course_code"))
    
    # ========== GET USER FEEDBACK FOR COLLABORATIVE FILTERING ==========
    feedback_docs = list(mongo.db.feedback.find({"user_id": user_id}))
    
    # ========== BUILD USER QUERY FROM PREFERENCES ==========
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
    
    # Add generic CS keywords to improve matching
    user_interests.extend([
        "programming", "computer", "software", "data", 
        "algorithm", "technology", "development"
    ])
    
    user_query = " ".join(user_interests) if user_interests else "computer science programming"
    
    print(f"\n{'='*60}")
    print(f"RECOMMENDATION REQUEST")
    print(f"{'='*60}")
    print(f"User ID: {user_id}")
    print(f"User Query: {user_query}")
    print(f"Total Courses: {len(all_courses)}")
    print(f"Taken Courses: {len(taken_course_codes)}")
    print(f"Feedback Count: {len(feedback_docs)}")
    
    # ========== PREPARE COURSE DATA ==========
    course_codes = [c.get("course_code") for c in all_courses]
    
    try:
        # ========== GENERATE HYBRID RECOMMENDATIONS ==========
        final_scores, alpha_used, content_scores, collab_scores = recommendation_engine.hybrid_recommend(
            user_query=user_query,
            course_codes=course_codes,
            feedback_docs=feedback_docs
        )
        
        print(f"Alpha (Content Weight): {alpha_used:.2f}")
        print(f"Content Scores - Max: {content_scores.max():.3f}, Mean: {content_scores.mean():.3f}")
        print(f"Collab Scores - Max: {collab_scores.max():.3f}, Mean: {collab_scores.mean():.3f}")
        print(f"Final Scores - Max: {final_scores.max():.3f}, Mean: {final_scores.mean():.3f}")
        
        # ========== BUILD RECOMMENDATIONS LIST ==========
        recommendations = []
        
        for i, course in enumerate(all_courses):
            course_code = course.get("course_code")
            
            # Skip courses already taken
            if course_code in taken_course_codes:
                continue
            
            score = float(final_scores[i]) * 100  # Convert to percentage
            
            # Generate explanation
            if len(feedback_docs) > 5:
                reason = f"Recommended based on your interests and past feedback (AI match: {score:.0f}%)"
            else:
                reason = f"AI-matched based on your interests in {', '.join(user_interests[:3])}"
            
            recommendations.append({
                "_id": str(course.get("_id")),
                "course_code": course_code,
                "course_name": course.get("course_name"),
                "description": course.get("description", ""),
                "credit_hours": course.get("credit_hours", 3),
                "level": course.get("level", 1),
                "skills": course.get("skills", []),
                "score": min(score, 99),  # Cap at 99%
                "reason": reason,
                "content_score": float(content_scores[i]) * 100,
                "collab_score": float(collab_scores[i]) * 100,
                "alpha": alpha_used
            })
        
        # Sort by score
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        print(f"Generated {len(recommendations)} recommendations")
        print(f"Top 5 scores: {[r['score'] for r in recommendations[:5]]}")
        print(f"{'='*60}\n")
        
        # Return top 10 recommendations
        return jsonify(recommendations[:10]), 200
        
    except Exception as e:
        print(f"❌ Error in recommendation: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": "Recommendation failed",
            "message": str(e)
        }), 500


@recommend_routes.route("/reload-models", methods=["POST"])
@jwt_required()
def reload_models():
    """
    Reload AI models (useful after rebuilding)
    Restricted to admin users only
    """
    user_id = get_jwt_identity()
    
    # Check if user is admin
    from bson import ObjectId
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    
    if not user or user.get("role") != "admin":
        return jsonify({"msg": "Admin access required"}), 403
    
    success = recommendation_engine.reload_models()
    
    if success:
        return jsonify({
            "msg": "Models reloaded successfully",
            "status": "ready"
        }), 200
    else:
        return jsonify({
            "msg": "Failed to reload models",
            "status": "not_ready"
        }), 500


@recommend_routes.route("/status", methods=["GET"])
@jwt_required()
def recommendation_status():
    """
    Check status of recommendation engine
    """
    return jsonify({
        "models_loaded": recommendation_engine.is_loaded,
        "status": "ready" if recommendation_engine.is_loaded else "not_ready",
        "vocabulary_size": len(recommendation_engine.vectorizer.vocabulary_) if recommendation_engine.is_loaded else 0,
        "matrix_shape": recommendation_engine.tfidf_matrix.shape if recommendation_engine.is_loaded else None
    }), 200