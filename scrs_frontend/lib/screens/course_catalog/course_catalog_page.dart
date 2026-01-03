import 'package:flutter/material.dart';
import '../../services/course_service.dart';
import '../../models/course.dart';

class CourseCatalogPage extends StatefulWidget {
  const CourseCatalogPage({super.key});

  @override
  State<CourseCatalogPage> createState() => _CourseCatalogPageState();
}

class _CourseCatalogPageState extends State<CourseCatalogPage> {
  bool isLoading = true;
  List<Course> allCourses = [];
  List<Course> filteredCourses = [];

  String searchQuery = '';
  String selectedSpecialization = 'All';
  String selectedLevel = 'All';
  bool showOnlyAvailable = false;

  final TextEditingController searchController = TextEditingController();

  // Specializations extracted from course codes
  final List<String> specializations = [
    'All',
    'Data Science',
    'Network & CyberSecurity',
    'Software Engineering',
    'AI & Machine Learning',
    'Web & Mobile Development',
  ];

  final List<String> levels = [
    'All',
    'Level 1',
    'Level 2',
    'Level 3',
    'Level 4'
  ];

  @override
  void initState() {
    super.initState();
    loadCourses();
  }

  @override
  void dispose() {
    searchController.dispose();
    super.dispose();
  }

  Future<void> loadCourses() async {
    setState(() => isLoading = true);
    try {
      final courses = await CourseService.getAllCourses();
      setState(() {
        allCourses = courses;
        filteredCourses = courses;
        isLoading = false;
      });
    } catch (e) {
      setState(() => isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading courses: $e')),
        );
      }
    }
  }

  void filterCourses() {
    setState(() {
      filteredCourses = allCourses.where((course) {
        // Search filter
        if (searchQuery.isNotEmpty) {
          final searchLower = searchQuery.toLowerCase();
          final matchesSearch = course.courseName
                  .toLowerCase()
                  .contains(searchLower) ||
              course.courseCode.toLowerCase().contains(searchLower) ||
              course.description.toLowerCase().contains(searchLower) ||
              course.skills
                  .any((skill) => skill.toLowerCase().contains(searchLower));

          if (!matchesSearch) return false;
        }

        // Specialization filter
        if (selectedSpecialization != 'All') {
          bool matchesSpec = false;
          switch (selectedSpecialization) {
            case 'Data Science':
              matchesSpec = course.courseCode.contains('CSCI42') ||
                  course.courseCode.contains('CSCI45') ||
                  course.courseName.toLowerCase().contains('data');
              break;
            case 'Network & CyberSecurity':
              matchesSpec = course.courseCode.contains('CSCI43') ||
                  course.courseName.toLowerCase().contains('network') ||
                  course.courseName.toLowerCase().contains('security');
              break;
            case 'Software Engineering':
              matchesSpec = course.courseCode.contains('CSCI33') ||
                  course.courseName.toLowerCase().contains('software');
              break;
            case 'AI & Machine Learning':
              matchesSpec = course.courseCode.contains('CSCI41') ||
                  course.courseName.toLowerCase().contains('intelligence') ||
                  course.courseName.toLowerCase().contains('machine learning');
              break;
            case 'Web & Mobile Development':
              matchesSpec = course.courseCode.contains('CSCI31') ||
                  course.courseCode.contains('CSCI32') ||
                  course.courseName.toLowerCase().contains('web') ||
                  course.courseName.toLowerCase().contains('mobile');
              break;
          }
          if (!matchesSpec) return false;
        }

        // Level filter
        if (selectedLevel != 'All') {
          final levelNum = int.parse(selectedLevel.split(' ')[1]);
          if (course.level != levelNum) return false;
        }

        // Availability filter
        if (showOnlyAvailable && !course.isAvailableThisSemester) {
          return false;
        }

        return true;
      }).toList();

      // Sort: Available courses first, then by level, then by code
      filteredCourses.sort((a, b) {
        if (a.isAvailableThisSemester != b.isAvailableThisSemester) {
          return a.isAvailableThisSemester ? -1 : 1;
        }
        if (a.level != b.level) {
          return a.level.compareTo(b.level);
        }
        return a.courseCode.compareTo(b.courseCode);
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: const Text('Course Catalog'),
        actions: [
          IconButton(
            icon: const Icon(Icons.filter_list),
            onPressed: _showFilterBottomSheet,
            tooltip: 'Filters',
          ),
        ],
      ),
      body: Column(
        children: [
          // Search Bar
          Container(
            padding: const EdgeInsets.all(16),
            color: Colors.white,
            child: TextField(
              controller: searchController,
              decoration: InputDecoration(
                hintText: 'Search courses...',
                prefixIcon: const Icon(Icons.search, color: Color(0xFF00796B)),
                suffixIcon: searchQuery.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear),
                        onPressed: () {
                          searchController.clear();
                          setState(() {
                            searchQuery = '';
                            filterCourses();
                          });
                        },
                      )
                    : null,
                filled: true,
                fillColor: Colors.grey[100],
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
                  filterCourses();
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
                children: [
                  // Available This Semester Toggle
                  FilterChip(
                    label: const Text('Available This Semester'),
                    selected: showOnlyAvailable,
                    onSelected: (selected) {
                      setState(() {
                        showOnlyAvailable = selected;
                        filterCourses();
                      });
                    },
                    selectedColor: Colors.green[100],
                    checkmarkColor: Colors.green[700],
                    avatar: showOnlyAvailable
                        ? const Icon(Icons.check_circle,
                            size: 18, color: Colors.green)
                        : null,
                  ),
                  const SizedBox(width: 8),

                  // Level Chips
                  ...levels.map((level) {
                    final isSelected = selectedLevel == level;
                    return Padding(
                      padding: const EdgeInsets.only(right: 8),
                      child: ChoiceChip(
                        label: Text(level),
                        selected: isSelected,
                        onSelected: (selected) {
                          setState(() {
                            selectedLevel = level;
                            filterCourses();
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
                  }),
                ],
              ),
            ),
          ),

          // Active Filters Summary
          if (selectedSpecialization != 'All' ||
              selectedLevel != 'All' ||
              showOnlyAvailable)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              color: Colors.blue[50],
              child: Row(
                children: [
                  Icon(Icons.info_outline, size: 16, color: Colors.blue[700]),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      'Showing ${filteredCourses.length} of ${allCourses.length} courses',
                      style: TextStyle(fontSize: 12, color: Colors.blue[700]),
                    ),
                  ),
                  TextButton(
                    onPressed: () {
                      setState(() {
                        selectedSpecialization = 'All';
                        selectedLevel = 'All';
                        showOnlyAvailable = false;
                        searchQuery = '';
                        searchController.clear();
                        filterCourses();
                      });
                    },
                    child:
                        const Text('Clear All', style: TextStyle(fontSize: 12)),
                  ),
                ],
              ),
            ),

          // Course List
          Expanded(
            child: isLoading
                ? const Center(child: CircularProgressIndicator())
                : filteredCourses.isEmpty
                    ? _buildEmptyState()
                    : RefreshIndicator(
                        onRefresh: loadCourses,
                        child: _buildCourseList(),
                      ),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.search_off, size: 64, color: Colors.grey[300]),
            const SizedBox(height: 16),
            Text(
              'No Courses Found',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.grey[700],
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Try adjusting your filters or search query',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 14, color: Colors.grey[600]),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCourseList() {
    // Group courses by specialization
    Map<String, List<Course>> groupedCourses = {};

    if (selectedSpecialization != 'All') {
      groupedCourses[selectedSpecialization] = filteredCourses;
    } else {
      for (var course in filteredCourses) {
        String spec = _getSpecialization(course);
        if (!groupedCourses.containsKey(spec)) {
          groupedCourses[spec] = [];
        }
        groupedCourses[spec]!.add(course);
      }
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: groupedCourses.length,
      itemBuilder: (context, index) {
        final spec = groupedCourses.keys.elementAt(index);
        final courses = groupedCourses[spec]!;

        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Specialization Header
            Padding(
              padding: EdgeInsets.only(
                bottom: 12,
                top: index == 0
                    ? 0
                    : 16, // ✅ FIX: Use 'index' here (it's available in this scope)
              ),
              child: Row(
                children: [
                  Container(
                    width: 4,
                    height: 24,
                    decoration: BoxDecoration(
                      color: const Color(0xFF00796B),
                      borderRadius: BorderRadius.circular(2),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Text(
                    spec,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.black87,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                    decoration: BoxDecoration(
                      color: Colors.grey[300],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      '${courses.length}',
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                        color: Colors.grey[700],
                      ),
                    ),
                  ),
                ],
              ),
            ),

            // Courses in this specialization
            ...courses.map((course) => _buildCourseCard(course)),
          ],
        );
      },
    );
  }

  Widget _buildCourseCard(Course course) {
    final isAvailable = course.isAvailableThisSemester;

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: isAvailable ? 4 : 1,
      shadowColor: isAvailable ? Colors.green.withOpacity(0.3) : Colors.black12,
      child: InkWell(
        onTap: () => _showCourseDetails(course),
        borderRadius: BorderRadius.circular(12),
        child: Container(
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(12),
            gradient: isAvailable
                ? LinearGradient(
                    colors: [
                      Colors.white,
                      Colors.green.withOpacity(0.05),
                    ],
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                  )
                : null,
            color: isAvailable ? null : Colors.grey[50],
          ),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Header Row
                Row(
                  children: [
                    // Course Code Badge
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(
                        color: isAvailable
                            ? const Color(0xFF00796B).withOpacity(0.1)
                            : Colors.grey[300],
                        borderRadius: BorderRadius.circular(8),
                        border: isAvailable
                            ? Border.all(
                                color: const Color(0xFF00796B), width: 1)
                            : null,
                      ),
                      child: Text(
                        course.courseCode,
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: isAvailable
                              ? const Color(0xFF00796B)
                              : Colors.grey[700],
                        ),
                      ),
                    ),
                    const Spacer(),

                    // Level Badge
                    Container(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: _getLevelColor(course.level).withOpacity(0.1),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(
                        'Level ${course.level}',
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                          color: _getLevelColor(course.level),
                        ),
                      ),
                    ),

                    // Available Badge
                    if (isAvailable) ...[
                      const SizedBox(width: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(
                          color: Colors.green[100],
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Row(
                          children: [
                            Icon(Icons.check_circle,
                                size: 12, color: Colors.green[700]),
                            const SizedBox(width: 4),
                            Text(
                              'Available',
                              style: TextStyle(
                                fontSize: 11,
                                fontWeight: FontWeight.bold,
                                color: Colors.green[700],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ],
                ),
                const SizedBox(height: 12),

                // Course Name
                Text(
                  course.courseName,
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: isAvailable ? Colors.black87 : Colors.grey[600],
                  ),
                ),
                const SizedBox(height: 8),

                // Description
                Text(
                  course.description,
                  style: TextStyle(
                    fontSize: 14,
                    color: isAvailable ? Colors.grey[700] : Colors.grey[500],
                    height: 1.4,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 12),

                // Info Row
                Row(
                  children: [
                    Icon(Icons.people_outline,
                        size: 16, color: Colors.grey[600]),
                    const SizedBox(width: 4),
                    Text(
                      'Capacity: ${course.capacity}',
                      style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                    ),
                    const SizedBox(width: 16),
                    Icon(Icons.credit_card, size: 16, color: Colors.grey[600]),
                    const SizedBox(width: 4),
                    Text(
                      '${course.creditHours} CH',
                      style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                    ),
                  ],
                ),

                // Skills
                if (course.skills.isNotEmpty) ...[
                  const SizedBox(height: 12),
                  Wrap(
                    spacing: 6,
                    runSpacing: 6,
                    children: course.skills.take(4).map((skill) {
                      return Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 8, vertical: 4),
                        decoration: BoxDecoration(
                          color:
                              isAvailable ? Colors.blue[50] : Colors.grey[200],
                          borderRadius: BorderRadius.circular(6),
                        ),
                        child: Text(
                          skill,
                          style: TextStyle(
                            fontSize: 11,
                            color: isAvailable
                                ? Colors.blue[700]
                                : Colors.grey[600],
                          ),
                        ),
                      );
                    }).toList(),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _showCourseDetails(Course course) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => DraggableScrollableSheet(
        initialChildSize: 0.7,
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
              Expanded(
                child: ListView(
                  controller: controller,
                  padding: const EdgeInsets.all(24),
                  children: [
                    // Header
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                course.courseCode,
                                style: const TextStyle(
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold,
                                  color: Color(0xFF00796B),
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                course.courseName,
                                style: const TextStyle(
                                  fontSize: 22,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        ),
                        if (course.isAvailableThisSemester)
                          Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 12, vertical: 6),
                            decoration: BoxDecoration(
                              color: Colors.green[100],
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Row(
                              children: [
                                Icon(Icons.check_circle,
                                    size: 16, color: Colors.green[700]),
                                const SizedBox(width: 4),
                                Text(
                                  'Available',
                                  style: TextStyle(
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.green[700],
                                  ),
                                ),
                              ],
                            ),
                          ),
                      ],
                    ),
                    const SizedBox(height: 24),

                    // Course Info
                    _buildDetailRow('Level', 'Level ${course.level}',
                        Icons.signal_cellular_alt),
                    _buildDetailRow('Capacity', '${course.capacity} students',
                        Icons.people),
                    _buildDetailRow('Credit Hours', '${course.creditHours} CH',
                        Icons.credit_card),
                    const SizedBox(height: 24),

                    // Description
                    const Text(
                      'Description',
                      style:
                          TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      course.description,
                      style: TextStyle(
                          fontSize: 14, color: Colors.grey[700], height: 1.6),
                    ),
                    const SizedBox(height: 24),

                    // Skills
                    if (course.skills.isNotEmpty) ...[
                      const Text(
                        'Skills You\'ll Learn',
                        style: TextStyle(
                            fontSize: 18, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 12),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: course.skills.map((skill) {
                          return Container(
                            padding: const EdgeInsets.symmetric(
                                horizontal: 16, vertical: 8),
                            decoration: BoxDecoration(
                              color: Colors.blue[50],
                              borderRadius: BorderRadius.circular(20),
                              border: Border.all(color: Colors.blue[200]!),
                            ),
                            child: Text(
                              skill,
                              style: TextStyle(
                                fontSize: 14,
                                fontWeight: FontWeight.w600,
                                color: Colors.blue[700],
                              ),
                            ),
                          );
                        }).toList(),
                      ),
                      const SizedBox(height: 24),
                    ],

                    // Prerequisites (if available)
                    if (course.prerequisites.isNotEmpty) ...[
                      const Text(
                        'Prerequisites',
                        style: TextStyle(
                            fontSize: 18, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 12),
                      ...course.prerequisites.map((prereq) {
                        return Padding(
                          padding: const EdgeInsets.only(bottom: 8),
                          child: Row(
                            children: [
                              const Icon(Icons.check_circle_outline,
                                  size: 20, color: Color(0xFF00796B)),
                              const SizedBox(width: 8),
                              Text(prereq,
                                  style: const TextStyle(fontSize: 14)),
                            ],
                          ),
                        );
                      }),
                      const SizedBox(height: 24),
                    ],

                    // Action Button
                    SizedBox(
                      width: double.infinity,
                      height: 48,
                      child: ElevatedButton.icon(
                        onPressed: course.isAvailableThisSemester
                            ? () {
                                Navigator.pop(context);
                                // Navigate to enrollment or recommendations
                              }
                            : null,
                        icon: const Icon(Icons.bookmark_add),
                        label: Text(
                          course.isAvailableThisSemester
                              ? 'Add to Wishlist'
                              : 'Not Available This Semester',
                        ),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF00796B),
                          disabledBackgroundColor: Colors.grey[300],
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildDetailRow(String label, String value, IconData icon) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        children: [
          Icon(icon, size: 20, color: const Color(0xFF00796B)),
          const SizedBox(width: 12),
          Text(
            '$label:',
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: Colors.grey[700],
            ),
          ),
          const SizedBox(width: 8),
          Text(
            value,
            style: const TextStyle(fontSize: 14),
          ),
        ],
      ),
    );
  }

  void _showFilterBottomSheet() {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.only(
          topLeft: Radius.circular(20),
          topRight: Radius.circular(20),
        ),
      ),
      builder: (context) => StatefulBuilder(
        builder: (context, setModalState) => Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Filter Courses',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 24),

              // Specialization
              const Text('Specialization',
                  style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: specializations.map((spec) {
                  final isSelected = selectedSpecialization == spec;
                  return ChoiceChip(
                    label: Text(spec),
                    selected: isSelected,
                    onSelected: (selected) {
                      setModalState(() {
                        selectedSpecialization = spec;
                      });
                      setState(() {
                        filterCourses();
                      });
                    },
                    selectedColor: const Color(0xFF00796B).withOpacity(0.2),
                    checkmarkColor: const Color(0xFF00796B),
                  );
                }).toList(),
              ),
              const SizedBox(height: 24),

              // Buttons
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      onPressed: () {
                        setModalState(() {
                          selectedSpecialization = 'All';
                          selectedLevel = 'All';
                          showOnlyAvailable = false;
                        });
                        setState(() {
                          filterCourses();
                        });
                      },
                      child: const Text('Clear'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: ElevatedButton(
                      onPressed: () => Navigator.pop(context),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF00796B),
                      ),
                      child: const Text('Apply'),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _getSpecialization(Course course) {
    if (course.courseCode.contains('CSCI42') ||
        course.courseCode.contains('CSCI45') ||
        course.courseName.toLowerCase().contains('data')) {
      return 'Data Science';
    } else if (course.courseCode.contains('CSCI43') ||
        course.courseName.toLowerCase().contains('network') ||
        course.courseName.toLowerCase().contains('security')) {
      return 'Network & CyberSecurity';
    } else if (course.courseCode.contains('CSCI33') ||
        course.courseName.toLowerCase().contains('software')) {
      return 'Software Engineering';
    } else if (course.courseCode.contains('CSCI41') ||
        course.courseName.toLowerCase().contains('intelligence') ||
        course.courseName.toLowerCase().contains('machine learning')) {
      return 'AI & Machine Learning';
    } else if (course.courseCode.contains('CSCI31') ||
        course.courseCode.contains('CSCI32') ||
        course.courseName.toLowerCase().contains('web') ||
        course.courseName.toLowerCase().contains('mobile')) {
      return 'Web & Mobile Development';
    }
    return 'Other Courses';
  }

  Color _getLevelColor(int level) {
    switch (level) {
      case 1:
        return Colors.green;
      case 2:
        return Colors.blue;
      case 3:
        return Colors.orange;
      case 4:
        return Colors.red;
      default:
        return Colors.grey;
    }
  }
}
