import 'dart:convert';
import 'package:http/http.dart' as http;
import 'session.dart';

class PreferencesService {
  static Future<void> savePreferences(Map<String, dynamic> data) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:5000/preferences/'),
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
}
