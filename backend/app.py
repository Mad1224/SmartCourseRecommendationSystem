from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.config import Config
from database.mongo import mongo
from routes import register_routes
from routes.enrollment_routes import enrollment_bp
from routes.recommend_routes import recommend_routes
from routes.preferences_routes import preferences_bp
from routes.academic_routes import academic_bp
from routes.metrics_routes import metrics_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    JWTManager(app)
    CORS(app)

    register_routes(app)
    app.register_blueprint(enrollment_bp)
    app.register_blueprint(recommend_routes)
    app.register_blueprint(preferences_bp, url_prefix="/preferences")
    app.register_blueprint(academic_bp, url_prefix="/academic")
    app.register_blueprint(metrics_bp)



    @app.route("/")
    def home():
        return {"msg": "Backend running"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
