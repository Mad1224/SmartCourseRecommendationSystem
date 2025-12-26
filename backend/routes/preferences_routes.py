from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.mongo import mongo
from datetime import datetime

preferences_bp = Blueprint("preferences", __name__)

@preferences_bp.route("/", methods=["POST"])
@jwt_required()
def save_preferences():
    user_id = get_jwt_identity()
    data = request.json

    doc = {
        "user_id": user_id,
        "kulliyyah": data.get("kulliyyah"),
        "semester": data.get("semester"),
        "cgpa": data.get("cgpa"),
        "preferredTypes": data.get("preferredTypes", []),
        "preferredTime": data.get("preferredTime"),
        "coursesToAvoid": data.get("coursesToAvoid", []),
        "created_at": datetime.utcnow()
    }

    mongo.db.preferences.insert_one(doc)

    return jsonify({"msg": "Preferences saved"}), 201
