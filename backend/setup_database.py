"""
Setup script to populate MongoDB with data from CSV files
This script will:
1. Read CSV files (courses.csv, users.csv, feedback.csv)
2. Connect to MongoDB
3. Populate the database with initial data
"""

import pandas as pd
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

# Get MongoDB URI from environment
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/course_recommendation_db")

print(f"Connecting to MongoDB: {MONGO_URI}")

try:
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db_name = MONGO_URI.split('/')[-1].split('?')[0] if '/' in MONGO_URI else 'course_recommendation_db'
    db = client[db_name]
    
    print(f"Connected to database: {db_name}")
    
    # Clear existing collections (optional - comment out if you want to keep existing data)
    print("\nClearing existing collections...")
    db.courses.delete_many({})
    db.users.delete_many({})
    db.feedback.delete_many({})
    print("Collections cleared.")
    
    # 1. Load and insert COURSES
    print("\n--- Loading Courses ---")
    courses_df = pd.read_csv('ml/data/courses.csv')
    print(f"Found {len(courses_df)} courses")
    
    courses_data = []
    for _, row in courses_df.iterrows():
        course = {
            "course_code": row['course_code'],
            "course_name": row['course_name'],
            "description": row['description']
        }
        courses_data.append(course)
    
    if courses_data:
        result = db.courses.insert_many(courses_data)
        print(f"✓ Inserted {len(result.inserted_ids)} courses")
    
    # 2. Load and insert USERS (create some test users)
    print("\n--- Loading Users ---")
    users_df = pd.read_csv('ml/data/users.csv')
    print(f"Found {len(users_df)} users in CSV")
    
    # Create test users with hashed passwords
    test_users = [
        {
            "email": "student1@iium.edu.my",
            "password": generate_password_hash("password123"),
            "name": "Ahmad Ali",
            "matric_number": "1234567",
            "role": "student"
        },
        {
            "email": "student2@iium.edu.my",
            "password": generate_password_hash("password123"),
            "name": "Fatimah Hassan",
            "matric_number": "1234568",
            "role": "student"
        },
        {
            "email": "test@iium.edu.my",
            "password": generate_password_hash("test123"),
            "name": "Test User",
            "matric_number": "9999999",
            "role": "student"
        }
    ]
    
    result = db.users.insert_many(test_users)
    print(f"✓ Inserted {len(result.inserted_ids)} test users")
    print("  Test credentials:")
    print("  Email: student1@iium.edu.my | Password: password123")
    print("  Email: student2@iium.edu.my | Password: password123")
    print("  Email: test@iium.edu.my | Password: test123")
    
    # 3. Load and insert FEEDBACK (if exists)
    print("\n--- Loading Feedback ---")
    try:
        feedback_df = pd.read_csv('ml/data/feedback.csv')
        print(f"Found {len(feedback_df)} feedback entries")
        
        if len(feedback_df) > 0:
            feedback_data = feedback_df.to_dict('records')
            result = db.feedback.insert_many(feedback_data)
            print(f"✓ Inserted {len(result.inserted_ids)} feedback entries")
    except FileNotFoundError:
        print("No feedback.csv found, skipping...")
    
    # Display summary
    print("\n" + "="*50)
    print("DATABASE SETUP COMPLETE!")
    print("="*50)
    print(f"Database: {db_name}")
    print(f"Courses: {db.courses.count_documents({})}")
    print(f"Users: {db.users.count_documents({})}")
    print(f"Feedback: {db.feedback.count_documents({})}")
    print("\n✓ You can now start your Flask app and login!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure MongoDB is running and accessible!")
    print("If using MongoDB Atlas, check your connection string in .env file")
