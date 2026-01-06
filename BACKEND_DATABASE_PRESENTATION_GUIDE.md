# Smart Course Recommendation System - Backend & Database Overview

## 🎯 Technology Stack

### Backend Framework
- **Framework**: Flask 3.1.2 (Python web framework)
- **Language**: Python 3.x
- **API Style**: RESTful API
- **Authentication**: JWT (JSON Web Tokens) via Flask-JWT-Extended
- **CORS**: Flask-CORS for cross-origin requests
- **Port**: 5000 (local development)

### Database
- **Database**: MongoDB 4.15.5 (NoSQL document database)
- **Driver**: PyMongo with Flask-PyMongo
- **Connection**: MongoDB Atlas or Local MongoDB
- **Database Name**: `fyp2`

### Machine Learning
- **ML Library**: Scikit-learn 1.7.2
- **NLP**: NLTK (Natural Language Toolkit)
- **Text Processing**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Data Processing**: Pandas 2.3.3, NumPy 2.3.5
- **Model Persistence**: Joblib

---

## 📁 Backend Architecture

### Project Structure
```
backend/
├── app.py                      # Main Flask application
├── config/
│   └── config.py              # Configuration management
├── database/
│   └── mongo.py               # MongoDB connection
├── routes/                     # API endpoints (Blueprints)
│   ├── auth_routes.py         # Login, Registration
│   ├── course_routes.py       # Course catalog operations
│   ├── enrollment_routes.py   # Course enrollment/drop
│   ├── feedback_routes.py     # Rating & reviews
│   ├── recommend_routes.py    # AI recommendations
│   ├── preferences_routes.py  # User preferences
│   ├── academic_routes.py     # Academic records
│   ├── advising_routes.py     # Academic advising
│   └── metrics_routes.py      # Performance metrics
├── ml/                         # Machine Learning Engine
│   ├── recommendation_engine.py
│   ├── preprocessing.py
│   └── artifacts/             # Trained models
└── utils/                      # Helper functions
```

---

## 🗄️ MongoDB Database Schema

### Collections Overview
The database uses **7 main collections**:

### 1. **users** Collection
Stores student and admin accounts.

```javascript
{
  "_id": ObjectId("..."),
  "name": "Muhammad Abdullah",
  "email": "student@iium.edu.my",
  "password": "hashed_password",      // Werkzeug hashed
  "matric_number": "2210000",
  "kulliyyah": "KICT",
  "programme": "Computer Science",
  "year": 2,
  "phone": "012-3456789",
  "role": "student",                  // or "admin", "lecturer"
  "created_at": ISODate("2025-01-01")
}
```

**Indexes**: `email` (unique), `matric_number` (unique)

### 2. **courses** Collection
Complete course catalog.

```javascript
{
  "_id": ObjectId("..."),
  "course_code": "INFO 4201",
  "course_name": "Database Systems",
  "description": "Introduction to database design, SQL...",
  "level": 4,                          // Year level (1-4)
  "capacity": 35,
  "credit_hours": 3,
  "skills": [
    "SQL", "Database Design", "Normalization"
  ],
  "prerequisites": ["INFO 3201"],
  "is_available_this_semester": true,
  "semester": "2024/2025 Sem 1",
  "instructor": "Dr. Ahmad",
  "department": "KICT"
}
```

**Indexes**: `course_code` (unique), `is_available_this_semester`

### 3. **enrollments** Collection
Student course registrations.

```javascript
{
  "_id": ObjectId("..."),
  "user_id": ObjectId("..."),          // Reference to users
  "course_id": ObjectId("..."),        // Reference to courses
  "enrolled_at": ISODate("2025-01-15"),
  "status": "enrolled"                 // or "dropped", "completed"
}
```

**Indexes**: Compound index on `(user_id, course_id, status)`

**Business Rules**:
- Max 20 credit hours per student per semester
- Cannot enroll in full courses (capacity check)
- No duplicate enrollments

### 4. **feedback** Collection
Course ratings and reviews.

