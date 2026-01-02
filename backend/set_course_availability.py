"""
Script to set course availability for current semester
Run this to mark which courses are offered this semester
"""
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['fyp2']

print("📅 Setting Course Availability for Current Semester\n")
print("=" * 60)

# Define current semester
CURRENT_SEMESTER = "2024/2025 Semester 2"

# Mark Level 1 and Level 2 courses as available (for new students)
# Mark some Level 3 and Level 4 courses as available

available_course_codes = [
    # Level 1 - All available for new students
    "CSCI1100", "CSCI1201",
    
    # Level 2 - Most available
    "CSCI2101", "CSCI2201", "CSCI2301", "INFO2101", "MATH2101",
    
    # Level 3 - Some available
    "CSCI3101", "CSCI3201", "CSCI3301", "CSCI3401", "INFO3101", "INFO3201", "STAT3101",
    
    # Level 4 - Selected advanced courses
    "CSCI4101", "CSCI4201", "CSCI4301", "CSCI4401", "CSCI4501",
]

# First, set all courses as NOT available
result = db.courses.update_many(
    {},
    {
        "$set": {
            "is_available_this_semester": False,
            "semester": "",
            "updated_at": datetime.utcnow()
        }
    }
)
print(f"✓ Reset all courses to unavailable: {result.modified_count} courses")

# Then, mark selected courses as available
result = db.courses.update_many(
    {"course_code": {"$in": available_course_codes}},
    {
        "$set": {
            "is_available_this_semester": True,
            "semester": CURRENT_SEMESTER,
            "updated_at": datetime.utcnow()
        }
    }
)

print(f"✓ Marked {result.modified_count} courses as available")
print(f"  Semester: {CURRENT_SEMESTER}\n")

# Show summary by level
print("📊 Availability Summary by Level:")
print("-" * 60)

for level in range(1, 5):
    total = db.courses.count_documents({"level": level})
    available = db.courses.count_documents({
        "level": level,
        "is_available_this_semester": True
    })
    
    print(f"Level {level}: {available}/{total} courses available")
    
    # Show which courses are available
    available_courses = list(db.courses.find({
        "level": level,
        "is_available_this_semester": True
    }, {"course_code": 1, "course_name": 1}))
    
    if available_courses:
        for course in available_courses:
            print(f"  ✓ {course['course_code']} - {course['course_name']}")
    print()

print("=" * 60)
print("✅ Course availability updated successfully!")
print("\n💡 Tip: Run this script at the start of each semester to update course offerings")
