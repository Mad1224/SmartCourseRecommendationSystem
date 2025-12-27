"""
Generate comprehensive sample data for testing AI recommendation system
Creates realistic IIUM courses, users, preferences, feedback, and enrollments
"""
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

client = MongoClient('mongodb://localhost:27017/')
db = client['fyp2']

print("🚀 Generating Sample Data for Smart Course Recommendation System\n")

# ============= COURSES =============
print("📚 Creating Courses...")
courses_data = [
    # Computer Science - Year 1
    {"course_code": "CSCI1100", "course_name": "Introduction to Computing", "description": "Basic computing concepts programming logic problem solving", "level": 1, "capacity": 40, "skills": ["Programming", "Logic", "Problem Solving"]},
    {"course_code": "CSCI1201", "course_name": "Programming I", "description": "Introduction to programming using Python basic syntax data structures", "level": 1, "capacity": 35, "skills": ["Python", "Data Structures", "Algorithms"]},
    
    # Computer Science - Year 2
    {"course_code": "CSCI2101", "course_name": "Data Structures", "description": "Advanced data structures arrays linked lists trees graphs", "level": 2, "capacity": 30, "skills": ["Data Structures", "Algorithms", "Analysis"]},
    {"course_code": "CSCI2201", "course_name": "Object-Oriented Programming", "description": "OOP concepts using Java classes inheritance polymorphism", "level": 2, "capacity": 30, "skills": ["Java", "OOP", "Design Patterns"]},
    {"course_code": "CSCI2301", "course_name": "Database Systems", "description": "Relational databases SQL normalization database design", "level": 2, "capacity": 35, "skills": ["SQL", "Database Design", "MySQL"]},
    
    # Computer Science - Year 3
    {"course_code": "CSCI3101", "course_name": "Web Development", "description": "HTML CSS JavaScript frameworks responsive design web applications", "level": 3, "capacity": 30, "skills": ["HTML", "CSS", "JavaScript", "React"]},
    {"course_code": "CSCI3201", "course_name": "Mobile App Development", "description": "iOS Android development mobile UI Flutter React Native", "level": 3, "capacity": 25, "skills": ["Flutter", "Mobile Dev", "UI Design"]},
    {"course_code": "CSCI3301", "course_name": "Software Engineering", "description": "Software development lifecycle agile testing requirements", "level": 3, "capacity": 30, "skills": ["SDLC", "Agile", "Testing"]},
    {"course_code": "CSCI3401", "course_name": "Computer Networks", "description": "Network protocols TCP IP routing switching network security", "level": 3, "capacity": 30, "skills": ["Networking", "TCP/IP", "Security"]},
    
    # Computer Science - Year 4
    {"course_code": "CSCI4101", "course_name": "Artificial Intelligence", "description": "AI concepts machine learning neural networks deep learning", "level": 4, "capacity": 25, "skills": ["AI", "Machine Learning", "Neural Networks"]},
    {"course_code": "CSCI4201", "course_name": "Data Science", "description": "Data analysis visualization statistics Python pandas machine learning", "level": 4, "capacity": 25, "skills": ["Data Science", "Python", "Statistics"]},
    {"course_code": "CSCI4301", "course_name": "Cybersecurity", "description": "Information security cryptography ethical hacking penetration testing", "level": 4, "capacity": 20, "skills": ["Security", "Cryptography", "Ethical Hacking"]},
    {"course_code": "CSCI4401", "course_name": "Cloud Computing", "description": "Cloud platforms AWS Azure containerization microservices DevOps", "level": 4, "capacity": 25, "skills": ["AWS", "Azure", "Docker", "DevOps"]},
    {"course_code": "CSCI4501", "course_name": "Big Data Analytics", "description": "Big data processing Hadoop Spark data mining analytics", "level": 4, "capacity": 20, "skills": ["Big Data", "Hadoop", "Spark"]},
    
    # Information Technology
    {"course_code": "INFO2101", "course_name": "IT Project Management", "description": "Project management methodologies planning budgeting risk management", "level": 2, "capacity": 35, "skills": ["Project Management", "Planning", "Leadership"]},
    {"course_code": "INFO3101", "course_name": "Business Intelligence", "description": "BI tools data warehousing OLAP reporting dashboards", "level": 3, "capacity": 30, "skills": ["BI", "Data Warehousing", "Reporting"]},
    {"course_code": "INFO3201", "course_name": "System Analysis and Design", "description": "System analysis UML design patterns requirements engineering", "level": 3, "capacity": 30, "skills": ["System Analysis", "UML", "Design"]},
    
    # Mathematics & Statistics
    {"course_code": "MATH2101", "course_name": "Discrete Mathematics", "description": "Logic sets relations graphs combinatorics proof techniques", "level": 2, "capacity": 40, "skills": ["Logic", "Mathematics", "Proof"]},
    {"course_code": "STAT3101", "course_name": "Probability and Statistics", "description": "Probability distributions hypothesis testing regression analysis", "level": 3, "capacity": 35, "skills": ["Statistics", "Probability", "Analysis"]},
    
    # Electives
    {"course_code": "CSCI4601", "course_name": "Game Development", "description": "Game design Unity game engines graphics programming", "level": 4, "capacity": 20, "skills": ["Game Dev", "Unity", "Graphics"]},
    {"course_code": "CSCI4602", "course_name": "IoT and Embedded Systems", "description": "Internet of Things Arduino sensors embedded programming", "level": 4, "capacity": 20, "skills": ["IoT", "Arduino", "Embedded Systems"]},
    {"course_code": "CSCI4603", "course_name": "Blockchain Technology", "description": "Blockchain cryptocurrency smart contracts distributed systems", "level": 4, "capacity": 20, "skills": ["Blockchain", "Cryptocurrency", "Smart Contracts"]},
    {"course_code": "INFO4101", "course_name": "Digital Marketing", "description": "Online marketing SEO social media analytics marketing strategies", "level": 4, "capacity": 30, "skills": ["Marketing", "SEO", "Social Media"]},
]