```javascript
{
  "_id": ObjectId("..."),
  "user_id": "ObjectId(...)",
  "user_name": "Muhammad Abdullah",
  "course_code": "INFO 4201",
  "course_name": "Database Systems",
  "rating": 5,                         // 1-5 stars
  "comment": "Excellent course!",
  "likes": 12,
  "created_at": "2025-01-20T10:30:00",
  "updated_at": "2025-01-20T10:30:00"
}
```

**Constraints**:
- One feedback per user per course
- Rating must be 1-5
- Used for collaborative filtering in recommendations

### 5. **preferences** Collection
User course preferences for recommendations.

```javascript
{
  "_id": ObjectId("..."),
  "user_id": "ObjectId(...)",
  "kulliyyah": "KICT",
  "semester": 4,
  "cgpa": 3.75,
  "preferredTypes": [
    "Theory", "Practical"
  ],
  "preferredTime": "Morning",          // Morning/Afternoon/Evening
  "coursesToAvoid": ["INFO 3999"],
  "topics": ["AI", "Machine Learning"],
  "goals": ["Research", "Industry"],
  "created_at": ISODate("2025-01-10"),
  "updated_at": ISODate("2025-01-15")
}
```

**Note**: Latest preference is used for recommendations (sorted by `created_at`)

### 6. **academic_data** Collection
Student academic history and transcript.

```javascript
{
  "_id": ObjectId("..."),
  "user_id": "ObjectId(...)",
  "kulliyyah": "KICT",
  "programme": "Computer Science",
  "current_semester": 4,
  "cgpa": 3.75,
  "courses_taken": [
    {
      "course_code": "INFO 3201",
      "course_name": "Data Structures",
      "semester_taken": 3,
      "grade": "A",                    // A, A-, B+, B, etc.
      "credit_hours": 3
    },
    {
      "course_code": "INFO 3301",
      "course_name": "Algorithms",
      "semester_taken": 3,
      "grade": "A-",
      "credit_hours": 4
    }
  ],
  "created_at": ISODate("2025-01-01"),
  "updated_at": ISODate("2025-01-15")
}
```

**Purpose**:
- Track completed courses to avoid re-recommendations
- Calculate CGPA and credit hours
- Check prerequisites

### 7. **advising_sessions** Collection
Academic advising records.

```javascript
{
  "_id": ObjectId("..."),
  "user_id": "ObjectId(...)",
  "adviser_id": "ObjectId(...)",       // Lecturer/adviser
  "session_date": ISODate("2025-01-20"),
  "notes": "Recommended to take AI courses",
  "recommended_courses": [
    "INFO 4301", "INFO 4401"
  ],
  "status": "completed"                // scheduled/completed/cancelled
}
```

---

## 🔌 API Endpoints

### Authentication Endpoints (`/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register new user | ❌ |
| POST | `/auth/login` | Login user | ❌ |
| GET | `/auth/profile` | Get user profile | ✅ |
| PUT | `/auth/profile` | Update profile | ✅ |

**Example Request: Login**
```json
POST /auth/login
{
  "email": "student@iium.edu.my",
  "password": "password123"
}

Response (200):
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "abc123",
    "name": "Muhammad Abdullah",
    "email": "student@iium.edu.my"
  }
}
```

### Course Endpoints (`/courses`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/courses/` | Get all courses | ✅ |
| GET | `/courses/available` | Get available courses only | ✅ |
| GET | `/courses/<id>` | Get course details | ✅ |
| POST | `/courses/` | Create course (admin) | ✅ |
| PUT | `/courses/<id>` | Update course (admin) | ✅ |
| DELETE | `/courses/<id>` | Delete course (admin) | ✅ |

### Enrollment Endpoints (`/enroll`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/enroll` | Enroll in course | ✅ |
| DELETE | `/enroll` | Drop course | ✅ |
| GET | `/enroll/my-enrollments` | Get user's enrollments | ✅ |

**Example Request: Enroll**
```json
POST /enroll
{
  "course_id": "507f1f77bcf86cd799439011"
}

Response (200):
{
  "msg": "Enrollment successful",
  "course_id": "507f1f77bcf86cd799439011"
}

Response (400 - Full):
{
  "msg": "Course is full",
  "course_id": "507f1f77bcf86cd799439011"
}

Response (400 - Credit Limit):
{
  "msg": "Credit hour limit reached",
  "current_credit_hours": 18,
  "max_credit_hours": 20
}
```

