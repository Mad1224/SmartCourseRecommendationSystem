from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.mongo import mongo
from bson import ObjectId
from datetime import datetime

feedback_bp = Blueprint("feedback", __name__, url_prefix="/feedback")

@feedback_bp.route("/", methods=["POST"])
@jwt_required()
def add_feedback():
    """
    Submit feedback for a course
    Expected JSON:
    {
        "course_code": "CSCI4101",
        "rating": 5,
        "comment": "Great course!"
    }
    """
    user_id = get_jwt_identity()
    data = request.json

    course_code = data.get("course_code")
    rating = data.get("rating")
    comment = data.get("comment", "")

    # Validation
    if not course_code or not rating:
        return jsonify({"msg": "Course code and rating required"}), 400
    
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({"msg": "Rating must be between 1 and 5"}), 400

    # Get course details
    course = mongo.db.courses.find_one({"course_code": course_code})
    if not course:
        return jsonify({"msg": "Course not found"}), 404

    # Get user details
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Check if user has taken this course (from academic data)
    academic_data = mongo.db.academic_data.find_one({"user_id": user_id})
    if not academic_data:
        return jsonify({"msg": "You haven't taken any courses yet"}), 400
    
    courses_taken = academic_data.get("courses_taken", [])
    course_codes_taken = [c["course_code"] for c in courses_taken]
    
    if course_code not in course_codes_taken:
        return jsonify({"msg": "You can only give feedback for courses you have taken"}), 400

    # Check if user already gave feedback for this course
    existing_feedback = mongo.db.feedback.find_one({
        "user_id": user_id,
        "course_code": course_code
    })

    if existing_feedback:
        return jsonify({"msg": "You have already submitted feedback for this course"}), 400

    # Create feedback document
    feedback_doc = {
        "user_id": user_id,
        "user_name": user.get("name", "Anonymous"),
        "course_code": course_code,
        "course_name": course.get("course_name", ""),
        "rating": rating,
        "comment": comment,
        "likes": 0,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }

    result = mongo.db.feedback.insert_one(feedback_doc)

    return jsonify({
        "msg": "Feedback submitted successfully",
        "feedback_id": str(result.inserted_id)
    }), 201


@feedback_bp.route("/all", methods=["GET"])
@jwt_required()
def get_all_feedback():
    """Get all feedback from all users (public view)"""
    try:
        # Get all feedback sorted by creation date (newest first)
        feedback_list = list(mongo.db.feedback.find().sort("created_at", -1))
        
        # Remove MongoDB _id field and user_id for privacy
        for fb in feedback_list:
            fb["_id"] = str(fb["_id"])
            fb.pop("user_id", None)  # Remove user_id for privacy
        
        return jsonify(feedback_list), 200
    except Exception as e:
        return jsonify({"msg": f"Error fetching feedback: {str(e)}"}), 500


@feedback_bp.route("/course/<course_code>", methods=["GET"])
@jwt_required()
def get_course_feedback(course_code):
    """Get all feedback for a specific course"""
    try:
        feedback_list = list(mongo.db.feedback.find({"course_code": course_code}).sort("created_at", -1))
        
        if not feedback_list:
            return jsonify([]), 200
        
        # Calculate average rating
        total_rating = sum(fb.get("rating", 0) for fb in feedback_list)
        avg_rating = total_rating / len(feedback_list)
        
        # Format feedback
        for fb in feedback_list:
            fb["_id"] = str(fb["_id"])
            fb.pop("user_id", None)
        
        return jsonify({
            "course_code": course_code,
            "average_rating": round(avg_rating, 2),
            "total_feedback": len(feedback_list),
            "feedback": feedback_list
        }), 200
    except Exception as e:
        return jsonify({"msg": f"Error fetching feedback: {str(e)}"}), 500


@feedback_bp.route("/my", methods=["GET"])
@jwt_required()
def get_my_feedback():
    """Get feedback submitted by current user"""
    user_id = get_jwt_identity()
    
    try:
        feedback_list = list(mongo.db.feedback.find({"user_id": user_id}).sort("created_at", -1))
        
        for fb in feedback_list:
            fb["_id"] = str(fb["_id"])
        
        return jsonify(feedback_list), 200
    except Exception as e:
        return jsonify({"msg": f"Error fetching your feedback: {str(e)}"}), 500


@feedback_bp.route("/<feedback_id>", methods=["PUT"])
@jwt_required()
def update_feedback(feedback_id):
    """
    Update existing feedback
    Expected JSON:
    {
        "rating": 4,
        "comment": "Updated comment"
    }
    """
    user_id = get_jwt_identity()
    data = request.json

    try:
        # Find feedback
        feedback = mongo.db.feedback.find_one({"_id": ObjectId(feedback_id)})
        
        if not feedback:
            return jsonify({"msg": "Feedback not found"}), 404
        
        # Check ownership
        if feedback.get("user_id") != user_id:
            return jsonify({"msg": "Unauthorized"}), 403
        
        # Update fields
        update_data = {}
        if "rating" in data:
            rating = data["rating"]
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                return jsonify({"msg": "Rating must be between 1 and 5"}), 400
            update_data["rating"] = rating
        
        if "comment" in data:
            update_data["comment"] = data["comment"]
        
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        # Update in database
        mongo.db.feedback.update_one(
            {"_id": ObjectId(feedback_id)},
            {"$set": update_data}
        )
        
        return jsonify({"msg": "Feedback updated successfully"}), 200
    
    except Exception as e:
        return jsonify({"msg": f"Error updating feedback: {str(e)}"}), 500


