import 'package:flutter/material.dart';
import '../profile/profile_page.dart';
import '../preferences/input_preferences_page.dart';
import '../recommendation/recommendation_results_page.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F5F5),
      body: SafeArea(
        child: Column(
          children: [
            // ===== HEADER =====
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  // Profile icon (NOT clickable)
                  const CircleAvatar(
                    radius: 22,
                    backgroundColor: Colors.grey,
                    child: Icon(Icons.person, color: Colors.white),
                  ),

                  const Spacer(),

                  // Title + welcome
                  Column(
                    children: const [
                      Text(
                        'Smart Course\nRecommendation System',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      SizedBox(height: 4),
                      Text(
                        'Welcome, USER',
                        style: TextStyle(color: Colors.grey),
                      ),
                    ],
                  ),

                  const Spacer(),

                  // Settings button (clickable)
                  IconButton(
                    icon: const Icon(Icons.settings),
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const ProfilePage(),
                        ),
                      );
                    },
                  ),
                ],
              ),
            ),

            const SizedBox(height: 12),

            // ===== BUTTON CONTAINER =====
            Expanded(
              child: Container(
                margin: const EdgeInsets.symmetric(horizontal: 16),
                padding: const EdgeInsets.symmetric(vertical: 20),
                decoration: BoxDecoration(
                  color: Colors.grey.shade300,
                  borderRadius: BorderRadius.circular(24),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _menuButton(context, 'Input Personalization'),
                    _menuButton(context, 'Course Recommended'),
                    _menuButton(context, 'Course Catalog'),
                    _menuButton(context, 'Academic Data'),
                    _menuButton(context, 'Feedback'),
                    _menuButton(context, 'Request Academic Advisor'),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 16),

            // ===== LOGOUT =====
            Padding(
              padding: const EdgeInsets.all(16),
              child: SizedBox(
                width: double.infinity,
                height: 48,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.red,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(24),
                    ),
                  ),
                  onPressed: () {
                    Navigator.pushReplacementNamed(context, '/');
                  },
                  child: const Text('Logout'),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _menuButton(BuildContext context, String title) {
    return SizedBox(
      width: 260,
      height: 48,
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.grey.shade200,
          foregroundColor: Colors.black87,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(24),
          ),
          elevation: 0,
        ),
        onPressed: () {
          if (title == 'Input Personalization' ||
              title == 'Input Preferences') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => const InputPreferencesPage(),
              ),
            );
          }
          if (title == 'Course Recommendation' ||
              title == 'Course Recommended') {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => const RecommendationResultsPage(),
              ),
            );
          }
        },
        child: Text(title),
      ),
    );
  }
}
