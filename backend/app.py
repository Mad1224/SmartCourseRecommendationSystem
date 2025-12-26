from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.config import Config
from database.mongo import mongo
from routes import register_routes
from routes.enrollment_routes import enrollment_bp
from routes.recommend_routes import recommend_routes
from routes.preferences_routes import preferences_bp



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



    @app.route("/")
    def home():
        return {"msg": "Backend running"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