db.courses.delete_many({})
result = db.courses.insert_many(courses_data)
print(f"✓ Created {len(result.inserted_ids)} courses")

# ============= USERS =============
print("\n👥 Creating Users...")
users_data = [
    {"email": "test@iium.edu.my", "password": generate_password_hash("test123"), "name": "Test User", "matric_number": "2210000", "role": "student", "year": 2, "program": "Computer Science"},
    {"email": "ahmad@iium.edu.my", "password": generate_password_hash("pass123"), "name": "Ahmad Ali", "matric_number": "2110001", "role": "student", "year": 3, "program": "Computer Science"},
    {"email": "fatimah@iium.edu.my", "password": generate_password_hash("pass123"), "name": "Fatimah Hassan", "matric_number": "2210002", "role": "student", "year": 2, "program": "Information Technology"},
    {"email": "omar@iium.edu.my", "password": generate_password_hash("pass123"), "name": "Omar Ibrahim", "matric_number": "2010003", "role": "student", "year": 4, "program": "Computer Science"},
    {"email": "aisha@iium.edu.my", "password": generate_password_hash("pass123"), "name": "Aisha Rahman", "matric_number": "2210004", "role": "student", "year": 2, "program": "Data Science"},
    {"email": "yusuf@iium.edu.my", "password": generate_password_hash("pass123"), "name": "Yusuf Ahmed", "matric_number": "2110005", "role": "student", "year": 3, "program": "Computer Science"},
    {"email": "maryam@iium.edu.my", "password": generate_password_hash("pass123"), "name": "Maryam Khan", "matric_number": "2010006", "role": "student", "year": 4, "program": "Information Technology"},
    {"email": "ibrahim@iium.edu.my", "password": generate_password_hash("pass123"), "name": "Ibrahim Malik", "matric_number": "2310007", "role": "student", "year": 1, "program": "Computer Science"},
    {"email": "zahra@iium.edu.my", "password": generate_password_hash("pass123"), "name": "Zahra Noor", "matric_number": "2210008", "role": "student", "year": 2, "program": "Computer Science"},
    {"email": "hassan@iium.edu.my", "password": generate_password_hash("pass123"), "name": "Hassan Abdullah", "matric_number": "2110009", "role": "student", "year": 3, "program": "Data Science"},
    {"email": "admin@iium.edu.my", "password": generate_password_hash("admin123"), "name": "System Admin", "matric_number": "ADMIN", "role": "admin", "year": None, "program": None},
]

# Keep existing test user, add others
existing_user = db.users.find_one({"email": "test@iium.edu.my"})
if not existing_user:
    db.users.insert_many(users_data)
    print(f"✓ Created {len(users_data)} users")
else:
    new_users = [u for u in users_data if u["email"] != "test@iium.edu.my"]
    if new_users:
        db.users.insert_many(new_users)
        print(f"✓ Created {len(new_users)} new users (kept existing test user)")

