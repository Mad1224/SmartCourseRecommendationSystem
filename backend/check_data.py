from database.mongo import mongo
from config.config import Config
from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)

with app.app_context():
    courses_count = mongo.db.courses.count_documents({})
    users_count = mongo.db.users.count_documents({})
    feedback_count = mongo.db.feedback.count_documents({})
    
    print(f"Courses: {courses_count}")
    print(f"Users: {users_count}")
    print(f"Feedback: {feedback_count}")
    
    if courses_count > 0:
        print("\nSample course:")
        course = mongo.db.courses.find_one()
        print(f"  Code: {course.get('course_code')}")
        print(f"  Name: {course.get('course_name')}")
