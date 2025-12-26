from flask import Blueprint, request, jsonify
from database.mongo import mongo
from bson.objectid import ObjectId

course_bp = Blueprint("courses", __name__, url_prefix="/courses")

# ------------------ ADD COURSE ------------------
@course_bp.post("")
def add_course():
    data = request.json

    course_code = data.get("course_code")
    course_name = data.get("course_name")
    level = data.get("level")
    skills = data.get("skills")

    if not all([course_code, course_name, level, skills]):
        return jsonify({"msg": "All fields are required"}), 400

    mongo.db.courses.insert_one({
        "course_code": course_code,
        "course_name": course_name,
        "level": level,
        "skills": skills
    })

    return jsonify({"msg": "Course added successfully"}), 201


# ------------------ GET ALL COURSES ------------------
@course_bp.get("")
def get_courses():
    courses = mongo.db.courses.find()
    result = []

    for course in courses:
        result.append({
            "id": str(course["_id"]),
            "course_code": course["course_code"],
            "course_name": course["course_name"],
            "level": course["level"],
            "skills": course["skills"]
        })

    return jsonify(result), 200


# ------------------ GET COURSE BY ID ------------------
@course_bp.get("/<course_id>")
def get_course(course_id):
    course = mongo.db.courses.find_one({"_id": ObjectId(course_id)})

    if not course:
        return jsonify({"msg": "Course not found"}), 404

    return jsonify({
        "id": str(course["_id"]),
        "course_code": course["course_code"],
        "course_name": course["course_name"],
        "level": course["level"],
        "skills": course["skills"]
    }), 200
