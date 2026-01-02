class Course {
  final String id;
  final String courseCode;
  final String courseName;
  final String description;
  final int level;
  final int capacity;
  final List<String> skills;
  final int creditHours;
  final List<String> prerequisites;
  final double? score; // For recommendations
  final bool isAvailableThisSemester; // NEW: Availability status
  final String?
      semester; // NEW: Which semester it's available (e.g., "2024/2025 Sem 1")
  final String? instructor;
  final String? department;

  Course({
    required this.id,
    required this.courseCode,
    required this.courseName,
    required this.description,
    required this.level,
    required this.capacity,
    required this.skills,
    this.creditHours = 3,
    this.prerequisites = const [],
    this.score,
    this.isAvailableThisSemester = false,
    this.semester,
    this.instructor,
    this.department,
  });

  factory Course.fromJson(Map<String, dynamic> json) {
    return Course(
      id: json['_id'] ?? json['id'] ?? '',
      courseCode: json['course_code'] ?? '',
      courseName: json['course_name'] ?? '',
      description: json['description'] ?? '',
      level: json['level'] ?? 1,
      capacity: json['capacity'] ?? 30,
      skills: List<String>.from(json['skills'] ?? []),
      creditHours: json['credit_hours'] ?? 3,
      prerequisites: List<String>.from(json['prerequisites'] ?? []),
      score: json['score']?.toDouble(),
      isAvailableThisSemester: json['is_available_this_semester'] ?? false,
      semester: json['semester'],
      instructor: json['instructor'],
      department: json['department'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      '_id': id,
      'course_code': courseCode,
      'course_name': courseName,
      'description': description,
      'level': level,
      'capacity': capacity,
      'skills': skills,
      'credit_hours': creditHours,
      'prerequisites': prerequisites,
      'score': score,
      'is_available_this_semester': isAvailableThisSemester,
      'semester': semester,
      'instructor': instructor,
      'department': department,
    };
  }

  // Helper method to check if available
  bool get isAvailable => isAvailableThisSemester;

  // Helper to get display status
  String get availabilityStatus {
    if (isAvailableThisSemester) {
      return 'Available This Semester';
    } else if (semester != null && semester!.isNotEmpty) {
      return 'Available in $semester';
    } else {
      return 'Not Currently Offered';
    }
  }
}
