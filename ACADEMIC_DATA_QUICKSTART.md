# Academic Data System - Quick Start Guide

## 🚀 Quick Setup

### 1. Backend is Ready
The backend routes are already integrated in [backend/app.py](backend/app.py)
- Endpoint: `/academic`
- 8 API endpoints available
- JWT authentication enabled

### 2. Frontend is Ready
- Service: [scrs_frontend/lib/services/academic_service.dart](scrs_frontend/lib/services/academic_service.dart)
- UI: [scrs_frontend/lib/screens/academic/academic_page.dart](scrs_frontend/lib/screens/academic/academic_page.dart)
- Navigation: Added to Dashboard

### 3. Test It Out

**Start Backend**:
```powershell
cd backend
python app.py
```

**Run Flutter App**:
```powershell
cd scrs_frontend
flutter run
```

**Access Academic Data**:
1. Login to the app
2. From Dashboard, click "Academic Data"
3. Fill in your information
4. Add courses using the + button

## 📋 What You Can Do

### Basic Information
- ✅ Store Kulliyyah (e.g., KICT, KENMS)
- ✅ Store Programme (e.g., Computer Science)
- ✅ Track current semester
- ✅ Record CGPA

### Course Management
- ✅ Add courses with code, name, semester, grade, credit hours
- ✅ View all courses in a list
- ✅ Delete courses
- ✅ Filter courses by semester
- ✅ View academic statistics

## 🔗 Key Files Created/Modified

### Backend:
1. **NEW**: `backend/routes/academic_routes.py` - All API endpoints
2. **MODIFIED**: `backend/app.py` - Registered academic blueprint

### Frontend:
1. **NEW**: `scrs_frontend/lib/services/academic_service.dart` - API service
2. **NEW**: `scrs_frontend/lib/screens/academic/academic_page.dart` - UI screen
3. **MODIFIED**: `scrs_frontend/lib/screens/dashboard/dashboard_page.dart` - Added navigation

## 📦 Database

Collection: `academic_data` (auto-created in MongoDB)

Sample document:
```json
{
  "user_id": "userId123",
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

## 🎯 Next Steps

1. **Test the system** - Add some sample academic data
2. **Integrate with recommendations** - Use course history to filter recommendations
3. **Add validation** - Check prerequisites based on completed courses
4. **Enhance UI** - Add charts, semester GPA, grade trends

## 💡 Usage Examples

### Adding Academic Data (Frontend):
```dart
await AcademicService.saveAcademicData(
  kulliyyah: 'KICT',
  programme: 'Computer Science',
  currentSemester: 4,
  cgpa: 3.75,
);
```

### Adding a Course (Frontend):
```dart
await AcademicService.addCourse(
  courseCode: 'INFO 4201',
  courseName: 'Database Systems',
  semesterTaken: 3,
  grade: 'A',
  creditHours: 3,
);
```

### Getting Statistics (Frontend):
```dart
final stats = await AcademicService.getStatistics();
print('Total courses: ${stats['total_courses_completed']}');
print('CGPA: ${stats['cgpa']}');
```

## 🐛 Troubleshooting

**Issue**: Academic Data button doesn't work
- **Fix**: Make sure you've saved all files and restarted the Flutter app

**Issue**: API returns 401 Unauthorized
- **Fix**: Ensure you're logged in and the JWT token is valid

**Issue**: Courses not showing up
- **Fix**: Check MongoDB connection and ensure data is being saved

## 📚 Documentation

See [ACADEMIC_DATA_DOCUMENTATION.md](ACADEMIC_DATA_DOCUMENTATION.md) for complete API reference and detailed usage guide.
