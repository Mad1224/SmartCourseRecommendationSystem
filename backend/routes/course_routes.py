from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.mongo import mongo
from bson import ObjectId
from datetime import datetime

course_bp = Blueprint("courses", __name__, url_prefix="/courses")

# ------------------ GET ALL COURSES ------------------
@course_bp.route("/", methods=["GET"])
@jwt_required()
def get_courses():
    """
    Get all courses with availability status
    Returns courses sorted by: available first, then by level, then by code
    """
    try:
        courses = list(mongo.db.courses.find())
        result = []

        for course in courses:
            result.append({
                "id": str(course["_id"]),
                "_id": str(course["_id"]),
                "course_code": course.get("course_code"),
                "course_name": course.get("course_name"),
                "description": course.get("description", ""),
                "level": course.get("level", 1),
                "capacity": course.get("capacity", 30),
                "credit_hours": course.get("credit_hours", 3),
                "skills": course.get("skills", []),
                "prerequisites": course.get("prerequisites", []),
                "is_available_this_semester": course.get("is_available_this_semester", False),
                "semester": course.get("semester", ""),
                "instructor": course.get("instructor", ""),
                "department": course.get("department", "")
            })
        
        # Sort: available first, then by level, then by code
        result.sort(key=lambda x: (
            not x["is_available_this_semester"],  # Available first (False < True)
            x["level"],
            x["course_code"]
        ))

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"msg": f"Error fetching courses: {str(e)}"}), 500


# ------------------ GET AVAILABLE COURSES ONLY ------------------
@course_bp.route("/available", methods=["GET"])
@jwt_required()
def get_available_courses():
    """Get only courses available this semester"""
    try:
        courses = list(mongo.db.courses.find({"is_available_this_semester": True}))
        result = []

        for course in courses:
            result.append({
                "id": str(course["_id"]),
                "_id": str(course["_id"]),
                "course_code": course.get("course_code"),
                "course_name": course.get("course_name"),
                "description": course.get("description", ""),
                "level": course.get("level", 1),
                "capacity": course.get("capacity", 30),
                "credit_hours": course.get("credit_hours", 3),
                "skills": course.get("skills", []),
                "prerequisites": course.get("prerequisites", []),
                "is_available_this_semester": True,
                "semester": course.get("semester", ""),
                "instructor": course.get("instructor", "")
            })

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"msg": f"Error fetching available courses: {str(e)}"}), 500


# ------------------ GET COURSE BY ID ------------------
@course_bp.route("/<course_id>", methods=["GET"])
@jwt_required()
def get_course(course_id):
    """Get detailed information about a specific course"""
    try:
        course = mongo.db.courses.find_one({"_id": ObjectId(course_id)})

        if not course:
            return jsonify({"msg": "Course not found"}), 404

        return jsonify({
            "id": str(course["_id"]),
            "_id": str(course["_id"]),
            "course_code": course.get("course_code"),
            "course_name": course.get("course_name"),
            "description": course.get("description", ""),
            "level": course.get("level", 1),
            "capacity": course.get("capacity", 30),
            "credit_hours": course.get("credit_hours", 3),
            "skills": course.get("skills", []),
            "prerequisites": course.get("prerequisites", []),
            "is_available_this_semester": course.get("is_available_this_semester", False),
            "semester": course.get("semester", ""),
            "instructor": course.get("instructor", ""),
            "department": course.get("department", "")
        }), 200
    
    except Exception as e:
        return jsonify({"msg": f"Error fetching course: {str(e)}"}), 500


# ------------------ GET COURSES BY LEVEL ------------------
@course_bp.route("/level/<int:level>", methods=["GET"])
@jwt_required()
def get_courses_by_level(level):
    """Get all courses for a specific level"""
    try:
        courses = list(mongo.db.courses.find({"level": level}))
        result = []

        for course in courses:
            result.append({
                "id": str(course["_id"]),
                "_id": str(course["_id"]),
                "course_code": course.get("course_code"),
                "course_name": course.get("course_name"),
                "description": course.get("description", ""),
                "level": course.get("level", 1),
                "capacity": course.get("capacity", 30),
                "credit_hours": course.get("credit_hours", 3),
                "skills": course.get("skills", []),
                "prerequisites": course.get("prerequisites", []),
                "is_available_this_semester": course.get("is_available_this_semester", False),
                "semester": course.get("semester", "")
            })

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"msg": f"Error fetching courses: {str(e)}"}), 500


# ------------------ SEARCH COURSES ------------------
@course_bp.route("/search", methods=["GET"])
@jwt_required()
def search_courses():
    """
    Search courses by query string
    Searches in: course code, course name, description, skills
    """
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify([]), 200
    
    try:
        # Create search filter
        search_filter = {
            "$or": [
                {"course_code": {"$regex": query, "$options": "i"}},
                {"course_name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"skills": {"$regex": query, "$options": "i"}}
            ]
        }
        
        courses = list(mongo.db.courses.find(search_filter))
        result = []

        for course in courses:
            result.append({
                "id": str(course["_id"]),
                "_id": str(course["_id"]),
                "course_code": course.get("course_code"),
                "course_name": course.get("course_name"),
                "description": course.get("description", ""),
                "level": course.get("level", 1),
                "capacity": course.get("capacity", 30),
                "credit_hours": course.get("credit_hours", 3),
                "skills": course.get("skills", []),
                "prerequisites": course.get("prerequisites", []),
                "is_available_this_semester": course.get("is_available_this_semester", False),
                "semester": course.get("semester", "")
            })

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"msg": f"Error searching courses: {str(e)}"}), 500


