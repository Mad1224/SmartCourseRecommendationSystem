import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api.dart';

class AuthService {
  /// Login user
  static Future<String> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['token'];
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['msg'] ?? 'Login failed');
    }
  }

  /// Register new user
  static Future<String> register({
    required String name,
    required String email,
    required String matricNumber,
    required String password,
    required String kulliyyah,
    required String programme,
    required int year,
    String? phone,
  }) async {
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'name': name,
        'email': email,
        'matric_number': matricNumber,
        'password': password,
        'kulliyyah': kulliyyah,
        'programme': programme,
        'year': year,
        'phone': phone ?? '',
      }),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body);
      // Return token for auto-login
      return data['token'];
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['msg'] ?? 'Registration failed');
    }
  }
}