@feedback_bp.route("/<feedback_id>", methods=["DELETE"])
@jwt_required()
def delete_feedback(feedback_id):
    """Delete feedback (only by owner or admin)"""
    user_id = get_jwt_identity()
    
    try:
        # Find feedback
        feedback = mongo.db.feedback.find_one({"_id": ObjectId(feedback_id)})
        
        if not feedback:
            return jsonify({"msg": "Feedback not found"}), 404
        
        # Check ownership or admin
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        is_admin = user.get("role") == "admin"
        is_owner = feedback.get("user_id") == user_id
        
        if not (is_owner or is_admin):
            return jsonify({"msg": "Unauthorized"}), 403
        
        # Delete feedback
        mongo.db.feedback.delete_one({"_id": ObjectId(feedback_id)})
        
        return jsonify({"msg": "Feedback deleted successfully"}), 200
    
    except Exception as e:
        return jsonify({"msg": f"Error deleting feedback: {str(e)}"}), 500


@feedback_bp.route("/<feedback_id>/like", methods=["POST"])
@jwt_required()
def like_feedback(feedback_id):
    """Like a feedback (increment like count)"""
    try:
        result = mongo.db.feedback.update_one(
            {"_id": ObjectId(feedback_id)},
            {"$inc": {"likes": 1}}
        )
        
        if result.modified_count == 0:
            return jsonify({"msg": "Feedback not found"}), 404
        
        # Get updated feedback
        feedback = mongo.db.feedback.find_one({"_id": ObjectId(feedback_id)})
        
        return jsonify({
            "msg": "Feedback liked",
            "likes": feedback.get("likes", 0)
        }), 200
    
    except Exception as e:
        return jsonify({"msg": f"Error liking feedback: {str(e)}"}), 500


@feedback_bp.route("/courses-taken", methods=["GET"])
@jwt_required()
def get_courses_taken():
    """Get courses that user has taken (can give feedback on)"""
    user_id = get_jwt_identity()
    
    try:
        # Get courses from academic data (courses user has completed)
        academic_data = mongo.db.academic_data.find_one({"user_id": user_id})
        
        if not academic_data or not academic_data.get("courses_taken"):
            return jsonify([]), 200
        
        courses_taken = academic_data.get("courses_taken", [])
        
        # Get feedback already submitted by user
        existing_feedback = list(mongo.db.feedback.find(
            {"user_id": user_id},
            {"course_code": 1}
        ))
        feedback_course_codes = {fb["course_code"] for fb in existing_feedback}
        
        # Filter out courses that already have feedback
        available_courses = [
            {
                "course_code": course["course_code"],
                "course_name": course["course_name"],
                "grade": course.get("grade"),
                "semester_taken": course.get("semester_taken")
            }
            for course in courses_taken
            if course["course_code"] not in feedback_course_codes
        ]
        
        return jsonify(available_courses), 200
    
    except Exception as e:
        return jsonify({"msg": f"Error fetching courses: {str(e)}"}), 500


@feedback_bp.route("/stats", methods=["GET"])
@jwt_required()
def get_feedback_stats():
    """Get overall feedback statistics"""
    try:
        total_feedback = mongo.db.feedback.count_documents({})
        
        if total_feedback == 0:
            return jsonify({
                "total_feedback": 0,
                "average_rating": 0,
                "rating_distribution": {}
            }), 200
        
        # Calculate statistics
        all_feedback = list(mongo.db.feedback.find({}, {"rating": 1}))
        ratings = [fb.get("rating", 0) for fb in all_feedback]
        
        avg_rating = sum(ratings) / len(ratings)
        
        # Rating distribution
        rating_dist = {i: ratings.count(i) for i in range(1, 6)}
        
        # Top rated courses
        pipeline = [
            {
                "$group": {
                    "_id": "$course_code",
                    "course_name": {"$first": "$course_name"},
                    "avg_rating": {"$avg": "$rating"},
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"avg_rating": -1}},
            {"$limit": 5}
        ]
        
        top_courses = list(mongo.db.feedback.aggregate(pipeline))
        
        return jsonify({
            "total_feedback": total_feedback,
            "average_rating": round(avg_rating, 2),
            "rating_distribution": rating_dist,
            "top_rated_courses": top_courses
        }), 200
    
    except Exception as e:
        return jsonify({"msg": f"Error fetching stats: {str(e)}"}), 500