# ------------------ ADMIN: ADD COURSE ------------------
@course_bp.route("/", methods=["POST"])
@jwt_required()
def add_course():
    """
    Add a new course (Admin only)
    Expected JSON:
    {
        "course_code": "CSCI4501",
        "course_name": "Course Name",
        "description": "Course description",
        "level": 4,
        "capacity": 30,
        "credit_hours": 3,
        "skills": ["Skill1", "Skill2"],
        "prerequisites": ["CSCI3301"],
        "is_available_this_semester": true,
        "semester": "2024/2025 Sem 1",
        "instructor": "Dr. John Doe"
    }
    """
    user_id = get_jwt_identity()
    
    # Check if user is admin
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user or user.get("role") != "admin":
        return jsonify({"msg": "Admin access required"}), 403
    
    data = request.json

    # Validation
    required_fields = ["course_code", "course_name", "description", "level"]
    if not all(field in data for field in required_fields):
        return jsonify({"msg": "Missing required fields"}), 400
    
    # Check if course code already exists
    existing = mongo.db.courses.find_one({"course_code": data["course_code"]})
    if existing:
        return jsonify({"msg": "Course code already exists"}), 409

    # Create course document
    course_doc = {
        "course_code": data["course_code"],
        "course_name": data["course_name"],
        "description": data["description"],
        "level": data["level"],
        "capacity": data.get("capacity", 30),
        "credit_hours": data.get("credit_hours", 3),
        "skills": data.get("skills", []),
        "prerequisites": data.get("prerequisites", []),
        "is_available_this_semester": data.get("is_available_this_semester", False),
        "semester": data.get("semester", ""),
        "instructor": data.get("instructor", ""),
        "department": data.get("department", ""),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = mongo.db.courses.insert_one(course_doc)

    return jsonify({
        "msg": "Course added successfully",
        "course_id": str(result.inserted_id)
    }), 201


# ------------------ ADMIN: UPDATE COURSE ------------------
@course_bp.route("/<course_id>", methods=["PUT"])
@jwt_required()
def update_course(course_id):
    """Update course information (Admin only)"""
    user_id = get_jwt_identity()
    
    # Check if user is admin
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user or user.get("role") != "admin":
        return jsonify({"msg": "Admin access required"}), 403
    
    data = request.json
    
    # Find course
    course = mongo.db.courses.find_one({"_id": ObjectId(course_id)})
    if not course:
        return jsonify({"msg": "Course not found"}), 404
    
    # Update fields
    update_data = {}
    allowed_fields = [
        "course_name", "description", "level", "capacity", "credit_hours",
        "skills", "prerequisites", "is_available_this_semester", "semester",
        "instructor", "department"
    ]
    
    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field]
    
    update_data["updated_at"] = datetime.utcnow()
    
    mongo.db.courses.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": update_data}
    )
    
    return jsonify({"msg": "Course updated successfully"}), 200


# ------------------ ADMIN: DELETE COURSE ------------------
@course_bp.route("/<course_id>", methods=["DELETE"])
@jwt_required()
def delete_course(course_id):
    """Delete a course (Admin only)"""
    user_id = get_jwt_identity()
    
    # Check if user is admin
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user or user.get("role") != "admin":
        return jsonify({"msg": "Admin access required"}), 403
    
    result = mongo.db.courses.delete_one({"_id": ObjectId(course_id)})
    
    if result.deleted_count == 0:
        return jsonify({"msg": "Course not found"}), 404
    
    return jsonify({"msg": "Course deleted successfully"}), 200


# ------------------ ADMIN: SET COURSE AVAILABILITY ------------------
@course_bp.route("/<course_id>/availability", methods=["PUT"])
@jwt_required()
def set_course_availability(course_id):
    """
    Set course availability for current semester (Admin only)
    Expected JSON:
    {
        "is_available": true,
        "semester": "2024/2025 Sem 1"
    }
    """
    user_id = get_jwt_identity()
    
    # Check if user is admin
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user or user.get("role") != "admin":
        return jsonify({"msg": "Admin access required"}), 403
    
    data = request.json
    
    if "is_available" not in data:
        return jsonify({"msg": "is_available field required"}), 400
    
    update_data = {
        "is_available_this_semester": data["is_available"],
        "updated_at": datetime.utcnow()
    }
    
    if "semester" in data:
        update_data["semester"] = data["semester"]
    
    result = mongo.db.courses.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        return jsonify({"msg": "Course not found"}), 404
    
    return jsonify({"msg": "Course availability updated"}), 200


# ------------------ GET COURSE STATISTICS ------------------
@course_bp.route("/stats", methods=["GET"])
@jwt_required()
def get_course_stats():
    """Get overall course statistics"""
    try:
        total_courses = mongo.db.courses.count_documents({})
        available_courses = mongo.db.courses.count_documents({"is_available_this_semester": True})
        
        # Count by level
        courses_by_level = {}
        for level in range(1, 5):
            count = mongo.db.courses.count_documents({"level": level})
            courses_by_level[f"level_{level}"] = count
        
        return jsonify({
            "total_courses": total_courses,
            "available_this_semester": available_courses,
            "not_available": total_courses - available_courses,
            "by_level": courses_by_level
        }), 200
    
    except Exception as e:
        return jsonify({"msg": f"Error fetching statistics: {str(e)}"}), 500