import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api.dart';
import 'session.dart';

class AcademicService {
  // Save or update academic data
  static Future<Map<String, dynamic>> saveAcademicData({
    required String kulliyyah,
    required String programme,
    required int currentSemester,
    required double cgpa,
    List<Map<String, dynamic>>? coursesTaken,
  }) async {
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}/academic/'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'kulliyyah': kulliyyah,
        'programme': programme,
        'current_semester': currentSemester,
        'cgpa': cgpa,
        'courses_taken': coursesTaken ?? [],
      }),
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to save academic data: ${response.body}');
    }
  }

  // Get academic data
  static Future<Map<String, dynamic>> getAcademicData() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/academic/'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else if (response.statusCode == 404) {
      // No academic data found, return empty
      return {};
    } else {
      throw Exception('Failed to load academic data: ${response.body}');
    }
  }

  // Add a single course to transcript
  static Future<Map<String, dynamic>> addCourse({
    required String courseCode,
    required String courseName,
    required int semesterTaken,
    required String grade,
    required int creditHours,
  }) async {
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}/academic/course'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'course_code': courseCode,
        'course_name': courseName,
        'semester_taken': semesterTaken,
        'grade': grade,
        'credit_hours': creditHours,
      }),
    );

    if (response.statusCode == 201) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to add course: ${response.body}');
    }
  }

  // Update a course in transcript
  static Future<Map<String, dynamic>> updateCourse({
    required String courseCode,
    required String courseName,
    required int semesterTaken,
    required String grade,
    required int creditHours,
  }) async {
    final response = await http.put(
      Uri.parse('${ApiConfig.baseUrl}/academic/course/$courseCode'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'course_name': courseName,
        'semester_taken': semesterTaken,
        'grade': grade,
        'credit_hours': creditHours,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to update course: ${response.body}');
    }
  }

  // Delete a course from transcript
  static Future<Map<String, dynamic>> deleteCourse(String courseCode) async {
    final response = await http.delete(
      Uri.parse('${ApiConfig.baseUrl}/academic/course/$courseCode'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to delete course: ${response.body}');
    }
  }

  // Get courses by semester
  static Future<Map<String, dynamic>> getCoursesBySemester(
      int semester) async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/academic/semester/$semester'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load courses: ${response.body}');
    }
  }

  // Update CGPA
  static Future<Map<String, dynamic>> updateCGPA({
    required double cgpa,
    int? currentSemester,
  }) async {
    final Map<String, dynamic> body = {'cgpa': cgpa};
    if (currentSemester != null) {
      body['current_semester'] = currentSemester;
    }

    final response = await http.put(
      Uri.parse('${ApiConfig.baseUrl}/academic/cgpa'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode(body),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to update CGPA: ${response.body}');
    }
  }

  // Get academic statistics
  static Future<Map<String, dynamic>> getStatistics() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/academic/statistics'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load statistics: ${response.body}');
    }
  }
}
