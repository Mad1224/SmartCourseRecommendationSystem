import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api.dart';
import 'session.dart';

class AdvisingService {
  /// Submit an advising request
  static Future<Map<String, dynamic>> submitAdvisingRequest({
    required String advisingType,
    String? preferredLecturer,
    required String additionalNote,
  }) async {
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}/advising/request'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'advising_type': advisingType,
        'preferred_lecturer_id': preferredLecturer,
        'additional_note': additionalNote,
      }),
    );

    if (response.statusCode == 201) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to submit advising request: ${response.body}');
    }
  }

  /// Get available lecturers/advisers
  static Future<List<Map<String, dynamic>>> getAvailableLecturers() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/advising/lecturers'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((item) => item as Map<String, dynamic>).toList();
    } else {
      throw Exception('Failed to load lecturers: ${response.body}');
    }
  }

  /// Get user's advising requests
  static Future<List<Map<String, dynamic>>> getMyRequests() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/advising/my-requests'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((item) => item as Map<String, dynamic>).toList();
    } else {
      throw Exception('Failed to load requests: ${response.body}');
    }
  }

  /// Cancel an advising request
  static Future<bool> cancelRequest(String requestId) async {
    final response = await http.delete(
      Uri.parse('${ApiConfig.baseUrl}/advising/request/$requestId'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
      },
    );

    return response.statusCode == 200;
  }

  /// Get request details
  static Future<Map<String, dynamic>> getRequestDetails(
      String requestId) async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/advising/request/$requestId'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load request details: ${response.body}');
    }
  }
}
