from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime

from database.mongo import mongo

enrollment_bp = Blueprint("enrollment", __name__, url_prefix="/enroll")


@enrollment_bp.post("")
@jwt_required()
def enroll_course():
    user_id = get_jwt_identity()
    data = request.json

    course_id = data.get("course_id")
    if not course_id:
        return jsonify({"msg": "course_id is required"}), 400

    # Check course exists
    course = mongo.db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        return jsonify({"msg": "Course not found"}), 404

    capacity = course.get("capacity", 0)
    course_credit_hours = course.get("credit_hours", 3)  # Default to 3 if not specified

    # Count current enrollments
    enrolled_count = mongo.db.enrollments.count_documents({
        "course_id": ObjectId(course_id),
        "status": "enrolled"
    })

    if enrolled_count >= capacity:
        return jsonify({
            "msg": "Course is full",
            "course_id": course_id
        }), 409

    # Prevent duplicate enrollment
    existing = mongo.db.enrollments.find_one({
        "course_id": ObjectId(course_id),
        "user_id": ObjectId(user_id),
        "status": "enrolled"
    })

    if existing:
        return jsonify({"msg": "Already enrolled"}), 400

    # Check credit hour limit (20 credit hours max)
    user_enrollments = mongo.db.enrollments.find({
        "user_id": ObjectId(user_id),
        "status": "enrolled"
    })
    
    total_credit_hours = 0
    for enrollment in user_enrollments:
        enrolled_course = mongo.db.courses.find_one({"_id": enrollment["course_id"]})
        if enrolled_course:
            total_credit_hours += enrolled_course.get("credit_hours", 3)
    
    if total_credit_hours + course_credit_hours > 20:
        return jsonify({
            "msg": "Credit hour limit reached",
            "current_credit_hours": total_credit_hours,
            "max_credit_hours": 20
        }), 400

    # Create enrollment
    mongo.db.enrollments.insert_one({
        "user_id": ObjectId(user_id),
        "course_id": ObjectId(course_id),
        "enrolled_at": datetime.utcnow(),
        "status": "enrolled"
    })

    return jsonify({
        "msg": "Enrollment successful",
        "course_id": course_id
    }), 201

from bson import ObjectId

@enrollment_bp.get("/my")
@jwt_required()
def my_enrollments():
    user_id = get_jwt_identity()

    enrollments = mongo.db.enrollments.find({
        "user_id": ObjectId(user_id),
        "status": "enrolled"
    })

    results = []
    for e in enrollments:
        course = mongo.db.courses.find_one({"_id": e["course_id"]})
        if course:
            results.append({
                "course_id": str(course["_id"]),
                "course_code": course.get("course_code"),
                "course_name": course.get("course_name"),
                "level": course.get("level"),
                "enrolled_at": e.get("enrolled_at")
            })
    
    print(f"Enrolled courses for user {user_id}: {len(results)} courses")
    return jsonify(results), 200

@enrollment_bp.delete("/<course_id>")
@jwt_required()
def remove_enrollment(course_id):
    user_id = get_jwt_identity()
    
    result = mongo.db.enrollments.delete_one({
        "user_id": ObjectId(user_id),
        "course_id": ObjectId(course_id),
        "status": "enrolled"
    })
    
    if result.deleted_count > 0:
        return jsonify({"msg": "Enrollment removed"}), 200
    else:
        return jsonify({"msg": "Enrollment not found"}), 404