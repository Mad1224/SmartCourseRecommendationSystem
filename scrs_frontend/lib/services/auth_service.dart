import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api.dart';

class AuthService {
  static Future<String> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['token']; // ✅ EXACT match to backend
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['msg'] ?? 'Login failed');
    }
  }
}