### Recommendation Endpoints (`/recommend`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET/POST | `/recommend/` | Get AI recommendations | ✅ |

**How It Works**:
1. Reads user preferences from `preferences` collection
2. Gets courses already taken from `academic_data`
3. Fetches user's feedback for collaborative filtering
4. Runs hybrid ML algorithm (content + collaborative)
5. Returns top 10 courses with scores (0-1 range)

**Response Example**:
```json
[
  {
    "_id": "abc123",
    "course_code": "INFO 4501",
    "course_name": "Artificial Intelligence",
    "description": "Introduction to AI concepts...",
    "level": 4,
    "credit_hours": 3,
    "skills": ["Python", "Machine Learning", "AI"],
    "score": 0.89,                    // Recommendation score
    "is_available_this_semester": true
  },
  {
    "course_code": "INFO 4401",
    "course_name": "Data Mining",
    "score": 0.85,
    ...
  }
]
```

### Feedback Endpoints (`/feedback`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/feedback/` | Submit feedback | ✅ |
| GET | `/feedback/all` | Get all feedback | ✅ |
| GET | `/feedback/course/<code>` | Get course feedback | ✅ |
| GET | `/feedback/my-feedback` | Get user's feedback | ✅ |
| PUT | `/feedback/<id>` | Update feedback | ✅ |
| DELETE | `/feedback/<id>` | Delete feedback | ✅ |

### Academic Endpoints (`/academic`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/academic/` | Save academic data | ✅ |
| GET | `/academic/` | Get academic data | ✅ |
| POST | `/academic/course` | Add course to transcript | ✅ |
| DELETE | `/academic/course` | Remove course | ✅ |

---

## 🤖 Machine Learning Engine

### Architecture Overview

The recommendation system uses a **Hybrid Approach**:
- **Content-Based Filtering** (TF-IDF)
- **Collaborative Filtering** (User ratings)
- **Adaptive Weighting** (Dynamic alpha)

### How It Works

#### Step 1: Data Preprocessing
```python
# preprocessing.py
def preprocess_text(text):
    - Lowercase conversion
    - Remove special characters
    - Tokenization
    - Remove stopwords (NLTK)
    - Lemmatization
    - Return cleaned text
```

#### Step 2: TF-IDF Model Training
```python
# rebuild_models.py
1. Fetch all courses from MongoDB
2. Combine: course_name + description + skills
3. Preprocess text for each course
4. Build TF-IDF vectorizer
5. Create course TF-IDF matrix
6. Save models to ml/artifacts/
   - tfidf_vectorizer.pkl
   - course_tfidf_matrix.pkl
```

**TF-IDF Explained**:
- **Term Frequency**: How often words appear in course description
- **Inverse Document Frequency**: Rarity of words across all courses
- Creates numerical vectors representing course content
- Similar courses have similar vectors

#### Step 3: Content-Based Filtering
```python
def compute_content_similarity(user_query):
    1. User preferences → text query
       Example: "programming web development database"
    
    2. Vectorize query using TF-IDF
    
    3. Compute cosine similarity with all courses
       cos(θ) = (A · B) / (||A|| × ||B||)
    
    4. Return similarity scores (0-1)
       Higher = more relevant to user interests
```

#### Step 4: Collaborative Filtering
```python
def compute_collaborative_scores(course_codes, feedback_docs):
    1. Aggregate ratings from all users
    
    2. For each course:
       average_rating = sum(ratings) / count(ratings)
    
    3. Normalize to 0-1 range:
       score = average_rating / 5.0
    
    4. Return collaborative scores
```

#### Step 5: Hybrid Recommendation
```python
def hybrid_recommend(user_query, course_codes, feedback_docs):
    1. Get content scores (TF-IDF similarity)
    2. Get collaborative scores (average ratings)
    
    3. Calculate adaptive alpha:
       - No feedback → alpha = 0.9 (90% content)
       - Few feedback → alpha = 0.8 (80% content)
       - Some feedback → alpha = 0.6 (balanced)
       - Lots feedback → alpha = 0.3 (70% collaborative)
    
    4. Combine scores:
       final_score = alpha × content_score + (1-alpha) × collab_score
    
    5. Sort by final_score descending
    6. Return top 10 recommendations
```

