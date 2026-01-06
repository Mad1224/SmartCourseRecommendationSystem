from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.mongo import mongo
from bson import ObjectId
from datetime import datetime

advising_bp = Blueprint("advising", __name__, url_prefix="/advising")

@advising_bp.route("/request", methods=["POST"])
@jwt_required()
def submit_advising_request():
    """
    Submit an academic advising request
    Expected JSON:
    {
        "advising_type": "Course Selection",
        "preferred_lecturer_id": "lecturer_id_here" (optional),
        "additional_note": "Details about the request"
    }
    """
    user_id = get_jwt_identity()
    data = request.json

    # Validation
    if not data.get("advising_type") or not data.get("additional_note"):
        return jsonify({"msg": "Advising type and additional note are required"}), 400

    if len(data.get("additional_note", "").strip()) < 10:
        return jsonify({"msg": "Additional note must be at least 10 characters"}), 400

    # Get user details
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Get preferred lecturer details (if specified)
    assigned_lecturer = None
    if data.get("preferred_lecturer_id"):
        lecturer = mongo.db.users.find_one({
            "_id": ObjectId(data.get("preferred_lecturer_id")),
            "role": {"$in": ["lecturer", "admin", "staff"]}
        })
        if lecturer:
            assigned_lecturer = {
                "id": str(lecturer["_id"]),
                "name": lecturer.get("name", ""),
                "email": lecturer.get("email", "")
            }

    # Create advising request document
    request_doc = {
        "student_id": user_id,
        "student_name": user.get("name", ""),
        "student_email": user.get("email", ""),
        "student_matric": user.get("matric_number", ""),
        "advising_type": data.get("advising_type"),
        "preferred_lecturer_id": data.get("preferred_lecturer_id"),
        "assigned_lecturer": assigned_lecturer,
        "additional_note": data.get("additional_note").strip(),
        "status": "pending",  # pending, assigned, in_progress, completed, cancelled
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "response": None,
        "response_date": None
    }

    result = mongo.db.advising_requests.insert_one(request_doc)

    return jsonify({
        "msg": "Advising request submitted successfully",
        "request_id": str(result.inserted_id),
        "status": "pending"
    }), 201


@advising_bp.route("/lecturers", methods=["GET"])
@jwt_required()
def get_available_lecturers():
    """Get list of available lecturers/advisers"""
    try:
        # Get users with role lecturer, staff, or admin
        lecturers = list(mongo.db.users.find(
            {"role": {"$in": ["lecturer", "admin", "staff"]}},
            {"name": 1, "email": 1, "specialization": 1}
        ))

        result = []
        for lecturer in lecturers:
            result.append({
                "id": str(lecturer["_id"]),
                "name": lecturer.get("name", ""),
                "email": lecturer.get("email", ""),
                "specialization": lecturer.get("specialization", "General Advising")
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"msg": f"Error fetching lecturers: {str(e)}"}), 500


@advising_bp.route("/my-requests", methods=["GET"])
@jwt_required()
def get_my_requests():
    """Get all advising requests for the current user"""
    user_id = get_jwt_identity()

    try:
        requests_list = list(mongo.db.advising_requests.find(
            {"student_id": user_id}
        ).sort("created_at", -1))

        result = []
        for req in requests_list:
            result.append({
                "id": str(req["_id"]),
                "advising_type": req.get("advising_type"),
                "additional_note": req.get("additional_note"),
                "status": req.get("status"),
                "assigned_lecturer": req.get("assigned_lecturer"),
                "response": req.get("response"),
                "created_at": req.get("created_at").isoformat() if req.get("created_at") else None,
                "updated_at": req.get("updated_at").isoformat() if req.get("updated_at") else None,
                "response_date": req.get("response_date").isoformat() if req.get("response_date") else None
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"msg": f"Error fetching requests: {str(e)}"}), 500


@advising_bp.route("/request/<request_id>", methods=["GET"])
@jwt_required()
def get_request_details(request_id):
    """Get details of a specific advising request"""
    user_id = get_jwt_identity()

    try:
        request_doc = mongo.db.advising_requests.find_one({"_id": ObjectId(request_id)})

        if not request_doc:
            return jsonify({"msg": "Request not found"}), 404

        # Check if user is the owner or an admin
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        is_admin = user.get("role") in ["admin", "staff", "lecturer"]
        is_owner = request_doc.get("student_id") == user_id

        if not (is_owner or is_admin):
            return jsonify({"msg": "Unauthorized"}), 403

        result = {
            "id": str(request_doc["_id"]),
            "student_name": request_doc.get("student_name"),
            "student_email": request_doc.get("student_email"),
            "student_matric": request_doc.get("student_matric"),
            "advising_type": request_doc.get("advising_type"),
            "additional_note": request_doc.get("additional_note"),
            "status": request_doc.get("status"),
            "assigned_lecturer": request_doc.get("assigned_lecturer"),
            "response": request_doc.get("response"),
            "created_at": request_doc.get("created_at").isoformat() if request_doc.get("created_at") else None,
            "updated_at": request_doc.get("updated_at").isoformat() if request_doc.get("updated_at") else None,
            "response_date": request_doc.get("response_date").isoformat() if request_doc.get("response_date") else None
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"msg": f"Error fetching request: {str(e)}"}), 500


