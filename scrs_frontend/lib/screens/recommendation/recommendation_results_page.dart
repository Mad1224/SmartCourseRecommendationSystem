import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import '../../services/session.dart';

class RecommendationResultsPage extends StatefulWidget {
  const RecommendationResultsPage({super.key});

  @override
  State<RecommendationResultsPage> createState() =>
      _RecommendationResultsPageState();
}

class _RecommendationResultsPageState extends State<RecommendationResultsPage> {
  bool loading = true;
  List recommendations = [];

  @override
  void initState() {
    super.initState();
    fetchRecommendations();
  }

  Future<void> fetchRecommendations() async {
    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:5000/recommend/'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ${Session.token}',
        },
        body: jsonEncode({
          // TEMP: hardcoded preferences (later read from DB)
          "kulliyyah": "KOE",
          "semester": 5,
          "cgpa": 3.33,
          "preferred_course_types": ["Practical"],
          "preferred_class_time": "Morning",
          "courses_to_avoid": []
        }),
      );

      if (response.statusCode == 200) {
        setState(() {
          recommendations = jsonDecode(response.body);
          loading = false;
        });
      } else {
        debugPrint(response.body);
        throw Exception('Failed to load recommendations');
      }
    } catch (e) {
      setState(() => loading = false);
      debugPrint(e.toString());
    }
  }

  void _enrollCourse(String courseCode) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Course added'),
        content: const Text('The course has been added'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Back'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              // Later: Navigate to Current Courses page
            },
            child: const Text('Current Course'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Courses Recommended'),
      ),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: recommendations.length.clamp(0, 5),
              itemBuilder: (context, index) {
                final course = recommendations[index];

                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          course['course_name'] ?? 'Course Name',
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          course['description'] ?? 'Course description...',
                        ),
                        const SizedBox(height: 12),
                        Align(
                          alignment: Alignment.centerRight,
                          child: ElevatedButton(
                            onPressed: () =>
                                _enrollCourse(course['course_code']),
                            child: const Text('Enroll Course'),
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
