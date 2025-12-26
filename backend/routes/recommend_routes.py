from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

recommend_routes = Blueprint(
    "recommend_routes",
    __name__,
    url_prefix="/recommend"
)

@recommend_routes.route("/", methods=["POST"])
@jwt_required()
def recommend():
    return jsonify([
        {
            "course_code": "CSCI 4300",
            "course_name": "Machine Learning",
            "description": "Introduction to ML concepts",
            "score": 0.91
        },
        {
            "course_code": "CSCI 4302",
            "course_name": "Big Data Analytics",
            "description": "Big data frameworks",
            "score": 0.88
        },
        {
            "course_code": "CSCI 4301",
            "course_name": "Natural Language Processing",
            "description": "Text and language processing",
            "score": 0.85
        }
    ])