### Adaptive Alpha Logic

| Feedback Count | Alpha | Content Weight | Collaborative Weight |
|----------------|-------|----------------|----------------------|
| 0 | 0.9 | 90% | 10% |
| 1-4 | 0.8 | 80% | 20% |
| 5-19 | 0.6 | 60% | 40% |
| 20+ | 0.3 | 30% | 70% |

**Why Adaptive?**
- **New system**: Rely on content (no ratings yet)
- **Mature system**: Trust user ratings (cold start solved)

### Real Example

**User Preferences**:
- Kulliyyah: KICT
- Interests: AI, Machine Learning, Python
- CGPA: 3.75

**Content-Based** finds courses with:
- Words: "artificial intelligence", "machine learning", "python"
- High TF-IDF similarity

**Collaborative** finds courses with:
- High average ratings from other students
- Popular among similar users

**Hybrid** balances both:
- Course A: High content (0.9), Low rating (0.6) → Final: 0.75
- Course B: Medium content (0.7), High rating (0.9) → Final: 0.80
- **Course B wins!** (Better overall)

---

## 🔐 Security & Authentication

### JWT Authentication Flow

1. **User logs in** → Sends email + password
2. **Backend validates** → Checks password hash
3. **Generate JWT token** → Contains user_id, expires in 24h
4. **Return token** → Frontend stores in Session
5. **Every API call** → Include `Authorization: Bearer <token>`
6. **Backend verifies** → Decodes JWT, extracts user_id
7. **Process request** → Access user's data

### Password Security
- **Hashing**: Werkzeug's `generate_password_hash()`
- **Algorithm**: PBKDF2-SHA256 (secure)
- **No plaintext storage**: Passwords never stored directly

### JWT Configuration
```python
JWT_SECRET_KEY = "your-secret-key-here"  # From .env
JWT_TOKEN_LOCATION = ["headers"]
JWT_HEADER_NAME = "Authorization"
JWT_HEADER_TYPE = "Bearer"
```

### Protected Routes
All routes except `/auth/login` and `/auth/register` require JWT token.

**Error Responses**:
- 401: Missing token
- 401: Invalid token
- 401: Expired token

---

## 🚀 Key Features & Algorithms

### 1. Smart Enrollment System

**Features**:
- Real-time capacity checking
- Credit hour limit enforcement (20 max)
- Duplicate enrollment prevention
- Prerequisite validation

**Algorithm**:
```
function enrollCourse(user_id, course_id):
    course = getCourse(course_id)
    
    // Check capacity
    enrolled_count = countEnrollments(course_id)
    if enrolled_count >= course.capacity:
        return ERROR: "Course is full"
    
    // Check duplicate
    existing = findEnrollment(user_id, course_id)
    if existing:
        return ERROR: "Already enrolled"
    
    // Check credit limit
    user_credits = sumCreditHours(user_id)
    if user_credits + course.credit_hours > 20:
        return ERROR: "Credit limit reached"
    
    // Enroll
    createEnrollment(user_id, course_id)
    return SUCCESS
```

### 2. Recommendation Filtering

**Filters Applied**:
1. ✅ **Exclude taken courses**: No re-recommendations
2. ✅ **Exclude enrolled courses**: No duplicates
3. ✅ **Score-based ranking**: Best matches first
4. ✅ **Availability filter**: Optional (show all or available only)
5. ✅ **Preference matching**: Kulliyyah, time, type

### 3. Feedback Aggregation

**Statistics Calculated**:
- Average rating per course
- Total feedback count
- Rating distribution (5★, 4★, 3★, etc.)
- Top-rated courses
- Most reviewed courses

### 4. Academic Progress Tracking

**Metrics Computed**:
- CGPA calculation
- Total credit hours earned
- Courses per semester
- Grade distribution
- Prerequisite completion status

---

## 📊 Performance Optimizations

