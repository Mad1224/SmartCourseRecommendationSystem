"""
Routes package initialization
Exports all blueprints for easy import
"""
from .auth_routes import auth_bp
from .course_routes import course_bp
from .enrollment_routes import enrollment_bp
from .feedback_routes import feedback_bp
from .preferences_routes import preferences_bp
from .recommend_routes import recommend_routes
from .academic_routes import academic_bp
from .metrics_routes import metrics_bp
from .advising_routes import advising_bp

__all__ = [
    'auth_bp',
    'course_bp',
    'enrollment_bp',
    'feedback_bp',
    'preferences_bp',
    'recommend_routes',
    'academic_bp',
    'metrics_bp',
    'advising_bp'
]

def register_routes(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(enrollment_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(preferences_bp, url_prefix="/preferences")
    app.register_blueprint(recommend_routes)
    app.register_blueprint(academic_bp, url_prefix="/academic")
    app.register_blueprint(metrics_bp)
    app.register_blueprint(advising_bp)
    