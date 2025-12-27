"""
Generate Academic Data for users in the database
Creates realistic academic records with courses taken, grades, and CGPA
"""
from pymongo import MongoClient
from datetime import datetime
import random

client = MongoClient('mongodb://localhost:27017/')
db = client['fyp2']

print("📚 Generating Academic Data for Users\n")

# Get all student users
users = list(db.users.find({"role": "student"}))
print(f"Found {len(users)} students")

# Get all courses from database
all_courses = list(db.courses.find({}))

if not all_courses:
    print("❌ No courses found in database! Run generate_sample_data.py first.")
    exit(1)

# Grade points mapping
grade_points = {
    'A+': 4.0, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'F': 0.0
}

grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']  # Most students get B-A range

# Programs and kulliyyahs
programs = {
    'Computer Science': 'KICT',
    'Information Technology': 'KICT',
    'Data Science': 'KICT',
    'Software Engineering': 'KICT'
}

# Clear existing academic data
db.academic_data.delete_many({})

academic_records = []

for user in users:
    user_year = user.get('year', 2)
    user_program = user.get('program', 'Computer Science')
    user_kulliyyah = programs.get(user_program, 'KICT')
    
    # Determine courses taken based on year
    current_semester = user_year * 2  # Year 2 = Semester 4
    max_level = user_year  # Year 2 students can take up to level 2 courses
    
    # Select courses appropriate for the student's level
    eligible_courses = [c for c in all_courses if c.get('level', 1) <= max_level]
    
    # Number of courses taken (3-5 per semester)
    num_courses = random.randint(3, 5) * user_year
    selected_courses = random.sample(eligible_courses, min(num_courses, len(eligible_courses)))
    
    courses_taken = []
    total_points = 0
    total_credits = 0
    
    for i, course in enumerate(selected_courses):
        # Determine which semester the course was taken
        course_level = course.get('level', 1)
        semester_taken = random.randint(course_level * 2 - 1, min(course_level * 2, current_semester - 1))
        
        # Generate grade (bias toward better grades)
        grade = random.choices(
            grades,
            weights=[5, 10, 8, 7, 5, 3, 2, 1],  # More A's and B's
            k=1
        )[0]
        
        credit_hours = course.get('capacity', 3) if course.get('capacity', 3) <= 4 else 3
        
        course_record = {
            "course_code": course.get('course_code'),
            "course_name": course.get('course_name'),
            "semester_taken": semester_taken,
            "grade": grade,
            "credit_hours": credit_hours
        }
        
        courses_taken.append(course_record)
        
        # Calculate CGPA
        total_points += grade_points[grade] * credit_hours
        total_credits += credit_hours
    
    # Calculate final CGPA
    cgpa = round(total_points / total_credits, 2) if total_credits > 0 else 3.0
    
    # Create academic data document
    academic_doc = {
        "user_id": str(user["_id"]),
        "kulliyyah": user_kulliyyah,
        "programme": user_program,
        "current_semester": current_semester,
        "cgpa": cgpa,
        "courses_taken": sorted(courses_taken, key=lambda x: x['semester_taken']),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    academic_records.append(academic_doc)
    
    print(f"✓ {user['name']}")
    print(f"  Program: {user_program} | Year: {user_year} | Semester: {current_semester}")
    print(f"  CGPA: {cgpa} | Courses Taken: {len(courses_taken)}")
    print()

# Insert academic data
if academic_records:
    result = db.academic_data.insert_many(academic_records)
    print("="*60)
    print(f"✅ Created {len(result.inserted_ids)} academic records")
    print("="*60)
else:
    print("❌ No academic records created")

# Show summary
print("\n📊 Academic Data Summary:")
print(f"Total Records: {db.academic_data.count_documents({})}")

# Show CGPA distribution
cgpas = [rec['cgpa'] for rec in academic_records]
if cgpas:
    print(f"Average CGPA: {sum(cgpas)/len(cgpas):.2f}")
    print(f"Highest CGPA: {max(cgpas):.2f}")
    print(f"Lowest CGPA: {min(cgpas):.2f}")

# Show courses taken distribution
courses_per_student = [len(rec['courses_taken']) for rec in academic_records]
if courses_per_student:
    print(f"Average Courses/Student: {sum(courses_per_student)/len(courses_per_student):.1f}")
    print(f"Total Course Enrollments: {sum(courses_per_student)}")

print("\n✅ Academic data is ready!")
print("\n🔐 Login with any test account to view their academic data:")
print("  test@iium.edu.my / test123")
print("  ahmad@iium.edu.my / pass123")
print("  fatimah@iium.edu.my / pass123")
