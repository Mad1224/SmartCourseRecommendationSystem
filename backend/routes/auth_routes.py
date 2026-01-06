from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database.mongo import mongo
from bson import ObjectId
from datetime import datetime

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    Expected JSON:
    {
        "name": "Full Name",
        "email": "student@iium.edu.my",
        "matric_number": "2210000",
        "password": "password123",
        "kulliyyah": "KICT - Kulliyyah of ICT",
        "programme": "Computer Science",
        "year": 2,
        "phone": "01x-xxxxxxx" (optional)
    }
    """
    data = request.get_json()

    # Required fields validation
    required_fields = ["name", "email", "matric_number", "password", "kulliyyah", "programme", "year"]
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        return jsonify({"msg": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    email = data.get("email").lower().strip()
    password = data.get("password")
    name = data.get("name").strip()
    matric = data.get("matric_number").strip()
    kulliyyah = data.get("kulliyyah")
    programme = data.get("programme")
    year = data.get("year")
    phone = data.get("phone", "").strip()

    # Validation
    if len(password) < 6:
        return jsonify({"msg": "Password must be at least 6 characters"}), 400

    if "@" not in email:
        return jsonify({"msg": "Invalid email format"}), 400

    # Check if email already exists
    if mongo.db.users.find_one({"email": email}):
        return jsonify({"msg": "Email already registered"}), 409

    # Check if matric number already exists
    if mongo.db.users.find_one({"matric_number": matric}):
        return jsonify({"msg": "Matric number already registered"}), 409

    # Create user document
    user_doc = {
        "name": name,
        "email": email,
        "password": generate_password_hash(password),
        "matric_number": matric,
        "kulliyyah": kulliyyah,
        "programme": programme,
        "year": year,
        "phone": phone,
        "role": "student",
        "created_at": datetime.utcnow()
    }

    # Insert user
    result = mongo.db.users.insert_one(user_doc)
    user_id = str(result.inserted_id)

    # Generate token for auto-login
    token = create_access_token(identity=user_id)

    return jsonify({
        "msg": "Registration successful",
        "token": token,  # Return token for auto-login
        "user": {
            "id": user_id,
            "name": name,
            "email": email,
            "matric_number": matric
        }
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email", "").lower().strip()
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    user = mongo.db.users.find_one({"email": email})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"msg": "Invalid email or password"}), 401

    token = create_access_token(identity=str(user["_id"]))

    return jsonify({"token": token})


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    return jsonify({"logged_in_as": user_id})

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "email": user.get("email"),
        "name": user.get("name"),
        "matric_number": user.get("matric_number"),
        "kulliyyah": user.get("kulliyyah"),
        "programme": user.get("programme"),
        "year": user.get("year"),
        "phone": user.get("phone"),
        "role": user.get("role")
    }), 200