### Database Indexing
```javascript
// Indexes created for fast queries
db.users.createIndex({ email: 1 }, { unique: true })
db.users.createIndex({ matric_number: 1 }, { unique: true })
db.courses.createIndex({ course_code: 1 }, { unique: true })
db.enrollments.createIndex({ user_id: 1, course_id: 1 })
db.feedback.createIndex({ user_id: 1, course_code: 1 })
```

### Caching Strategy
- TF-IDF models loaded once at startup
- Course data cached in memory during recommendations
- JWT tokens expire in 24h (reduces DB queries)

### Query Optimization
- Use projection to select only needed fields
- Limit results (top 10 recommendations)
- Compound indexes for frequent queries

---

## 🛠️ Development Workflow

### Setup & Installation

**1. Install Dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

**2. Configure Environment** (`.env`):
```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
MONGO_URI=mongodb://localhost:27017/fyp2
```

**3. Setup Database**:
```bash
python setup_database.py
```

**4. Build ML Models**:
```bash
python rebuild_models.py
```

**5. Start Backend**:
```bash
python app.py
# or
.\start_backend.bat
```

### Important Scripts

| Script | Purpose |
|--------|---------|
| `app.py` | Main Flask application |
| `setup_database.py` | Populate DB from CSV files |
| `rebuild_models.py` | Rebuild TF-IDF models |
| `generate_academic_data.py` | Generate sample academic data |
| `import_courses.py` | Import courses from CSV |
| `add_test_user.py` | Create test users |
| `check_engine.py` | Test ML engine |
| `set_course_availability.py` | Mark courses as available |

---

## 💡 Demo Flow for Presentation

### 1. Database Overview (2 min)
- Show MongoDB Compass or Studio 3T
- Display collections: users, courses, enrollments, feedback
- Show sample documents from each collection
- Explain relationships between collections

### 2. API Testing (3 min)
- Use Postman or Thunder Client
- **Demo Login**: Show JWT token generation
- **Demo Get Courses**: Show course catalog API
- **Demo Recommendations**: Show AI recommendation response
- Highlight response structure and scores

### 3. ML Engine Explanation (3 min)
- Open `recommendation_engine.py`
- Explain TF-IDF visualization (optional: show word cloud)
- Show `rebuild_models.py` - model training process
- Explain hybrid algorithm with diagram

### 4. Code Walkthrough (2 min)
- Show `recommend_routes.py` - main recommendation logic
- Show `enrollment_routes.py` - business rules
- Highlight error handling and validation

---

## 🎤 Key Talking Points

### What makes this backend special?

1. **Intelligent Hybrid Recommendations**
   - Not just simple filtering - actual AI/ML
   - Combines content similarity (what course is about) with collaborative filtering (what others liked)
   - Adaptive algorithm that improves with more data

2. **Robust Business Logic**
   - Enforces academic rules (credit limits, capacity, prerequisites)
   - Prevents data inconsistencies
   - Real-time validation

3. **Scalable Architecture**
   - RESTful API design (stateless)
   - Blueprint-based routing (modular)
   - MongoDB for flexible schema
   - Easy to add new features

4. **Production-Ready**
   - JWT authentication
   - Error handling (404, 500, 401)
   - Input validation
   - CORS support for frontend

### MongoDB Advantages

1. **Flexibility**: No rigid schema - easy to add fields
2. **Performance**: Fast document retrieval with indexing
3. **Scalability**: Horizontal scaling with sharding
4. **JSON-like**: Natural fit for REST APIs
5. **Rich Queries**: Supports complex aggregations

### ML Algorithm Advantages

1. **Cold Start Solution**: Works even with no feedback (content-based)
2. **Improved Over Time**: Better with more user ratings (collaborative)
3. **Personalized**: Uses individual preferences
4. **Explainable**: Can show why courses recommended (TF-IDF scores)

---

## ❓ Potential Questions & Answers

### Q: Why MongoDB instead of MySQL/PostgreSQL?
**A**: MongoDB provides schema flexibility for evolving requirements, native JSON support for REST APIs, and excellent performance for document-based queries. For a recommendation system, the nested structure (courses with skills array, preferences with topics array) is more natural in MongoDB than in relational tables.

