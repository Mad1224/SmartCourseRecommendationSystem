# Academic Data System - Documentation

## Overview
A complete academic data management system that allows students to:
- Store their kulliyyah, programme, current semester, and CGPA
- Manage their course transcript (add, view, update, delete courses)
- View academic statistics
- Link academic data with course recommendations

## Backend API Endpoints

### Base URL: `/academic`

### 1. **Save/Update Academic Data**
- **Endpoint**: `POST /academic/`
- **Authentication**: Required (JWT Token)
- **Request Body**:
```json
{
  "kulliyyah": "KICT",
  "programme": "Computer Science",
  "current_semester": 4,
  "cgpa": 3.75,
  "courses_taken": [
    {
      "course_code": "INFO 4201",
      "course_name": "Database Systems",
      "semester_taken": 3,
      "grade": "A",
      "credit_hours": 3
    }
  ]
}
```
- **Response**: `201 Created` or `200 OK`

### 2. **Get Academic Data**
- **Endpoint**: `GET /academic/`
- **Authentication**: Required
- **Response**:
```json
{
  "user_id": "user123",
  "kulliyyah": "KICT",
  "programme": "Computer Science",
  "current_semester": 4,
  "cgpa": 3.75,
  "courses_taken": [...],
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-15T00:00:00"
}
```

### 3. **Add Single Course**
- **Endpoint**: `POST /academic/course`
- **Authentication**: Required
- **Request Body**:
```json
{
  "course_code": "INFO 4201",
  "course_name": "Database Systems",
  "semester_taken": 3,
  "grade": "A",
  "credit_hours": 3
}
```
- **Response**: `201 Created`

### 4. **Update Course**
- **Endpoint**: `PUT /academic/course/<course_code>`
- **Authentication**: Required
- **Request Body**:
```json
{
  "course_name": "Advanced Database Systems",
  "semester_taken": 3,
  "grade": "A+",
  "credit_hours": 3
}
```
- **Response**: `200 OK`

### 5. **Delete Course**
- **Endpoint**: `DELETE /academic/course/<course_code>`
- **Authentication**: Required
- **Response**: `200 OK`

### 6. **Get Courses by Semester**
- **Endpoint**: `GET /academic/semester/<semester_number>`
- **Authentication**: Required
- **Response**:
```json
{
  "semester": 3,
  "courses": [...]
}
```

### 7. **Update CGPA**
- **Endpoint**: `PUT /academic/cgpa`
- **Authentication**: Required
- **Request Body**:
```json
{
  "cgpa": 3.85,
  "current_semester": 5
}
```
- **Response**: `200 OK`

### 8. **Get Academic Statistics**
- **Endpoint**: `GET /academic/statistics`
- **Authentication**: Required
- **Response**:
```json
{
  "cgpa": 3.75,
  "current_semester": 4,
  "total_courses_completed": 25,
  "total_credit_hours": 75,
  "grade_distribution": {
    "A": 10,
    "A-": 8,
    "B+": 5,
    "B": 2
  },
  "kulliyyah": "KICT",
  "programme": "Computer Science"
}
```

## Frontend Implementation

### Service: `academic_service.dart`
Located at: `scrs_frontend/lib/services/academic_service.dart`

**Key Methods**:
- `saveAcademicData()` - Save/update complete academic data
- `getAcademicData()` - Retrieve academic data
- `addCourse()` - Add a single course
- `updateCourse()` - Update existing course
- `deleteCourse()` - Remove a course
- `getCoursesBySemester()` - Get courses for specific semester
- `updateCGPA()` - Update CGPA only
- `getStatistics()` - Get academic statistics

### UI Screen: `academic_page.dart`
Located at: `scrs_frontend/lib/screens/academic/academic_page.dart`

**Features**:
- Basic information form (Kulliyyah, Programme, Semester, CGPA)
- List of all courses taken
- Add new course dialog
- Delete course confirmation
- Save button to update basic info
- Floating action button to add courses

## Database Schema

### Collection: `academic_data`

```javascript
{
  "_id": ObjectId,
  "user_id": "string",  // JWT identity
  "kulliyyah": "string",
  "programme": "string",
  "current_semester": int,
  "cgpa": float,
  "courses_taken": [
    {
      "course_code": "string",
      "course_name": "string",
      "semester_taken": int,
      "grade": "string",
      "credit_hours": int,
      "added_at": DateTime
    }
  ],
  "created_at": DateTime,
  "updated_at": DateTime
}
```

## Usage Guide

### For Students:

1. **First Time Setup**:
   - Navigate to Dashboard → Academic Data
   - Fill in basic information (Kulliyyah, Programme, Semester, CGPA)
   - Click the save icon in the app bar

2. **Adding Courses**:
   - Click the floating + button
   - Enter course details (code, name, semester, grade, credit hours)
   - Click "Add"

3. **Managing Courses**:
   - View all courses in a scrollable list
   - Delete courses by clicking the red trash icon
   - Courses are organized by the order they were added

4. **Updating Information**:
   - Edit any basic info fields
   - Click the save icon to update
   - Add or remove courses as needed

### For Developers:

1. **Backend Setup**:
   - The academic routes are already registered in `app.py`
   - MongoDB collection `academic_data` is automatically created
   - All endpoints are protected with JWT authentication

2. **Frontend Integration**:
   - Import the service: `import '../../services/academic_service.dart';`
   - Use async/await for all service calls
   - Handle errors with try-catch blocks
   - Display loading states and error messages

3. **Testing**:
   - Start the Flask backend: `python backend/app.py`
   - Run the Flutter app: `flutter run`
   - Login with valid credentials
   - Navigate to Academic Data page

## Integration with Course Recommendations

The academic data can be used to:
- Filter recommendations based on completed courses
- Suggest courses appropriate for current semester
- Consider CGPA for prerequisite checking
- Avoid recommending already taken courses
- Personalize based on grade patterns

## Error Handling

### Backend:
- Returns appropriate HTTP status codes (400, 404, 500)
- Provides descriptive error messages in JSON format
- Validates required fields before processing

### Frontend:
- Shows SnackBar messages for success/error states
- Displays loading indicators during API calls
- Handles 404 gracefully (no data found)
- Form validation before submission

## Security

- All endpoints require JWT authentication
- User can only access their own academic data
- MongoDB user_id is linked to JWT identity
- No data exposure to other users

## Future Enhancements

Potential improvements:
- Export transcript as PDF
- Semester-wise GPA calculation
- Grade point calculations
- Visual analytics (charts/graphs)
- Bulk course import from CSV
- Course prerequisite validation
- Academic advisor recommendations based on transcript
