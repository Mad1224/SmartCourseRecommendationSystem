import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../profile/profile_page.dart';
import '../preferences/input_preferences_page.dart';
import '../recommendation/recommendation_results_page.dart';
import '../academic/academic_page.dart';
import '../../services/user_service.dart';
import '../../services/session.dart';
import '../../services/enrollment_service.dart';
import '../../config/api.dart';
import '../feedback/feedback_page.dart';
import '../course_catalog/course_catalog_page.dart';

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  Map<String, dynamic>? user;
  bool isLoading = true;
  List<dynamic> enrolledCourses = [];
  bool loadingEnrollments = true;
  double cgpa = 0.0;
  int currentCreditHours = 0;
  int totalCreditHours = 120;

  @override
  void initState() {
    super.initState();
    loadProfile();
    loadEnrollments();
    loadAcademicData();
  }

  Future<void> loadProfile() async {
    try {
      final data = await UserService.getProfile();
      setState(() {
        user = data;
        isLoading = false;
      });
    } catch (e) {
      setState(() => isLoading = false);
    }
  }

  Future<void> loadAcademicData() async {
    try {
      final response = await http.get(
        Uri.parse('${ApiConfig.baseUrl}/academic/'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ${Session.token}',
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          cgpa = (data['cgpa'] ?? 0.0).toDouble();

          // Calculate credit hours from courses_taken
          int completedCredits = 0;
          if (data['courses_taken'] != null) {
            for (var course in data['courses_taken']) {
              completedCredits += (course['credit_hours'] ?? 3) as int;
            }
          }
          currentCreditHours = completedCredits;
        });
      }
    } catch (e) {
      debugPrint('Error loading academic data: $e');
    }
  }

  Future<void> loadEnrollments() async {
    try {
      final enrollments = await EnrollmentService.getMyEnrollments();
      setState(() {
        enrolledCourses = enrollments;
        loadingEnrollments = false;
      });
    } catch (e) {
      setState(() => loadingEnrollments = false);
    }
  }

  Future<void> refreshData() async {
    await loadProfile();
    await loadEnrollments();
    await loadAcademicData();
  }

  Future<void> removeEnrollment(String courseId, String courseName) async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => Dialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        child: Container(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                width: 80,
                height: 80,
                decoration: BoxDecoration(
                  color: Colors.red[50],
                  shape: BoxShape.circle,
                ),
                child: Icon(
                  Icons.warning_rounded,
                  size: 50,
                  color: Colors.red[600],
                ),
              ),
              const SizedBox(height: 20),
              const Text(
                'Remove Course?',
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 12),
              Text(
                courseName,
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  color: Colors.grey[700],
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'This action cannot be undone. You will need to enroll again if you change your mind.',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey[600],
                ),
              ),
              const SizedBox(height: 24),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      onPressed: () => Navigator.pop(context, false),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      child: const Text('Cancel'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: ElevatedButton(
                      onPressed: () => Navigator.pop(context, true),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.red,
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      child: const Text('Remove'),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );

    if (confirm == true) {
      final success = await EnrollmentService.removeEnrollment(courseId);
      if (success) {
        await loadEnrollments();
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Course removed successfully')),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final userName = user?['name']?.split(' ')[0] ?? 'User';

    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: const Text('SmartCourse'),
        automaticallyImplyLeading: false,
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: refreshData,
              child: ListView(
                padding: const EdgeInsets.all(16.0),
                children: [
                  // Welcome Message
                  Text(
                    'Welcome, $userName',
                    style: const TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 20),

                  // Key Stats Card
                  Card(
                    elevation: 0,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12.0),
                      side: BorderSide(color: Colors.grey[200]!),
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          _buildStatColumn('CGPA',
                              cgpa > 0 ? cgpa.toStringAsFixed(2) : 'N/A'),
                          Container(
                              height: 40, width: 1, color: Colors.grey[200]),
                          _buildStatColumn('Credit Hours',
                              '$currentCreditHours/$totalCreditHours'),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),

                  // Refine Preferences Button
                  ElevatedButton.icon(
                    icon: const Icon(Icons.filter_list, size: 20),
                    label: const Text('Refine Preferences'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                      foregroundColor: Colors.black,
                      side: BorderSide(color: Colors.grey[300]!),
                      padding: const EdgeInsets.symmetric(vertical: 14),
                    ),
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const InputPreferencesPage(),
                        ),
                      );
                    },
                  ),
                  const SizedBox(height: 30),

                  // Quick Actions
                  const Text(
                    'Quick Actions',
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 16),

                  _ActionCard(
                    title: 'Course Recommendations',
                    subtitle: 'View personalized course suggestions',
                    icon: Icons.recommend,
                    color: Colors.blue[400]!,
                    onTap: () async {
                      await Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) =>
                              const RecommendationResultsPage(),
                        ),
                      );
                      // Refresh data when returning from recommendations
                      await loadEnrollments();
                    },
                  ),
                  _ActionCard(
                    title: 'Academic Data',
                    subtitle: 'View your academic records',
                    icon: Icons.school,
                    color: Colors.green[400]!,
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const AcademicPage(),
                        ),
                      );
                    },
                  ),
                  _ActionCard(
                    title: 'Course Feedback',
                    subtitle: 'View and submit course feedback',
                    icon: Icons.rate_review,
                    color: Colors.purple[400]!,
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const FeedbackPage(),
                        ),
                      );
                    },
                  ),
                  _ActionCard(
                    title: 'Course Catalog',
                    subtitle: 'Browse all available courses',
                    icon: Icons.book,
                    color: Colors.orange[400]!,
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const CourseCatalogPage(),
                        ),
                      );
                    },
                  ),

                  // Enrolled Courses Section
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text(
                        'My Enrolled Courses',
                        style: TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      if (enrolledCourses.isNotEmpty)
                        TextButton(
                          onPressed: () {
                            // Navigate to full enrolled courses page
                          },
                          child: const Text('View All'),
                        ),
                    ],
                  ),
                  const SizedBox(height: 12),

                  if (loadingEnrollments)
                    const Center(
                      child: Padding(
                        padding: EdgeInsets.all(20.0),
                        child: CircularProgressIndicator(),
                      ),
                    )
                  else if (enrolledCourses.isEmpty)
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(32.0),
                        child: Column(
                          children: [
                            Icon(Icons.school_outlined,
                                size: 64, color: Colors.grey[300]),
                            const SizedBox(height: 16),
                            Text(
                              'No Enrolled Courses',
                              style: TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.bold,
                                color: Colors.grey[700],
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Visit Course Recommendations to enroll in courses',
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                fontSize: 14,
                                color: Colors.grey[600],
                              ),
                            ),
                          ],
                        ),
                      ),
                    )
                  else
                    ...enrolledCourses.map((course) {
                      return Card(
                        margin: const EdgeInsets.only(bottom: 12),
                        child: ListTile(
                          contentPadding: const EdgeInsets.all(16),
                          leading: CircleAvatar(
                            backgroundColor: Colors.green[100],
                            child: Icon(Icons.check_circle,
                                color: Colors.green[700]),
                          ),
                          title: Text(
                            course['course_name'] ?? 'Course',
                            style: const TextStyle(fontWeight: FontWeight.bold),
                          ),
                          subtitle: Text(course['course_code'] ?? ''),
                          trailing: IconButton(
                            icon: const Icon(Icons.remove_circle_outline,
                                color: Colors.red),
                            onPressed: () => removeEnrollment(
                              course['course_id'],
                              course['course_name'] ?? 'this course',
                            ),
                          ),
                        ),
                      );
                    }).toList(),
                ],
              ),
            ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: 0,
        selectedItemColor: const Color(0xFF00796B),
        unselectedItemColor: Colors.grey[600],
        type: BottomNavigationBarType.fixed,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Browse'),
          BottomNavigationBarItem(
              icon: Icon(Icons.feedback_outlined), label: 'Feedback'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
        onTap: (index) {
          if (index == 1) {
            Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) => const CourseCatalogPage()));
          } else if (index == 2) {
            Navigator.push(context,
                MaterialPageRoute(builder: (context) => const FeedbackPage()));
          } else if (index == 3) {
            Navigator.push(context,
                MaterialPageRoute(builder: (context) => const ProfilePage()));
          }
        },
      ),
    );
  }

  Widget _buildStatColumn(String label, String value) {
    return Column(
      children: [
        Text(label,
            style: const TextStyle(fontSize: 14, color: Colors.black54)),
        const SizedBox(height: 4),
        Text(value,
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
      ],
    );
  }
}

class _ActionCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final IconData icon;
  final Color color;
  final VoidCallback onTap;

  const _ActionCard({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        leading: CircleAvatar(
          backgroundColor: color.withOpacity(0.1),
          child: Icon(icon, color: color),
        ),
        title: Text(title,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        subtitle: Text(subtitle),
        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
        onTap: onTap,
      ),
    );
  }
}