# Get user IDs for later use
users = list(db.users.find({"role": "student"}))
user_ids = [str(u["_id"]) for u in users]

# ============= PREFERENCES =============
print("\n⚙️ Creating User Preferences...")
preferences_data = []
programs = ["Computer Science", "Information Technology", "Data Science"]
preferred_times = ["Morning", "Afternoon", "Evening"]
preferred_types = [["Practical", "Theoretical"], ["Hands-on", "Project-based"], ["Lecture", "Lab"]]

for user in users[:8]:  # Create preferences for 8 users
    pref = {
        "user_id": str(user["_id"]),
        "kulliyyah": "KICT",
        "semester": user.get("year", 2) * 2,  # Approximate semester
        "cgpa": round(random.uniform(2.5, 4.0), 2),
        "preferredTypes": random.choice(preferred_types),
        "preferredTime": random.choice(preferred_times),
        "coursesToAvoid": [],
        "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 30))
    }
    preferences_data.append(pref)

db.preferences.delete_many({})
result = db.preferences.insert_many(preferences_data)
print(f"✓ Created {len(result.inserted_ids)} preference records")

# ============= ENROLLMENTS =============
print("\n📝 Creating Enrollments...")
enrollments_data = []
course_codes = [c["course_code"] for c in courses_data]

for user in users:
    user_level = user.get("year", 2)
    # Enroll in appropriate level courses
    eligible_courses = [c for c in courses_data if c.get("level", 1) <= user_level]
    num_enrollments = random.randint(3, 6)
    enrolled_courses = random.sample(eligible_courses, min(num_enrollments, len(eligible_courses)))
    
    for course in enrolled_courses:
        enrollment = {
            "user_id": str(user["_id"]),
            "course_id": str(db.courses.find_one({"course_code": course["course_code"]})["_id"]),
            "enrolled_at": datetime.utcnow() - timedelta(days=random.randint(30, 180)),
            "status": "enrolled"
        }
        enrollments_data.append(enrollment)

db.enrollments.delete_many({})
result = db.enrollments.insert_many(enrollments_data)
print(f"✓ Created {len(result.inserted_ids)} enrollments")

# ============= FEEDBACK =============
print("\n⭐ Creating Feedback...")
feedback_data = []

for enrollment in enrollments_data[:40]:  # Create feedback for 40 enrollments
    try:
        from bson import ObjectId
        course_id = enrollment["course_id"]
        if isinstance(course_id, str):
            course_id = ObjectId(course_id)
        
        course = db.courses.find_one({"_id": course_id})
        if not course:
            continue
        
        rating = random.choices([3, 4, 5], weights=[2, 3, 5])[0]  # Bias toward positive
        
        comments = {
            5: ["Excellent course! Learned a lot.", "Best course ever!", "Highly recommend this course.", "Professor was amazing!"],
            4: ["Good course but quite challenging.", "Really enjoyed the content.", "Well structured course.", "Very practical and useful."],
            3: ["Average course, could be better.", "Decent but needs improvement.", "Good but quite tough.", "Okay experience overall."]
        }
        
        feedback = {
            "user_id": enrollment["user_id"],
            "course_code": course["course_code"],
            "rating": rating,
            "comment": random.choice(comments[rating])
        }
        feedback_data.append(feedback)
    except Exception as e:
        print(f"Skipping feedback: {e}")
        continue

if feedback_data:
    db.feedback.delete_many({})
    result = db.feedback.insert_many(feedback_data)
    print(f"✓ Created {len(result.inserted_ids)} feedback entries")
else:
    print("⚠ No feedback created")

# ============= SUMMARY =============
print("\n" + "="*50)
print("📊 DATA GENERATION COMPLETE")
print("="*50)
print(f"Courses:      {db.courses.count_documents({})}")
print(f"Users:        {db.users.count_documents({})}")
print(f"Preferences:  {db.preferences.count_documents({})}")
print(f"Enrollments:  {db.enrollments.count_documents({})}")
print(f"Feedback:     {db.feedback.count_documents({})}")
print("="*50)
print("\n✅ Sample data is ready for testing!")
print("\n🔐 Test Accounts:")
print("  test@iium.edu.my / test123")
print("  ahmad@iium.edu.my / pass123")
print("  fatimah@iium.edu.my / pass123")
print("  admin@iium.edu.my / admin123")
