"""
Display detailed information for sample courses from each kulliyyah
"""
from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017/')
db = client['fyp2']

print('🔍 Sample Course Details from Each Kulliyyah\n')
print('='*80)

kulliyyahs = ['KICT', 'KOE', 'KENMS', 'KAHS', 'KOP', 'KIRKHS']

for kulliyyah in kulliyyahs:
    courses = list(db.courses.find({'kulliyyah': kulliyyah}).limit(2))
    
    if courses:
        print(f'\n\n{kulliyyah} - Sample Courses:\n')
        for course in courses:
            print(f"📚 {course['course_code']}: {course['course_name']}")
            print(f"   Kulliyyah: {course.get('kulliyyah', 'N/A')}")
            print(f"   Program: {course.get('program', 'N/A')}")
            print(f"   Level: {course.get('level', 'N/A')}")
            print(f"   Description: {course.get('description', 'N/A')}")
            if course.get('skills'):
                print(f"   Skills: {', '.join(course['skills'])}")
            print()

print('='*80)
print(f"\n✅ Database now contains courses from 6 IIUM Kulliyyahs!")
print(f"   Total: {db.courses.count_documents({})} courses")
