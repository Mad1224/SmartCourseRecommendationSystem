from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.mongo import mongo

feedback_bp = Blueprint("feedback", __name__, url_prefix="/feedback")

# ------------------ ADD FEEDBACK ------------------
@feedback_bp.post("")
@jwt_required()
def add_feedback():
    user_id = get_jwt_identity()
    data = request.json

    course_code = data.get("course_code")
    rating = data.get("rating")
    comment = data.get("comment", "")

    if not course_code or not rating:
        return jsonify({"msg": "Course code and rating required"}), 400

    mongo.db.feedback.insert_one({
        "user_id": user_id,
        "course_code": course_code,
        "rating": rating,
        "comment": comment
    })

    return jsonify({"msg": "Feedback submitted successfully"}), 201