@advising_bp.route("/request/<request_id>", methods=["DELETE"])
@jwt_required()
def cancel_request(request_id):
    """Cancel an advising request (only if pending)"""
    user_id = get_jwt_identity()

    try:
        request_doc = mongo.db.advising_requests.find_one({"_id": ObjectId(request_id)})

        if not request_doc:
            return jsonify({"msg": "Request not found"}), 404

        # Check ownership
        if request_doc.get("student_id") != user_id:
            return jsonify({"msg": "Unauthorized"}), 403

        # Can only cancel if pending
        if request_doc.get("status") != "pending":
            return jsonify({"msg": "Can only cancel pending requests"}), 400

        # Update status to cancelled
        mongo.db.advising_requests.update_one(
            {"_id": ObjectId(request_id)},
            {
                "$set": {
                    "status": "cancelled",
                    "updated_at": datetime.utcnow()
                }
            }
        )

        return jsonify({"msg": "Request cancelled successfully"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error cancelling request: {str(e)}"}), 500


@advising_bp.route("/admin/requests", methods=["GET"])
@jwt_required()
def get_all_requests():
    """Get all advising requests (Admin/Staff only)"""
    user_id = get_jwt_identity()

    # Check if user is admin/staff
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user or user.get("role") not in ["admin", "staff", "lecturer"]:
        return jsonify({"msg": "Admin/Staff access required"}), 403

    try:
        # Get filter parameters
        status = request.args.get('status')  # pending, assigned, in_progress, completed, cancelled
        
        query = {}
        if status:
            query["status"] = status

        requests_list = list(mongo.db.advising_requests.find(query).sort("created_at", -1))

        result = []
        for req in requests_list:
            result.append({
                "id": str(req["_id"]),
                "student_name": req.get("student_name"),
                "student_matric": req.get("student_matric"),
                "advising_type": req.get("advising_type"),
                "status": req.get("status"),
                "assigned_lecturer": req.get("assigned_lecturer"),
                "created_at": req.get("created_at").isoformat() if req.get("created_at") else None,
                "updated_at": req.get("updated_at").isoformat() if req.get("updated_at") else None
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"msg": f"Error fetching requests: {str(e)}"}), 500


@advising_bp.route("/admin/request/<request_id>/status", methods=["PUT"])
@jwt_required()
def update_request_status(request_id):
    """
    Update advising request status (Admin/Staff only)
    Expected JSON:
    {
        "status": "assigned",
        "assigned_lecturer_id": "lecturer_id",
        "response": "Response message"
    }
    """
    user_id = get_jwt_identity()

    # Check if user is admin/staff
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user or user.get("role") not in ["admin", "staff", "lecturer"]:
        return jsonify({"msg": "Admin/Staff access required"}), 403

    data = request.json

    try:
        request_doc = mongo.db.advising_requests.find_one({"_id": ObjectId(request_id)})

        if not request_doc:
            return jsonify({"msg": "Request not found"}), 404

        update_data = {
            "updated_at": datetime.utcnow()
        }

        # Update status
        if "status" in data:
            valid_statuses = ["pending", "assigned", "in_progress", "completed", "cancelled"]
            if data["status"] not in valid_statuses:
                return jsonify({"msg": "Invalid status"}), 400
            update_data["status"] = data["status"]

        # Assign lecturer
        if "assigned_lecturer_id" in data:
            lecturer = mongo.db.users.find_one({
                "_id": ObjectId(data["assigned_lecturer_id"]),
                "role": {"$in": ["lecturer", "admin", "staff"]}
            })
            if lecturer:
                update_data["assigned_lecturer"] = {
                    "id": str(lecturer["_id"]),
                    "name": lecturer.get("name", ""),
                    "email": lecturer.get("email", "")
                }

        # Add response
        if "response" in data:
            update_data["response"] = data["response"]
            update_data["response_date"] = datetime.utcnow()

        # Update in database
        mongo.db.advising_requests.update_one(
            {"_id": ObjectId(request_id)},
            {"$set": update_data}
        )

        return jsonify({"msg": "Request updated successfully"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error updating request: {str(e)}"}), 500


@advising_bp.route("/stats", methods=["GET"])
@jwt_required()
def get_advising_stats():
    """Get advising request statistics"""
    user_id = get_jwt_identity()

    # Check if user is admin/staff
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user or user.get("role") not in ["admin", "staff", "lecturer"]:
        return jsonify({"msg": "Admin/Staff access required"}), 403

    try:
        total_requests = mongo.db.advising_requests.count_documents({})
        pending_requests = mongo.db.advising_requests.count_documents({"status": "pending"})
        assigned_requests = mongo.db.advising_requests.count_documents({"status": "assigned"})
        in_progress_requests = mongo.db.advising_requests.count_documents({"status": "in_progress"})
        completed_requests = mongo.db.advising_requests.count_documents({"status": "completed"})

        # Count by advising type
        pipeline = [
            {
                "$group": {
                    "_id": "$advising_type",
                    "count": {"$sum": 1}
                }
            }
        ]
        advising_types = list(mongo.db.advising_requests.aggregate(pipeline))

        return jsonify({
            "total_requests": total_requests,
            "by_status": {
                "pending": pending_requests,
                "assigned": assigned_requests,
                "in_progress": in_progress_requests,
                "completed": completed_requests
            },
            "by_type": advising_types
        }), 200

    except Exception as e:
        return jsonify({"msg": f"Error fetching statistics: {str(e)}"}), 500
    
    