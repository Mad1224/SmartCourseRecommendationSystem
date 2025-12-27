from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['fyp2']

# Check if user exists
existing = db.users.find_one({'email': 'test@iium.edu.my'})
if existing:
    print('User test@iium.edu.my already exists')
else:
    # Create test user
    test_user = {
        'email': 'test@iium.edu.my',
        'password': generate_password_hash('test123'),
        'name': 'Test User',
        'matric_number': '2210000',
        'role': 'student',
        'year': 2,
        'program': 'Computer Science'
    }
    
    result = db.users.insert_one(test_user)
    print(f'✓ Created user: test@iium.edu.my')
    print(f'  Password: test123')
    print(f'  User ID: {result.inserted_id}')

print('\nAll users in fyp2:')
for user in db.users.find({}, {'email': 1, 'name': 1}):
    print(f'  - {user["email"]} ({user.get("name", "No name")})')
