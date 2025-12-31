class Course {
  final String id;
  final String courseCode;
  final String courseName;
  final String description;
  final int level;
  final int capacity;
  final List<String> skills;
  final int creditHours;
  final double? score; // For recommendations

  Course({
    required this.id,
    required this.courseCode,
    required this.courseName,
    required this.description,
    required this.level,
    required this.capacity,
    required this.skills,
    this.creditHours = 3,
    this.score,
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
      score: json['score']?.toDouble(),
    );
  }
}
