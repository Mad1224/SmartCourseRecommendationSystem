"""
Check current courses in the database
"""
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['fyp2']

courses = list(db.courses.find({}))
print(f'Found {len(courses)} courses in database:\n')

for c in courses:
    print(f"{c['course_code']} - {c['course_name']}")
