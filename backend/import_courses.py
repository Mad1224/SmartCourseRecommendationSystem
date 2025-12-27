"""
Import courses from CSV to MongoDB fyp2 database
"""
from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['fyp2']

# Read courses CSV
courses_df = pd.read_csv('ml/data/courses.csv')
print(f"Found {len(courses_df)} courses in CSV")

# Clear existing courses
db.courses.delete_many({})

# Prepare courses data
courses_data = []
for _, row in courses_df.iterrows():
    course = {
        "course_code": row['course_code'],
        "course_name": row['course_name'],
        "description": row['description']
    }
    
    # Add optional fields if they exist
    if 'level' in row and pd.notna(row['level']):
        course['level'] = int(row['level'])
    
    if 'capacity' in row and pd.notna(row['capacity']):
        course['capacity'] = int(row['capacity'])
    
    if 'skills' in row and pd.notna(row['skills']):
        # Skills might be a list or string
        skills = row['skills']
        if isinstance(skills, str):
            course['skills'] = [s.strip() for s in skills.split(',')]
        else:
            course['skills'] = []
    
    courses_data.append(course)
    print(f"  - {course['course_code']}: {course['course_name']}")

# Insert courses
if courses_data:
    result = db.courses.insert_many(courses_data)
    print(f"\n✓ Inserted {len(result.inserted_ids)} courses into fyp2 database")
else:
    print("❌ No courses to insert")

# Verify
count = db.courses.count_documents({})
print(f"✓ Total courses in database: {count}")
