from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.mongo import mongo
from bson import ObjectId
from datetime import datetime

academic_bp = Blueprint("academic", __name__, url_prefix="/academic")

# ---------- SAVE/UPDATE ACADEMIC DATA ----------
@academic_bp.route("/", methods=["POST"])
@jwt_required()
def save_academic_data():
    """
    Save or update academic data for a user
    Expected JSON:
    {
        "kulliyyah": "KICT",
        "programme": "Computer Science",
        "current_semester": 4,
        "cgpa": 3.75,
        "courses_taken": [
            {
                "course_code": "INFO 4201",
                "course_name": "Database Systems",
                "semester_taken": 3,
                "grade": "A",
                "credit_hours": 3
            }
        ]
    }
    """
    user_id = get_jwt_identity()
    data = request.json

    # Check if academic data already exists
    existing = mongo.db.academic_data.find_one({"user_id": user_id})

    academic_doc = {
        "user_id": user_id,
        "kulliyyah": data.get("kulliyyah"),
        "programme": data.get("programme"),
        "current_semester": data.get("current_semester"),
        "cgpa": data.get("cgpa"),
        "courses_taken": data.get("courses_taken", []),
        "updated_at": datetime.utcnow()
    }

    if existing:
        # Update existing document
        mongo.db.academic_data.update_one(
            {"user_id": user_id},
            {"$set": academic_doc}
        )
        return jsonify({"msg": "Academic data updated successfully"}), 200
    else:
        # Create new document
        academic_doc["created_at"] = datetime.utcnow()
        mongo.db.academic_data.insert_one(academic_doc)
        return jsonify({"msg": "Academic data saved successfully"}), 201


# ---------- GET ACADEMIC DATA ----------
@academic_bp.route("/", methods=["GET"])
@jwt_required()
def get_academic_data():
    """Get academic data for the current user"""
    user_id = get_jwt_identity()

    academic_data = mongo.db.academic_data.find_one({"user_id": user_id})

    if not academic_data:
        return jsonify({"msg": "No academic data found"}), 404

    # Remove MongoDB _id field
    academic_data.pop("_id", None)

    return jsonify(academic_data), 200


# ---------- ADD COURSE TO TRANSCRIPT ----------
@academic_bp.route("/course", methods=["POST"])
@jwt_required()
def add_course():
    """
    Add a single course to the user's transcript
    Expected JSON:
    {
        "course_code": "INFO 4201",
        "course_name": "Database Systems",
        "semester_taken": 3,
        "grade": "A",
        "credit_hours": 3
    }
    """
    user_id = get_jwt_identity()
    course_data = request.json

    # Validate required fields
    required_fields = ["course_code", "course_name", "semester_taken", "grade", "credit_hours"]
    if not all(field in course_data for field in required_fields):
        return jsonify({"msg": "Missing required fields"}), 400

    # Add timestamp
    course_data["added_at"] = datetime.utcnow()

    # Update or create academic data
    result = mongo.db.academic_data.update_one(
        {"user_id": user_id},
        {
            "$push": {"courses_taken": course_data},
            "$set": {"updated_at": datetime.utcnow()}
        },
        upsert=True
    )

    return jsonify({"msg": "Course added successfully"}), 201


# ---------- UPDATE COURSE IN TRANSCRIPT ----------
@academic_bp.route("/course/<course_code>", methods=["PUT"])
@jwt_required()
def update_course(course_code):
    """
    Update a specific course in the transcript
    Expected JSON:
    {
        "course_name": "Updated Course Name",
        "semester_taken": 3,
        "grade": "A-",
        "credit_hours": 3
    }
    """
    user_id = get_jwt_identity()
    update_data = request.json

    # Find the user's academic data
    academic_data = mongo.db.academic_data.find_one({"user_id": user_id})

    if not academic_data:
        return jsonify({"msg": "No academic data found"}), 404

    # Find and update the course
    courses_taken = academic_data.get("courses_taken", [])
    course_found = False

    for i, course in enumerate(courses_taken):
        if course.get("course_code") == course_code:
            # Update the course
            courses_taken[i].update(update_data)
            course_found = True
            break

    if not course_found:
        return jsonify({"msg": "Course not found"}), 404

    # Update the database
    mongo.db.academic_data.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "courses_taken": courses_taken,
                "updated_at": datetime.utcnow()
            }
        }
    )

    return jsonify({"msg": "Course updated successfully"}), 200


# ---------- DELETE COURSE FROM TRANSCRIPT ----------
@academic_bp.route("/course/<course_code>", methods=["DELETE"])
@jwt_required()
def delete_course(course_code):
    """Delete a specific course from the transcript"""
    user_id = get_jwt_identity()

    result = mongo.db.academic_data.update_one(
        {"user_id": user_id},
        {
            "$pull": {"courses_taken": {"course_code": course_code}},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )

    if result.modified_count == 0:
        return jsonify({"msg": "Course not found"}), 404

    return jsonify({"msg": "Course deleted successfully"}), 200


# ---------- GET COURSES BY SEMESTER ----------
@academic_bp.route("/semester/<int:semester>", methods=["GET"])
@jwt_required()
def get_courses_by_semester(semester):
    """Get all courses taken in a specific semester"""
    user_id = get_jwt_identity()

    academic_data = mongo.db.academic_data.find_one({"user_id": user_id})

    if not academic_data:
        return jsonify({"msg": "No academic data found"}), 404

    # Filter courses by semester
    courses = [
        course for course in academic_data.get("courses_taken", [])
        if course.get("semester_taken") == semester
    ]

    return jsonify({"semester": semester, "courses": courses}), 200


# ---------- UPDATE CGPA ----------
@academic_bp.route("/cgpa", methods=["PUT"])
@jwt_required()
def update_cgpa():
    """
    Update the user's CGPA
    Expected JSON:
    {
        "cgpa": 3.75,
        "current_semester": 4
    }
    """
    user_id = get_jwt_identity()
    data = request.json

    if "cgpa" not in data:
        return jsonify({"msg": "CGPA is required"}), 400

    update_fields = {
        "cgpa": data["cgpa"],
        "updated_at": datetime.utcnow()
    }

    if "current_semester" in data:
        update_fields["current_semester"] = data["current_semester"]

    result = mongo.db.academic_data.update_one(
        {"user_id": user_id},
        {"$set": update_fields},
        upsert=True
    )

    return jsonify({"msg": "CGPA updated successfully"}), 200


# ---------- GET ACADEMIC STATISTICS ----------
@academic_bp.route("/statistics", methods=["GET"])
@jwt_required()
def get_statistics():
    """Get academic statistics for the user"""
    user_id = get_jwt_identity()

    academic_data = mongo.db.academic_data.find_one({"user_id": user_id})

    if not academic_data:
        return jsonify({"msg": "No academic data found"}), 404

    courses_taken = academic_data.get("courses_taken", [])

    # Calculate statistics
    total_courses = len(courses_taken)
    total_credit_hours = sum(course.get("credit_hours", 0) for course in courses_taken)

    # Count grades
    grade_distribution = {}
    for course in courses_taken:
        grade = course.get("grade", "N/A")
        grade_distribution[grade] = grade_distribution.get(grade, 0) + 1

    statistics = {
        "cgpa": academic_data.get("cgpa"),
        "current_semester": academic_data.get("current_semester"),
        "total_courses_completed": total_courses,
        "total_credit_hours": total_credit_hours,
        "grade_distribution": grade_distribution,
        "kulliyyah": academic_data.get("kulliyyah"),
        "programme": academic_data.get("programme")
    }

    return jsonify(statistics), 200
