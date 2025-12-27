import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api.dart';
import 'session.dart';

class EnrollmentService {
  static Future<Map<String, dynamic>> enrollCourse(String courseId) async {
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}/enroll'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ${Session.token}',
      },
      body: jsonEncode({'course_id': courseId}),
    );

    if (response.statusCode == 201) {
      return {'success': true, 'message': 'Enrollment successful'};
    } else if (response.statusCode == 400) {
      return {'success': false, 'message': 'Already enrolled'};
    } else if (response.statusCode == 409) {
      return {'success': false, 'message': 'Course is full'};
    } else {
      return {'success': false, 'message': 'Enrollment failed'};
    }
  }

  static Future<List<dynamic>> getMyEnrollments() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/enroll/my'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ${Session.token}',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return [];
  }

  static Future<bool> removeEnrollment(String courseId) async {
    final response = await http.delete(
      Uri.parse('${ApiConfig.baseUrl}/enroll/$courseId'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ${Session.token}',
      },
    );

    return response.statusCode == 200;
  }
}
