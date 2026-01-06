"""
List all users and their login credentials from the database
"""
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

client = MongoClient('mongodb://localhost:27017/')
db = client['fyp2']

users = list(db.users.find({}))

print(f"📋 Total Users in Database: {len(users)}\n")
print("="*80)
print(f"{'Email':<30} {'Password':<15} {'Name':<20} {'Role':<10}")
print("="*80)

# Common test password to check against
test_passwords = ['test123', 'pass123', 'password123', 'admin123', '123456']

for user in users:
    email = user.get('email', 'N/A')
    name = user.get('name', 'N/A')
    role = user.get('role', 'student')
    password_hash = user.get('password', '')
    
    # Try to match common passwords
    matched_password = '???'
    for pwd in test_passwords:
        try:
            from werkzeug.security import check_password_hash
            if check_password_hash(password_hash, pwd):
                matched_password = pwd
                break
        except:
            pass
    
    print(f"{email:<30} {matched_password:<15} {name:<20} {role:<10}")

print("="*80)
print("\n📝 Note: Passwords are hashed in the database for security.")
print("   Only common test passwords are shown above.")
print("\n💡 Default test accounts:")
print("   - test@iium.edu.my / test123")
print("   - admin@iium.edu.my / admin123")
