"""
Template and script for importing real IIUM course data
Supports CSV, Excel, and JSON formats
"""
from pymongo import MongoClient
import pandas as pd
import json
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['fyp2']

print("📥 IIUM Course Data Import Tool\n")

# ============= OPTION 1: Import from CSV =============
def import_from_csv(filepath):
    """
    Expected CSV format:
    course_code,course_name,description,level,capacity,skills,prerequisites
    
    Example:
    CSCI4401,Artificial Intelligence,AI and ML concepts,4,25,"AI,ML,Python",CSCI3301
    """
    print(f"📄 Reading CSV from: {filepath}")
    df = pd.read_csv(filepath)
    
    courses = []
    for _, row in df.iterrows():
        course = {
            "course_code": row['course_code'],
            "course_name": row['course_name'],
            "description": row['description'],
            "level": int(row['level']) if pd.notna(row.get('level')) else 1,
            "capacity": int(row['capacity']) if pd.notna(row.get('capacity')) else 30,
        }
        
        # Parse skills (comma-separated)
        if pd.notna(row.get('skills')):
            course['skills'] = [s.strip() for s in str(row['skills']).split(',')]
        
        # Parse prerequisites (comma-separated)
        if pd.notna(row.get('prerequisites')):
            course['prerequisites'] = [s.strip() for s in str(row['prerequisites']).split(',')]
        
        # Add optional fields
        optional_fields = ['credit_hours', 'department', 'instructor', 'semester_offered']
        for field in optional_fields:
            if field in row and pd.notna(row[field]):
                course[field] = row[field]
        
        courses.append(course)
    
    return courses

# ============= OPTION 2: Import from Excel =============
def import_from_excel(filepath, sheet_name='Courses'):
    """
    Excel file with sheet containing course data
    Same columns as CSV format
    """
    print(f"📊 Reading Excel from: {filepath}, Sheet: {sheet_name}")
    df = pd.read_excel(filepath, sheet_name=sheet_name)
    # Use same logic as CSV
    return import_from_csv_dataframe(df)

def import_from_csv_dataframe(df):
    courses = []
    for _, row in df.iterrows():
        course = {
            "course_code": row['course_code'],
            "course_name": row['course_name'],
            "description": row.get('description', ''),
            "level": int(row['level']) if pd.notna(row.get('level')) else 1,
            "capacity": int(row['capacity']) if pd.notna(row.get('capacity')) else 30,
        }
        
        if pd.notna(row.get('skills')):
            course['skills'] = [s.strip() for s in str(row['skills']).split(',')]
        
        courses.append(course)
    
    return courses

# ============= OPTION 3: Import from JSON =============
def import_from_json(filepath):
    """
    JSON format:
    [
        {
            "course_code": "CSCI4401",
            "course_name": "Artificial Intelligence",
            "description": "AI concepts",
            "level": 4,
            "capacity": 25,
            "skills": ["AI", "ML", "Python"]
        }
    ]
    """
    print(f"📋 Reading JSON from: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    return courses

# ============= MAIN IMPORT FUNCTION =============
def import_courses(filepath, format='csv', replace=False):
    """
    Main import function
    
    Args:
        filepath: Path to data file
        format: 'csv', 'excel', or 'json'
        replace: If True, delete existing courses; if False, add to existing
    """
    print(f"\n🚀 Starting import from {format.upper()} file...")
    
    # Import based on format
    if format == 'csv':
        courses = import_from_csv(filepath)
    elif format == 'excel':
        courses = import_from_excel(filepath)
    elif format == 'json':
        courses = import_from_json(filepath)
    else:
        print(f"❌ Unsupported format: {format}")
        return
    
    if not courses:
        print("❌ No courses found in file!")
        return
    
    print(f"✓ Parsed {len(courses)} courses")
    
    # Preview first course
    print("\n📋 Sample course:")
    print(json.dumps(courses[0], indent=2))
    
    # Confirm import
    response = input(f"\n⚠️  Import {len(courses)} courses? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Import cancelled")
        return
    
    # Delete existing if replace mode
    if replace:
        count = db.courses.count_documents({})
        db.courses.delete_many({})
        print(f"🗑️  Deleted {count} existing courses")
    
    # Insert courses
    result = db.courses.insert_many(courses)
    print(f"✅ Imported {len(result.inserted_ids)} courses successfully!")
    
    # Show statistics
    print("\n📊 Database Statistics:")
    print(f"  Total courses: {db.courses.count_documents({})}")
    
    levels = db.courses.distinct("level")
    print(f"  Levels: {sorted(levels)}")
    
    for level in sorted(levels):
        count = db.courses.count_documents({"level": level})
        print(f"    Level {level}: {count} courses")

# ============= CREATE TEMPLATE FILES =============
def create_template_csv(filepath='course_import_template.csv'):
    """Create a template CSV file for import"""
    template_data = {
        'course_code': ['CSCI4401', 'CSCI4402'],
        'course_name': ['Artificial Intelligence', 'Data Science'],
        'description': ['AI and machine learning concepts', 'Data analysis and visualization'],
        'level': [4, 4],
        'capacity': [25, 25],
        'skills': ['AI,ML,Python', 'Data Science,Python,Statistics'],
        'prerequisites': ['CSCI3301', 'CSCI2301,STAT3101']
    }
    
    df = pd.DataFrame(template_data)
    df.to_csv(filepath, index=False)
    print(f"✓ Created template CSV: {filepath}")

# ============= USAGE EXAMPLES =============
if __name__ == "__main__":
    print("="*60)
    print("IIUM COURSE DATA IMPORT TOOL")
    print("="*60)
    
    print("\n📝 Usage Options:")
    print("1. Create template CSV file")
    print("2. Import from CSV file")
    print("3. Import from Excel file")
    print("4. Import from JSON file")
    
    choice = input("\nSelect option (1-4): ")
    
    if choice == '1':
        create_template_csv()
        print("\n✓ Template created! Fill it with your course data and use option 2 to import.")
    
    elif choice == '2':
        filepath = input("Enter CSV file path: ")
        replace = input("Replace existing courses? (yes/no): ").lower() == 'yes'
        import_courses(filepath, format='csv', replace=replace)
    
    elif choice == '3':
        filepath = input("Enter Excel file path: ")
        sheet = input("Enter sheet name (default: Courses): ") or 'Courses'
        replace = input("Replace existing courses? (yes/no): ").lower() == 'yes'
        import_courses(filepath, format='excel', replace=replace)
    
    elif choice == '4':
        filepath = input("Enter JSON file path: ")
        replace = input("Replace existing courses? (yes/no): ").lower() == 'yes'
        import_courses(filepath, format='json', replace=replace)
    
    else:
        print("❌ Invalid option")
