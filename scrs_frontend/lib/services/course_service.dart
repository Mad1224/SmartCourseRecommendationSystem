import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api.dart';
import '../models/course.dart';
import 'session.dart';

class CourseService {
  /// Get all courses (with availability status)
  static Future<List<Course>> getAllCourses() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/courses/'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => Course.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load courses: ${response.body}');
    }
  }

  /// Get courses available this semester only
  static Future<List<Course>> getAvailableCourses() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/courses/available'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => Course.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load available courses: ${response.body}');
    }
  }

  /// Get a single course by ID
  static Future<Course> getCourseById(String courseId) async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/courses/$courseId'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return Course.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load course: ${response.body}');
    }
  }

  /// Get courses by level
  static Future<List<Course>> getCoursesByLevel(int level) async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/courses/level/$level'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => Course.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load courses: ${response.body}');
    }
  }

  /// Search courses
  static Future<List<Course>> searchCourses(String query) async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/courses/search?q=$query'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => Course.fromJson(json)).toList();
    } else {
      throw Exception('Failed to search courses: ${response.body}');
    }
  }
}
