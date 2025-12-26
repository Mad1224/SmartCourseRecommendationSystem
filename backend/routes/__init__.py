from .auth_routes import auth_bp
from .course_routes import course_bp

from .feedback_routes import feedback_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)

    app.register_blueprint(feedback_bp)
