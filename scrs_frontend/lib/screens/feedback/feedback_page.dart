import 'package:flutter/material.dart';
import '../../services/feedback_services.dart';
import '../dashboard/dashboard_page.dart';
import '../course_catalog/course_catalog_page.dart';
import '../profile/profile_page.dart';

class FeedbackPage extends StatefulWidget {
  const FeedbackPage({super.key});

  @override
  State<FeedbackPage> createState() => _FeedbackPageState();
}

class _FeedbackPageState extends State<FeedbackPage>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  bool isLoadingFeedback = true;
  bool isLoadingCourses = true;
  bool isLoadingMyFeedback = true;

  List<dynamic> allFeedback = [];
  List<dynamic> coursesTaken = [];
  List<dynamic> myFeedback = [];

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
    _tabController = TabController(length: 3, vsync: this);
    loadFeedback();
    loadCoursesTaken();
    loadMyFeedback();
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

  Future<void> loadCoursesTaken() async {
    setState(() => isLoadingCourses = true);
    try {
      final courses = await FeedbackService.getCoursesTaken();
      setState(() {
        coursesTaken = courses;
        isLoadingCourses = false;
      });
    } catch (e) {
      setState(() => isLoadingCourses = false);
    }
  }

  Future<void> loadMyFeedback() async {
    setState(() => isLoadingMyFeedback = true);
    try {
      final feedback = await FeedbackService.getMyFeedback();
      setState(() {
        myFeedback = feedback;
        isLoadingMyFeedback = false;
      });
    } catch (e) {
      setState(() => isLoadingMyFeedback = false);
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
            Tab(text: 'My Feedback'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildViewFeedbackTab(),
          _buildGiveFeedbackTab(),
          _buildMyFeedbackTab(),
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
    return isLoadingCourses
        ? const Center(child: CircularProgressIndicator())
        : coursesTaken.isEmpty
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
                        'No Completed Courses',
                        style: TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.bold,
                            color: Colors.grey[700]),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Complete courses to provide feedback',
                        textAlign: TextAlign.center,
                        style: TextStyle(fontSize: 14, color: Colors.grey[600]),
                      ),
                    ],
                  ),
                ),
              )
            : ListView.builder(
                padding: const EdgeInsets.all(16),
                itemCount: coursesTaken.length,
                itemBuilder: (context, index) {
                  final course = coursesTaken[index];
                  return Container(
                    margin: const EdgeInsets.only(bottom: 16),
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [
                          const Color(0xFF00796B).withOpacity(0.05),
                          Colors.white,
                        ],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(
                        color: const Color(0xFF00796B).withOpacity(0.2),
                        width: 1,
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.grey.withOpacity(0.1),
                          spreadRadius: 1,
                          blurRadius: 4,
                          offset: const Offset(0, 2),
                        ),
                      ],
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Row(
                        children: [
                          Container(
                            width: 56,
                            height: 56,
                            decoration: BoxDecoration(
                              gradient: const LinearGradient(
                                colors: [Color(0xFF00796B), Color(0xFF009688)],
                                begin: Alignment.topLeft,
                                end: Alignment.bottomRight,
                              ),
                              borderRadius: BorderRadius.circular(12),
                              boxShadow: [
                                BoxShadow(
                                  color: const Color(0xFF00796B).withOpacity(0.3),
                                  spreadRadius: 1,
                                  blurRadius: 6,
                                  offset: const Offset(0, 3),
                                ),
                              ],
                            ),
                            child: const Icon(
                              Icons.book_rounded,
                              color: Colors.white,
                              size: 28,
                            ),
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  course['course_name'] ?? 'Course',
                                  style: const TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 16,
                                    color: Color(0xFF212121),
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  course['course_code'] ?? '',
                                  style: TextStyle(
                                    fontSize: 13,
                                    color: Colors.grey[600],
                                    fontWeight: FontWeight.w500,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          const SizedBox(width: 12),
                          Container(
                            decoration: BoxDecoration(
                              gradient: const LinearGradient(
                                colors: [Color(0xFF00796B), Color(0xFF009688)],
                                begin: Alignment.topLeft,
                                end: Alignment.bottomRight,
                              ),
                              borderRadius: BorderRadius.circular(12),
                              boxShadow: [
                                BoxShadow(
                                  color: const Color(0xFF00796B).withOpacity(0.4),
                                  spreadRadius: 0,
                                  blurRadius: 8,
                                  offset: const Offset(0, 4),
                                ),
                              ],
                            ),
                            child: Material(
                              color: Colors.transparent,
                              child: InkWell(
                                borderRadius: BorderRadius.circular(12),
                                onTap: () => _showFeedbackDialog(course),
                                child: Padding(
                                  padding: const EdgeInsets.symmetric(
                                    horizontal: 20,
                                    vertical: 12,
                                  ),
                                  child: Row(
                                    mainAxisSize: MainAxisSize.min,
                                    children: const [
                                      Icon(
                                        Icons.rate_review_rounded,
                                        color: Colors.white,
                                        size: 18,
                                      ),
                                      SizedBox(width: 8),
                                      Text(
                                        'Review',
                                        style: TextStyle(
                                          color: Colors.white,
                                          fontWeight: FontWeight.bold,
                                          fontSize: 14,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                          ),
                        ],
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
                    loadFeedback(); // Refresh all feedback
                    loadMyFeedback(); // Refresh my feedback
                    loadCoursesTaken(); // Refresh courses taken list
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

  // ==================== MY FEEDBACK TAB ====================
  Widget _buildMyFeedbackTab() {
    // Filter out feedback with no course name or "Course" as name
    final validFeedback = myFeedback.where((fb) {
      final name = fb['course_name'] ?? '';
      return name.isNotEmpty && name != 'Course';
    }).toList();

    return isLoadingMyFeedback
        ? const Center(child: CircularProgressIndicator())
        : RefreshIndicator(
                onRefresh: loadMyFeedback,
                child: validFeedback.isEmpty
                    ? ListView(
                        children: const [
                          SizedBox(height: 200),
                        ],
                      )
                    : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: validFeedback.length,
                  itemBuilder: (context, index) {
                    final feedback = validFeedback[index];
                    final courseCode = feedback['course_code'] ?? 'UNKNOWN';
                    final courseName = feedback['course_name'] ?? '';
                    final rating = feedback['rating'] ?? 0;
                    final comment = feedback['comment'] ?? '';
                    final timestamp = feedback['created_at'] ?? '';

                    return Card(
                      margin: const EdgeInsets.only(bottom: 12),
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        courseName,
                                        style: const TextStyle(
                                          fontWeight: FontWeight.bold,
                                          fontSize: 16,
                                        ),
                                      ),
                                      const SizedBox(height: 4),
                                      Text(
                                        courseCode,
                                        style: TextStyle(
                                          fontSize: 14,
                                          color: Colors.grey[600],
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                                IconButton(
                                  icon: const Icon(Icons.delete,
                                      color: Colors.red),
                                  onPressed: () =>
                                      _confirmDeleteFeedback(feedback),
                                ),
                              ],
                            ),
                            const SizedBox(height: 12),
                            Row(
                              children: List.generate(5, (starIndex) {
                                return Icon(
                                  starIndex < rating
                                      ? Icons.star
                                      : Icons.star_border,
                                  size: 20,
                                  color: Colors.amber,
                                );
                              }),
                            ),
                            if (comment.isNotEmpty) ...[
                              const SizedBox(height: 12),
                              Text(
                                comment,
                                style: TextStyle(
                                  fontSize: 14,
                                  color: Colors.grey[700],
                                  height: 1.4,
                                ),
                              ),
                            ],
                            const SizedBox(height: 8),
                            Text(
                              _formatTimestamp(timestamp),
                              style: TextStyle(
                                fontSize: 12,
                                color: Colors.grey[500],
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

  void _confirmDeleteFeedback(Map<String, dynamic> feedback) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Feedback'),
        content: const Text(
          'Are you sure you want to delete this feedback? This action cannot be undone.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              Navigator.pop(context);
              await _deleteFeedback(feedback['_id']);
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
            ),
            child: const Text('Delete'),
          ),
        ],
      ),
    );
  }

  Future<void> _deleteFeedback(String feedbackId) async {
    try {
      await FeedbackService.deleteFeedback(feedbackId);

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Feedback deleted successfully')),
        );
        // Refresh all feedback lists
        loadMyFeedback();
        loadFeedback();
        loadCoursesTaken(); // Refresh Give Feedback tab
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error deleting feedback: $e')),
        );
      }
    }
  }
}
