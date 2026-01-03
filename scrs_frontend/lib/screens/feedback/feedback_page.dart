import 'package:flutter/material.dart';
import '../../services/feedback_services.dart';
import '../../services/enrollment_service.dart';

class FeedbackPage extends StatefulWidget {
  const FeedbackPage({super.key});

  @override
  State<FeedbackPage> createState() => _FeedbackPageState();
}

class _FeedbackPageState extends State<FeedbackPage>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  bool isLoadingFeedback = true;
  bool isLoadingEnrolled = true;

  List<dynamic> allFeedback = [];
  List<dynamic> enrolledCourses = [];

  String selectedFilter = 'All';
  final List<String> filters = [
    'All',
    'Top Rating',
    'Top IT Course',
    'Top CS Course',
    'Best Review'
  ];

  TextEditingController searchController = TextEditingController();
  String searchQuery = '';

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    loadFeedback();
    loadEnrolledCourses();
  }

  @override
  void dispose() {
    _tabController.dispose();
    searchController.dispose();
    super.dispose();
  }

  Future<void> loadFeedback() async {
    setState(() => isLoadingFeedback = true);
    try {
      final feedback = await FeedbackService.getAllFeedback();
      setState(() {
        allFeedback = feedback;
        isLoadingFeedback = false;
      });
    } catch (e) {
      setState(() => isLoadingFeedback = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading feedback: $e')),
        );
      }
    }
  }

  Future<void> loadEnrolledCourses() async {
    setState(() => isLoadingEnrolled = true);
    try {
      final courses = await EnrollmentService.getMyEnrollments();
      setState(() {
        enrolledCourses = courses;
        isLoadingEnrolled = false;
      });
    } catch (e) {
      setState(() => isLoadingEnrolled = false);
    }
  }

  List<dynamic> getFilteredFeedback() {
    List<dynamic> filtered = allFeedback;

    // Search filter
    if (searchQuery.isNotEmpty) {
      filtered = filtered.where((fb) {
        final courseName = fb['course_name']?.toString().toLowerCase() ?? '';
        final courseCode = fb['course_code']?.toString().toLowerCase() ?? '';
        final userName = fb['user_name']?.toString().toLowerCase() ?? '';
        final query = searchQuery.toLowerCase();
        return courseName.contains(query) ||
            courseCode.contains(query) ||
            userName.contains(query);
      }).toList();
    }

    // Category filter
    if (selectedFilter == 'Top Rating') {
      filtered.sort((a, b) => (b['rating'] ?? 0).compareTo(a['rating'] ?? 0));
      filtered = filtered.take(10).toList();
    } else if (selectedFilter == 'Top IT Course') {
      filtered = filtered.where((fb) {
        final code = fb['course_code']?.toString() ?? '';
        return code.startsWith('INFO');
      }).toList();
    } else if (selectedFilter == 'Top CS Course') {
      filtered = filtered.where((fb) {
        final code = fb['course_code']?.toString() ?? '';
        return code.startsWith('CSCI');
      }).toList();
    } else if (selectedFilter == 'Best Review') {
      filtered = filtered.where((fb) => (fb['rating'] ?? 0) >= 4).toList();
    }

    return filtered;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: const Text('Course Feedback'),
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: const Color(0xFF00796B),
          labelColor: Colors.black,
          unselectedLabelColor: Colors.grey,
          tabs: const [
            Tab(text: 'View Feedback'),
            Tab(text: 'Give Feedback'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildViewFeedbackTab(),
          _buildGiveFeedbackTab(),
        ],
      ),
    );
  }

  // ==================== VIEW FEEDBACK TAB ====================
  Widget _buildViewFeedbackTab() {
    return Column(
      children: [
        // Search Bar
        Container(
          padding: const EdgeInsets.all(16),
          color: Colors.white,
          child: TextField(
            controller: searchController,
            decoration: InputDecoration(
              hintText: 'Search courses',
              prefixIcon: const Icon(Icons.search),
              suffixIcon: searchQuery.isNotEmpty
                  ? IconButton(
                      icon: const Icon(Icons.clear),
                      onPressed: () {
                        setState(() {
                          searchController.clear();
                          searchQuery = '';
                        });
                      },
                    )
                  : null,
              filled: true,
              fillColor: Colors.grey[200],
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(30),
                borderSide: BorderSide.none,
              ),
              contentPadding:
                  const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
            ),
            onChanged: (value) {
              setState(() {
                searchQuery = value;
              });
            },
          ),
        ),

        // Filter Chips
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          color: Colors.white,
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: filters.map((filter) {
                final isSelected = selectedFilter == filter;
                return Padding(
                  padding: const EdgeInsets.only(right: 8),
                  child: FilterChip(
                    label: Text(filter),
                    selected: isSelected,
                    onSelected: (selected) {
                      setState(() {
                        selectedFilter = selected ? filter : 'All';
                      });
                    },
                    selectedColor: const Color(0xFF00796B).withOpacity(0.2),
                    checkmarkColor: const Color(0xFF00796B),
                    labelStyle: TextStyle(
                      color: isSelected
                          ? const Color(0xFF00796B)
                          : Colors.grey[700],
                      fontWeight:
                          isSelected ? FontWeight.bold : FontWeight.normal,
                    ),
                  ),
                );
              }).toList(),
            ),
          ),
        ),

        // Feedback List
        Expanded(
          child: isLoadingFeedback
              ? const Center(child: CircularProgressIndicator())
              : RefreshIndicator(
                  onRefresh: loadFeedback,
                  child: _buildFeedbackList(),
                ),
        ),
      ],
    );
  }

  Widget _buildFeedbackList() {
    final filteredFeedback = getFilteredFeedback();

    if (filteredFeedback.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.feedback_outlined, size: 64, color: Colors.grey[300]),
            const SizedBox(height: 16),
            Text(
              searchQuery.isNotEmpty ? 'No feedback found' : 'No feedback yet',
              style: TextStyle(fontSize: 18, color: Colors.grey[600]),
            ),
            const SizedBox(height: 8),
            Text(
              searchQuery.isNotEmpty
                  ? 'Try a different search'
                  : 'Be the first to leave feedback!',
              style: TextStyle(fontSize: 14, color: Colors.grey[500]),
            ),
          ],
        ),
      );
    }

    // Group feedback by course
    Map<String, List<dynamic>> feedbackByCourse = {};
    for (var fb in filteredFeedback) {
      final courseCode = fb['course_code'] ?? 'UNKNOWN';
      if (!feedbackByCourse.containsKey(courseCode)) {
        feedbackByCourse[courseCode] = [];
      }
      feedbackByCourse[courseCode]!.add(fb);
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: feedbackByCourse.length,
      itemBuilder: (context, index) {
        final courseCode = feedbackByCourse.keys.elementAt(index);
        final courseFeedback = feedbackByCourse[courseCode]!;
        final firstFeedback = courseFeedback.first;

        // Calculate average rating
        final avgRating = courseFeedback.fold<double>(
                0, (sum, fb) => sum + (fb['rating'] ?? 0)) /
            courseFeedback.length;

        return Card(
          margin: const EdgeInsets.only(bottom: 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Course Header
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFF00796B).withOpacity(0.1),
                  borderRadius: const BorderRadius.only(
                    topLeft: Radius.circular(12),
                    topRight: Radius.circular(12),
                  ),
                ),
                child: Row(
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            courseCode,
                            style: const TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              color: Color(0xFF00796B),
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            firstFeedback['course_name'] ?? 'Course',
                            style: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(
                        color: Colors.amber[100],
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.star, size: 16, color: Colors.amber),
                          const SizedBox(width: 4),
                          Text(
                            avgRating.toStringAsFixed(1),
                            style: const TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 14,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              // Feedback Items
              ...courseFeedback.take(3).map((fb) => _buildFeedbackItem(fb)),

              // Show more button
              if (courseFeedback.length > 3)
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Center(
                    child: TextButton.icon(
                      onPressed: () {
                        _showAllCourseFeedback(courseCode, courseFeedback);
                      },
                      icon: const Icon(Icons.expand_more),
                      label: Text('Show ${courseFeedback.length - 3} more'),
                    ),
                  ),
                ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildFeedbackItem(Map<String, dynamic> feedback) {
    final userName = feedback['user_name'] ?? 'Anonymous';
    final rating = feedback['rating'] ?? 0;
    final comment = feedback['comment'] ?? '';
    final timestamp = feedback['created_at'] ?? '';
    final likes = feedback['likes'] ?? 0;

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        border: Border(
          top: BorderSide(color: Colors.grey[200]!),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              CircleAvatar(
                backgroundColor: const Color(0xFF00796B),
                child: Text(
                  userName[0].toUpperCase(),
                  style: const TextStyle(
                      color: Colors.white, fontWeight: FontWeight.bold),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      userName,
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Row(
                      children: List.generate(5, (index) {
                        return Icon(
                          index < rating ? Icons.star : Icons.star_border,
                          size: 16,
                          color: Colors.amber,
                        );
                      }),
                    ),
                  ],
                ),
              ),
              Text(
                _formatTimestamp(timestamp),
                style: TextStyle(fontSize: 12, color: Colors.grey[600]),
              ),
            ],
          ),
          if (comment.isNotEmpty) ...[
            const SizedBox(height: 12),
            Text(
              comment,
              style:
                  TextStyle(fontSize: 14, color: Colors.grey[700], height: 1.4),
            ),
          ],
          const SizedBox(height: 8),
          Row(
            children: [
              Icon(Icons.favorite_border, size: 18, color: Colors.grey[600]),
              const SizedBox(width: 4),
              Text(
                likes.toString(),
                style: TextStyle(fontSize: 12, color: Colors.grey[600]),
              ),
            ],
          ),
        ],
      ),
    );
  }

  void _showAllCourseFeedback(String courseCode, List<dynamic> feedback) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.9,
        minChildSize: 0.5,
        maxChildSize: 0.95,
        builder: (_, controller) => Container(
          decoration: const BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.only(
              topLeft: Radius.circular(20),
              topRight: Radius.circular(20),
            ),
          ),
          child: Column(
            children: [
              const SizedBox(height: 12),
              Container(
                width: 40,
                height: 4,
                decoration: BoxDecoration(
                  color: Colors.grey[300],
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
              const SizedBox(height: 16),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Text(
                  '$courseCode - All Feedback',
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Expanded(
                child: ListView.separated(
                  controller: controller,
                  padding: const EdgeInsets.all(16),
                  itemCount: feedback.length,
                  separatorBuilder: (_, __) => const Divider(),
                  itemBuilder: (_, index) =>
                      _buildFeedbackItem(feedback[index]),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // ==================== GIVE FEEDBACK TAB ====================
  Widget _buildGiveFeedbackTab() {
    return isLoadingEnrolled
        ? const Center(child: CircularProgressIndicator())
        : enrolledCourses.isEmpty
            ? Center(
                child: Padding(
                  padding: const EdgeInsets.all(32),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.school_outlined,
                          size: 64, color: Colors.grey[300]),
                      const SizedBox(height: 16),
                      Text(
                        'No Enrolled Courses',
                        style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: Colors.grey[700]),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Enroll in courses to provide feedback',
                        textAlign: TextAlign.center,
                        style: TextStyle(fontSize: 14, color: Colors.grey[600]),
                      ),
                    ],
                  ),
                ),
              )
            : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: enrolledCourses.length,
                itemBuilder: (context, index) {
                  final course = enrolledCourses[index];
                  return Card(
                    margin: const EdgeInsets.only(bottom: 12),
                    child: ListTile(
                      contentPadding: const EdgeInsets.all(16),
                      leading: CircleAvatar(
                        backgroundColor:
                            const Color(0xFF00796B).withOpacity(0.1),
                        child: const Icon(Icons.book, color: Color(0xFF00796B)),
                      ),
                      title: Text(
                        course['course_name'] ?? 'Course',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      subtitle: Text(course['course_code'] ?? ''),
                      trailing: ElevatedButton(
                        onPressed: () => _showFeedbackDialog(course),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF00796B),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                        child: const Text('Add Feedback'),
                      ),
                    ),
                  );
                },
              );
  }

  void _showFeedbackDialog(Map<String, dynamic> course) {
    int rating = 5;
    final commentController = TextEditingController();

    showDialog(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          title: Text('Feedback for ${course['course_code']}'),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  course['course_name'] ?? 'Course',
                  style: TextStyle(fontSize: 14, color: Colors.grey[700]),
                ),
                const SizedBox(height: 20),
                const Text('Rating',
                    style: TextStyle(fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: List.generate(5, (index) {
                    return IconButton(
                      icon: Icon(
                        index < rating ? Icons.star : Icons.star_border,
                        size: 36,
                        color: Colors.amber,
                      ),
                      onPressed: () {
                        setDialogState(() {
                          rating = index + 1;
                        });
                      },
                    );
                  }),
                ),
                const SizedBox(height: 16),
                const Text('Comment (Optional)',
                    style: TextStyle(fontWeight: FontWeight.bold)),
                const SizedBox(height: 8),
                TextField(
                  controller: commentController,
                  maxLines: 4,
                  decoration: InputDecoration(
                    hintText: 'Share your experience with this course...',
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () async {
                try {
                  await FeedbackService.submitFeedback(
                    courseCode: course['course_code'],
                    rating: rating,
                    comment: commentController.text.trim(),
                  );

                  if (mounted) {
                    Navigator.pop(context);
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                          content: Text('Feedback submitted successfully!')),
                    );
                    loadFeedback(); // Refresh feedback list
                  }
                } catch (e) {
                  if (mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Error: $e')),
                    );
                  }
                }
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF00796B),
              ),
              child: const Text('Submit'),
            ),
          ],
        ),
      ),
    );
  }

  String _formatTimestamp(String timestamp) {
    try {
      final date = DateTime.parse(timestamp);
      final now = DateTime.now();
      final difference = now.difference(date);

      if (difference.inDays > 7) {
        return '${difference.inDays ~/ 7} weeks ago';
      } else if (difference.inDays > 0) {
        return '${difference.inDays} days ago';
      } else if (difference.inHours > 0) {
        return '${difference.inHours} hours ago';
      } else {
        return 'Just now';
      }
    } catch (e) {
      return '';
    }
  }
}
