from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database.mongo import mongo

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ---------- REGISTER ----------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    name = data.get("name", "")
    matric = data.get("matric_number", "")

    if not email or not password:
        return jsonify({"msg": "Email and password required"}), 400

    if mongo.db.users.find_one({"email": email}):
        return jsonify({"msg": "Email already exists"}), 409

    mongo.db.users.insert_one({
        "email": email,
        "password": generate_password_hash(password),
        "name": name,
        "matric_number": matric,
        "role": "student"
    })

    return jsonify({"msg": "User registered"}), 201



# ---------- LOGIN ----------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = mongo.db.users.find_one({"email": email})

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user["_id"]))

    return jsonify({"token": token})


# ---------- PROTECTED ----------
@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    return jsonify({"logged_in_as": user_id})

# ---------- GET CURRENT USER ----------
from bson import ObjectId

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
        "role": user.get("role")
    }), 200
