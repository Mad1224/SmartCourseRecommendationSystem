import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api.dart';
import 'session.dart';

class UserService {
  static Future<Map<String, dynamic>> getProfile() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/auth/me'),
      headers: {
        'Authorization': 'Bearer ${Session.token}',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to load profile');
    }
  }
}
