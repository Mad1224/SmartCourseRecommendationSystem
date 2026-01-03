"""
Script to add sample lecturers/advisers to the database
These will be available for students to request advising from
"""
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

client = MongoClient('mongodb://localhost:27017/')
db = client['fyp2']

print("👨‍🏫 Adding Sample Lecturers/Advisers\n")
print("=" * 60)

lecturers = [
    {
        "email": "dr.ahmad@iium.edu.my",
        "password": generate_password_hash("lecturer123"),
        "name": "Dr. Ahmad bin Abdullah",
        "matric_number": "STAFF001",
        "role": "lecturer",
        "specialization": "Software Engineering & Web Development"
    },
    {
        "email": "dr.fatimah@iium.edu.my",
        "password": generate_password_hash("lecturer123"),
        "name": "Dr. Fatimah binti Hassan",
        "matric_number": "STAFF002",
        "role": "lecturer",
        "specialization": "Data Science & Machine Learning"
    },
    {
        "email": "dr.ibrahim@iium.edu.my",
        "password": generate_password_hash("lecturer123"),
        "name": "Dr. Ibrahim bin Ali",
        "matric_number": "STAFF003",
        "role": "lecturer",
        "specialization": "Cybersecurity & Network"
    },
    {
        "email": "dr.sarah@iium.edu.my",
        "password": generate_password_hash("lecturer123"),
        "name": "Dr. Sarah binti Rahman",
        "matric_number": "STAFF004",
        "role": "staff",
        "specialization": "General Academic Advising"
    },
    {
        "email": "coordinator@iium.edu.my",
        "password": generate_password_hash("coordinator123"),
        "name": "Academic Coordinator",
        "matric_number": "COORD001",
        "role": "staff",
        "specialization": "Course Registration & Academic Planning"
    }
]

added_count = 0
existing_count = 0

for lecturer in lecturers:
    # Check if lecturer already exists
    existing = db.users.find_one({"email": lecturer["email"]})
    
    if existing:
        print(f"⚠️  {lecturer['name']} already exists")
        existing_count += 1
    else:
        db.users.insert_one(lecturer)
        print(f"✅ Added: {lecturer['name']}")
        print(f"   Email: {lecturer['email']}")
        print(f"   Specialization: {lecturer['specialization']}")
        print()
        added_count += 1

print("=" * 60)
print(f"✅ Added {added_count} new lecturers/advisers")
print(f"⚠️  {existing_count} already existed")
print("=" * 60)

print("\n📋 Lecturer Accounts:")
print("-" * 60)
for lecturer in lecturers:
    print(f"Email: {lecturer['email']}")
    print(f"Password: lecturer123 (or coordinator123)")
    print(f"Name: {lecturer['name']}")
    print(f"Specialization: {lecturer['specialization']}")
    print()

print("=" * 60)
print("✅ Lecturers are ready to receive advising requests!")