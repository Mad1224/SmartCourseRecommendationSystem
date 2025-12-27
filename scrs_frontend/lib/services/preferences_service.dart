import 'dart:convert';
import 'package:http/http.dart' as http;
import 'session.dart';
import '../config/api.dart';

class PreferencesService {
  static Future<void> savePreferences(Map<String, dynamic> data) async {
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}/preferences/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ${Session.token}',
      },
      body: jsonEncode(data),
    );

    if (response.statusCode != 201) {
      throw Exception('Failed to save preferences');
    }
  }

  static Future<Map<String, dynamic>> getPreferences() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}/preferences/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ${Session.token}',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else if (response.statusCode == 404) {
      return {}; // No preferences set yet
    } else {
      throw Exception('Failed to load preferences');
    }
  }
}
