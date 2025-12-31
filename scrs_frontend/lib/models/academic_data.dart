class AcademicData {
  final String userId;
  final String kulliyyah;
  final String programme;
  final int currentSemester;
  final double cgpa;
  final List<CourseRecord> coursesTaken;

  AcademicData({
    required this.userId,
    required this.kulliyyah,
    required this.programme,
    required this.currentSemester,
    required this.cgpa,
    required this.coursesTaken,
  });

  factory AcademicData.fromJson(Map<String, dynamic> json) {
    return AcademicData(
      userId: json['user_id'] ?? '',
      kulliyyah: json['kulliyyah'] ?? '',
      programme: json['programme'] ?? '',
      currentSemester: json['current_semester'] ?? 1,
      cgpa: (json['cgpa'] ?? 0.0).toDouble(),
      coursesTaken: (json['courses_taken'] as List?)
              ?.map((c) => CourseRecord.fromJson(c))
              .toList() ??
          [],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'user_id': userId,
      'kulliyyah': kulliyyah,
      'programme': programme,
      'current_semester': currentSemester,
      'cgpa': cgpa,
      'courses_taken': coursesTaken.map((c) => c.toJson()).toList(),
    };
  }
}

class CourseRecord {
  final String courseCode;
  final String courseName;
  final int semesterTaken;
  final String grade;
  final int creditHours;

  CourseRecord({
    required this.courseCode,
    required this.courseName,
    required this.semesterTaken,
    required this.grade,
    required this.creditHours,
  });

  factory CourseRecord.fromJson(Map<String, dynamic> json) {
    return CourseRecord(
      courseCode: json['course_code'] ?? '',
      courseName: json['course_name'] ?? '',
      semesterTaken: json['semester_taken'] ?? 1,
      grade: json['grade'] ?? 'N/A',
      creditHours: json['credit_hours'] ?? 3,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'course_code': courseCode,
      'course_name': courseName,
      'semester_taken': semesterTaken,
      'grade': grade,
      'credit_hours': creditHours,
    };
  }
}
