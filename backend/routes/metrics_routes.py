"""
Data Quality and Recommendation Metrics Monitoring
Provides insights into dataset health and recommendation accuracy
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from database.mongo import mongo
from datetime import datetime, timedelta
import numpy as np

metrics_bp = Blueprint("metrics", __name__, url_prefix="/metrics")

@metrics_bp.route("/data-quality", methods=["GET"])
@jwt_required()
def data_quality():
    """Analyze dataset quality and completeness"""
    
    # Course metrics
    total_courses = mongo.db.courses.count_documents({})
    courses_with_desc = mongo.db.courses.count_documents({"description": {"$exists": True, "$ne": ""}})
    courses_with_skills = mongo.db.courses.count_documents({"skills": {"$exists": True, "$ne": []}})
    
    courses_by_level = {}
    for level in range(1, 5):
        count = mongo.db.courses.count_documents({"level": level})
        courses_by_level[f"level_{level}"] = count
    
    # User metrics
    total_users = mongo.db.users.count_documents({"role": "student"})
    users_with_prefs = mongo.db.preferences.distinct("user_id")
    
    # Feedback metrics
    total_feedback = mongo.db.feedback.count_documents({})
    
    if total_feedback > 0:
        feedbacks = list(mongo.db.feedback.find({}, {"rating": 1}))
        ratings = [f["rating"] for f in feedbacks if "rating" in f]
        avg_rating = np.mean(ratings) if ratings else 0
        rating_distribution = {
            "5_stars": sum(1 for r in ratings if r == 5),
            "4_stars": sum(1 for r in ratings if r == 4),
            "3_stars": sum(1 for r in ratings if r == 3),
            "2_stars": sum(1 for r in ratings if r == 2),
            "1_star": sum(1 for r in ratings if r == 1),
        }
    else:
        avg_rating = 0
        rating_distribution = {}
    
    # Enrollment metrics
    total_enrollments = mongo.db.enrollments.count_documents({})
    
    # Data quality scores (0-100)
    course_completeness = (courses_with_desc / total_courses * 100) if total_courses > 0 else 0
    user_engagement = (len(users_with_prefs) / total_users * 100) if total_users > 0 else 0
    feedback_coverage = (total_feedback / (total_courses * 3) * 100) if total_courses > 0 else 0  # Aim for 3 feedbacks per course
    
    overall_quality = (course_completeness + user_engagement + feedback_coverage) / 3
    
    # Recommendations
    recommendations = []
    if total_courses < 20:
        recommendations.append({
            "priority": "high",
            "issue": "Insufficient courses",
            "detail": f"Only {total_courses} courses. Recommended: 20+ for testing, 100+ for production",
            "action": "Add more courses to improve recommendation diversity"
        })
    
    if len(users_with_prefs) < 5:
        recommendations.append({
            "priority": "high",
            "issue": "Low user preference data",
            "detail": f"Only {len(users_with_prefs)} users with preferences",
            "action": "Encourage users to set their preferences"
        })
    
    if total_feedback < 20:
        recommendations.append({
            "priority": "medium",
            "issue": "Insufficient feedback",
            "detail": f"Only {total_feedback} feedback entries. Recommended: 50+ for collaborative filtering",
            "action": "Collect more course feedback from users"
        })
    
    if courses_with_skills < total_courses * 0.8:
        recommendations.append({
            "priority": "medium",
            "issue": "Missing course skills data",
            "detail": f"{total_courses - courses_with_skills} courses missing skills tags",
            "action": "Add skills/tags to all courses for better matching"
        })
    
    return jsonify({
        "timestamp": datetime.utcnow().isoformat(),
        "overall_quality_score": round(overall_quality, 1),
        "dataset": {
            "courses": {
                "total": total_courses,
                "with_descriptions": courses_with_desc,
                "with_skills": courses_with_skills,
                "by_level": courses_by_level,
                "completeness_score": round(course_completeness, 1)
            },
            "users": {
                "total": total_users,
                "with_preferences": len(users_with_prefs),
                "engagement_score": round(user_engagement, 1)
            },
            "feedback": {
                "total": total_feedback,
                "average_rating": round(avg_rating, 2),
                "distribution": rating_distribution,
                "coverage_score": round(feedback_coverage, 1)
            },
            "enrollments": {
                "total": total_enrollments
            }
        },
        "recommendations": recommendations,
        "status": "excellent" if overall_quality >= 80 else "good" if overall_quality >= 60 else "needs_improvement"
    }), 200


@metrics_bp.route("/recommendation-accuracy", methods=["GET"])
@jwt_required()
def recommendation_accuracy():
    """Measure recommendation system performance"""
    
    # Get recent recommendations (would need to log these)
    # For now, calculate based on feedback
    
    total_courses = mongo.db.courses.count_documents({})
    total_feedback = mongo.db.feedback.count_documents({})
    
    if total_feedback == 0:
        return jsonify({
            "error": "Not enough data to calculate accuracy",
            "message": "Need at least 10 feedback entries to measure accuracy"
        }), 200
    
    # Calculate metrics based on feedback
    feedbacks = list(mongo.db.feedback.find({}, {"rating": 1, "user_id": 1, "course_code": 1}))
    
    # Satisfaction rate (4-5 star ratings)
    high_ratings = sum(1 for f in feedbacks if f.get("rating", 0) >= 4)
    satisfaction_rate = (high_ratings / total_feedback * 100) if total_feedback > 0 else 0
    
    # User coverage (how many users gave feedback)
    unique_users = len(set(f["user_id"] for f in feedbacks))
    total_users = mongo.db.users.count_documents({"role": "student"})
    user_coverage = (unique_users / total_users * 100) if total_users > 0 else 0
    
    # Course coverage (how many courses have feedback)
    unique_courses = len(set(f["course_code"] for f in feedbacks))
    course_coverage = (unique_courses / total_courses * 100) if total_courses > 0 else 0
    
    # Diversity score (variety in recommendations)
    diversity_score = course_coverage  # Higher is better
    
    # Calculate overall accuracy estimate
    accuracy_estimate = (satisfaction_rate * 0.5 + user_coverage * 0.3 + diversity_score * 0.2)
    
    return jsonify({
        "timestamp": datetime.utcnow().isoformat(),
        "accuracy_estimate": round(accuracy_estimate, 1),
        "metrics": {
            "satisfaction_rate": round(satisfaction_rate, 1),
            "user_coverage": round(user_coverage, 1),
            "course_coverage": round(course_coverage, 1),
            "diversity_score": round(diversity_score, 1)
        },
        "details": {
            "total_feedback": total_feedback,
            "high_ratings": high_ratings,
            "unique_users": unique_users,
            "unique_courses": unique_courses
        },
        "status": "excellent" if accuracy_estimate >= 80 else "good" if accuracy_estimate >= 60 else "needs_improvement"
    }), 200


@metrics_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def metrics_dashboard():
    """Complete metrics dashboard"""
    
    # Quick stats
    stats = {
        "courses": mongo.db.courses.count_documents({}),
        "users": mongo.db.users.count_documents({"role": "student"}),
        "preferences": mongo.db.preferences.count_documents({}),
        "feedback": mongo.db.feedback.count_documents({}),
        "enrollments": mongo.db.enrollments.count_documents({})
    }
    
    # Recent activity
    recent_enrollments = mongo.db.enrollments.count_documents({
        "enrolled_at": {"$gte": datetime.utcnow() - timedelta(days=7)}
    })
    
    recent_feedback = mongo.db.feedback.count_documents({
        "_id": {"$gte": datetime.utcnow() - timedelta(days=7)}
    })
    
    # Data health
    data_health = "healthy" if stats["courses"] >= 20 and stats["feedback"] >= 20 else "needs_data"
    
    return jsonify({
        "timestamp": datetime.utcnow().isoformat(),
        "quick_stats": stats,
        "recent_activity": {
            "enrollments_last_7_days": recent_enrollments,
            "feedback_last_7_days": recent_feedback
        },
        "data_health": data_health,
        "ai_status": "active" if stats["courses"] >= 4 else "insufficient_data"
    }), 200
