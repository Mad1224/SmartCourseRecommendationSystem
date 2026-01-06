import 'package:flutter/material.dart';
import '../../services/advising_service.dart';

class RequestAdvisingPage extends StatefulWidget {
  const RequestAdvisingPage({super.key});

  @override
  State<RequestAdvisingPage> createState() => _RequestAdvisingPageState();
}

class _RequestAdvisingPageState extends State<RequestAdvisingPage> {
  final _formKey = GlobalKey<FormState>();

  String? selectedAdvisingType;
  String? selectedLecturer;
  final TextEditingController additionalNoteController =
      TextEditingController();

  bool isLoading = false;
  bool isLoadingLecturers = true;
  List<Map<String, dynamic>> availableLecturers = [];

  final List<String> advisingTypes = [
    'Course Selection',
    'Academic Progress Review',
    'Career Guidance',
    'Course Drop/Add',
    'Academic Planning',
    'Graduation Requirements',
    'Internship Guidance',
    'Research Opportunities',
    'Other',
  ];

  @override
  void initState() {
    super.initState();
    loadLecturers();
  }

  @override
  void dispose() {
    additionalNoteController.dispose();
    super.dispose();
  }

  Future<void> loadLecturers() async {
    setState(() => isLoadingLecturers = true);
    try {
      final lecturers = await AdvisingService.getAvailableLecturers();
      setState(() {
        availableLecturers = lecturers;
        isLoadingLecturers = false;
      });
    } catch (e) {
      setState(() => isLoadingLecturers = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error loading lecturers: $e')),
        );
      }
    }
  }

  Future<void> submitRequest() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => isLoading = true);

    try {
      await AdvisingService.submitAdvisingRequest(
        advisingType: selectedAdvisingType!,
        preferredLecturer: selectedLecturer,
        additionalNote: additionalNoteController.text.trim(),
      );

      setState(() => isLoading = false);

      if (mounted) {
        // Show success dialog
        showDialog(
          context: context,
          barrierDismissible: false,
          builder: (context) => Dialog(
            shape:
                RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(
                    width: 80,
                    height: 80,
                    decoration: BoxDecoration(
                      color: Colors.green[50],
                      shape: BoxShape.circle,
                    ),
                    child: Icon(
                      Icons.check_circle,
                      size: 50,
                      color: Colors.green[600],
                    ),
                  ),
                  const SizedBox(height: 20),
                  const Text(
                    'Request Submitted!',
                    style: TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    'Your academic advising request has been sent to the academic office.',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey[700],
                    ),
                  ),
                  const SizedBox(height: 8),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.blue[50],
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Row(
                      children: [
                        Icon(Icons.info_outline,
                            size: 20, color: Colors.blue[700]),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            'You will receive a response within 2-3 business days',
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.blue[700],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),
                  Row(
                    children: [
                      Expanded(
                        child: OutlinedButton(
                          onPressed: () {
                            Navigator.pop(context);
                            Navigator.pop(context); // Go back to Academic Data
                          },
                          style: OutlinedButton.styleFrom(
                            padding: const EdgeInsets.symmetric(vertical: 14),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                          child: const Text('Close'),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: ElevatedButton(
                          onPressed: () {
                            Navigator.pop(context);
                            Navigator.pop(context);
                            // Navigate to view requests
                            Navigator.pushNamed(context, '/my-requests');
                          },
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFF00796B),
                            padding: const EdgeInsets.symmetric(vertical: 14),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                          child: const Text('View Requests'),
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
    } catch (e) {
      setState(() => isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error submitting request: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: const Text('Request Academic Advising'),
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Info Card
            Card(
              color: Colors.blue[50],
              elevation: 0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                side: BorderSide(color: Colors.blue[200]!),
              ),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  children: [
                    Icon(Icons.info_outline, color: Colors.blue[700], size: 24),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        'Submit an advising request and our academic staff will contact you within 2-3 business days',
                        style: TextStyle(
                          fontSize: 13,
                          color: Colors.blue[900],
                          height: 1.4,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Advising Type
            const Text(
              'Advising Type',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'What do you need help with?',
              style: TextStyle(fontSize: 12, color: Colors.grey[600]),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              initialValue: selectedAdvisingType,
              decoration: InputDecoration(
                hintText: 'Select advising type',
                prefixIcon:
                    const Icon(Icons.category, color: Color(0xFF00796B)),
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(color: Colors.grey[300]!),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(color: Colors.grey[300]!),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide:
                      const BorderSide(color: Color(0xFF00796B), width: 2),
                ),
              ),
              items: advisingTypes.map((type) {
                return DropdownMenuItem(
                  value: type,
                  child: Text(type),
                );
              }).toList(),
              validator: (value) =>
                  value == null ? 'Please select an advising type' : null,
              onChanged: (value) {
                setState(() {
                  selectedAdvisingType = value;
                });
              },
            ),
            const SizedBox(height: 24),

            // Preferred Lecturer
            const Text(
              'Preferred Lecturer (Optional)',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Choose a specific lecturer or leave empty for automatic assignment',
              style: TextStyle(fontSize: 12, color: Colors.grey[600]),
            ),
            const SizedBox(height: 12),
            isLoadingLecturers
                ? Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.grey[300]!),
                    ),
                    child: const Row(
                      children: [
                        SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        ),
                        SizedBox(width: 12),
                        Text('Loading lecturers...'),
                      ],
                    ),
                  )
                : DropdownButtonFormField<String>(
                    initialValue: selectedLecturer,
                    decoration: InputDecoration(
                      hintText: 'Auto-assign to available lecturer',
                      prefixIcon:
                          const Icon(Icons.person, color: Color(0xFF00796B)),
                      filled: true,
                      fillColor: Colors.white,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide(color: Colors.grey[300]!),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide(color: Colors.grey[300]!),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: const BorderSide(
                            color: Color(0xFF00796B), width: 2),
                      ),
                    ),
                    items: [
                      const DropdownMenuItem(
                        value: null,
                        child: Text('Auto-assign to available lecturer'),
                      ),
                      ...availableLecturers.map((lecturer) {
                        return DropdownMenuItem(
                          value: lecturer['id'],
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                lecturer['name'] ?? '',
                                style: const TextStyle(
                                    fontWeight: FontWeight.w600),
                              ),
                              if (lecturer['specialization'] != null)
                                Text(
                                  lecturer['specialization'],
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: Colors.grey[600],
                                  ),
                                ),
                            ],
                          ),
                        );
                      }),
                    ],
                    onChanged: (value) {
                      setState(() {
                        selectedLecturer = value;
                      });
                    },
                  ),
            const SizedBox(height: 24),

            // Additional Notes
            const Text(
              'Additional Notes',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Provide any additional details that might help the adviser',
              style: TextStyle(fontSize: 12, color: Colors.grey[600]),
            ),
            const SizedBox(height: 12),
            TextFormField(
              controller: additionalNoteController,
              maxLines: 6,
              maxLength: 500,
              decoration: InputDecoration(
                hintText:
                    'E.g., "I need help choosing electives for next semester..." or "I want to discuss my academic progress..."',
                filled: true,
                fillColor: Colors.white,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(color: Colors.grey[300]!),
                ),
                enabledBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide(color: Colors.grey[300]!),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide:
                      const BorderSide(color: Color(0xFF00796B), width: 2),
                ),
                counterStyle: TextStyle(color: Colors.grey[600]),
              ),
              validator: (value) {
                if (value == null || value.trim().isEmpty) {
                  return 'Please provide some details about your request';
                }
                if (value.trim().length < 10) {
                  return 'Please provide more details (at least 10 characters)';
                }
                return null;
              },
            ),
            const SizedBox(height: 32),

            // Submit Button
            SizedBox(
              width: double.infinity,
              height: 54,
              child: ElevatedButton.icon(
                onPressed: isLoading ? null : submitRequest,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF00796B),
                  disabledBackgroundColor: Colors.grey[400],
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  elevation: 2,
                ),
                icon: isLoading
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          valueColor:
                              AlwaysStoppedAnimation<Color>(Colors.white),
                        ),
                      )
                    : const Icon(Icons.send, size: 22),
                label: Text(
                  isLoading ? 'Submitting...' : 'Submit Request',
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Cancel Button
            TextButton(
              onPressed: isLoading ? null : () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }
}
