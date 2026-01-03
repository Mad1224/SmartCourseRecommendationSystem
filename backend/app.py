from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.config import Config
from database.mongo import mongo

from routes import register_routes
from routes.auth_routes import auth_bp
from routes.course_routes import course_bp
from routes.enrollment_routes import enrollment_bp
from routes.feedback_routes import feedback_bp
from routes.preferences_routes import preferences_bp
from routes.recommend_routes import recommend_routes
from routes.academic_routes import academic_bp
from routes.metrics_routes import metrics_bp
from routes.advising_routes import advising_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    jwt = JWTManager(app)
    CORS(app)

    register_routes(app)
#    app.register_blueprint(enrollment_bp)
#    app.register_blueprint(recommend_routes)
#    app.register_blueprint(preferences_bp, url_prefix="/preferences")
#    app.register_blueprint(academic_bp, url_prefix="/academic")
#    app.register_blueprint(metrics_bp)
#    app.register_blueprint(auth_bp)
#    app.register_blueprint(course_bp)
#    app.register_blueprint(feedback_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"msg": "Endpoint not found"}), 404
    
    @app.errorhandler(500) 
    def internal_error(error):
        return jsonify({"msg": "Internal server error"}), 500
    
    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"msg": "Token has expired"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"msg": "Invalid token"}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"msg": "Authorization token missing"}), 401
    
    @app.route("/")
    def home():
        return jsonify({
            "msg": "SCRS Backend API",
            "version": "1.0",
            "status": "running"
        })
    
    @app.route("/health")
    def health_check():
        return jsonify({
            "status": "healthy",
            "database": "connected" if mongo.db else "disconnected"
        })
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
