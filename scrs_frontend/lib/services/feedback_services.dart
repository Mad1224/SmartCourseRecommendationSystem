import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api.dart';
import 'session.dart';

class FeedbackService {
  /// Submit feedback for a course
  static Future<Map<String, dynamic>> submitFeedback({
    required String courseCode,
    required int rating,
    String? comment,
  }) async {
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}/feedback/'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'course_code': courseCode,
        'rating': rating,
        'comment': comment ?? '',
      }),
    );

    if (response.statusCode == 201) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to submit feedback: ${response.body}');
    }
  }

  /// Get all feedback (public view)
  static Future<List<dynamic>> getAllFeedback() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/feedback/all'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load feedback: ${response.body}');
    }
  }

  /// Get feedback for a specific course
  static Future<List<dynamic>> getCourseFeedback(String courseCode) async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/feedback/course/$courseCode'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load course feedback: ${response.body}');
    }
  }

  /// Get current user's feedback
  static Future<List<dynamic>> getMyFeedback() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/feedback/my'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load your feedback: ${response.body}');
    }
  }

  /// Delete feedback
  static Future<bool> deleteFeedback(String feedbackId) async {
    final response = await http.delete(
      Uri.parse('${ApiConfig.baseUrl}/feedback/$feedbackId'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
      },
    );

    return response.statusCode == 200;
  }

  /// Update feedback
  static Future<Map<String, dynamic>> updateFeedback({
    required String feedbackId,
    required int rating,
    String? comment,
  }) async {
    final response = await http.put(
      Uri.parse('${ApiConfig.baseUrl}/feedback/$feedbackId'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'rating': rating,
        'comment': comment ?? '',
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to update feedback: ${response.body}');
    }
  }

  /// Get courses taken (available for feedback)
  static Future<List<dynamic>> getCoursesTaken() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/feedback/courses-taken'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load courses: ${response.body}');
    }
  }
}