### Q: How accurate are the recommendations?
**A**: Accuracy improves with data. Initially, content-based filtering ensures relevant suggestions. As users provide feedback, collaborative filtering learns patterns. The hybrid approach achieves balanced results. We can measure with metrics like Precision@K and NDCG (implemented in evaluation functions).

### Q: Can the system handle many users?
**A**: Yes. MongoDB supports horizontal scaling. The ML models are pre-computed (TF-IDF) so recommendations are fast (just matrix multiplication). For heavy load, we can cache recommendations or use background jobs.

### Q: What if a student hasn't set preferences?
**A**: The system uses fallback strategies: generic keywords ("computer science programming"), completed courses (from academic_data), and pure content-based recommendations. The algorithm gracefully degrades.

### Q: How do you prevent recommendation bias?
**A**: The hybrid approach balances personal preferences (content) with community ratings (collaborative). The adaptive alpha ensures we don't over-rely on one method. We also filter out already-taken courses to avoid redundancy.

### Q: Security of JWT tokens?
**A**: Tokens are signed with SECRET_KEY, expire in 24h, and are transmitted over HTTPS in production. They contain only user_id (no sensitive data). Even if intercepted, they expire quickly. We can implement refresh tokens for better UX.

### Q: What happens if ML models aren't loaded?
**A**: The API returns a 503 error with instructions to rebuild models. The system checks `is_loaded` flag before processing recommendations. This prevents crashes and guides admins to fix the issue.

---

## 📈 System Statistics

### Database Metrics
- **7 Collections**: users, courses, enrollments, feedback, preferences, academic_data, advising_sessions
- **Indexes**: 10+ for query optimization
- **Sample Size**: 50+ courses, unlimited users

### API Metrics
- **9 Blueprint Routes**: Modular API design
- **30+ Endpoints**: Comprehensive coverage
- **Authentication**: JWT on 28 endpoints
- **Response Time**: <100ms for most queries

### ML Metrics
- **TF-IDF Vocabulary**: 200+ unique terms
- **Course Matrix Shape**: (50 courses, 200 features)
- **Recommendation Time**: <1 second
- **Top-K**: Returns 10 best matches

---

## 🔮 Future Enhancements

### Technical Improvements
1. **Redis Caching**: Cache recommendations for faster responses
2. **Celery Background Jobs**: Async model rebuilding
3. **GraphQL**: More flexible API queries
4. **Elasticsearch**: Advanced course search
5. **Docker**: Containerized deployment

### ML Enhancements
1. **Deep Learning**: Neural collaborative filtering
2. **Contextual Bandits**: Real-time learning from clicks
3. **A/B Testing**: Compare recommendation algorithms
4. **Explainability**: Show why courses recommended
5. **Diversity**: Ensure varied recommendations

### Database Improvements
1. **Sharding**: Horizontal scaling for large datasets
2. **Replica Sets**: High availability
3. **Time-Series**: Track enrollment trends
4. **Aggregation Pipeline**: Advanced analytics

---

## 🎓 Conclusion

The Smart Course Recommendation System backend demonstrates:

✅ **Modern API Design** - RESTful, JWT-secured, modular  
✅ **Intelligent ML** - Hybrid recommendations with TF-IDF + collaborative filtering  
✅ **Robust Data Management** - MongoDB with proper schema and indexing  
✅ **Business Logic** - Academic rules, validation, error handling  
✅ **Scalable Architecture** - Blueprint routing, separation of concerns  
✅ **Production-Ready** - Security, error handling, health checks  

The system successfully implements a complete backend for academic course management with AI-powered recommendations, combining traditional software engineering with modern machine learning techniques.

---

## 📚 Quick Reference

### Start Backend
```bash
cd backend
python app.py
```

### Test API
```bash
# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'

# Get Recommendations
curl -X GET http://localhost:5000/recommend/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Rebuild ML Models
```bash
cd backend
python rebuild_models.py
```

### Check Database
```bash
mongosh
use fyp2
db.courses.find().pretty()
```

---

**Good luck with your FYP presentation! 🎉**
