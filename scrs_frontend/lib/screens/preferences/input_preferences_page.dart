import 'package:flutter/material.dart';
import '../../services/preferences_service.dart';
import '../recommendation/recommendation_results_page.dart';

class InputPreferencesPage extends StatefulWidget {
  const InputPreferencesPage({super.key});

  @override
  State<InputPreferencesPage> createState() => _InputPreferencesPageState();
}

class _InputPreferencesPageState extends State<InputPreferencesPage> {
  final _formKey = GlobalKey<FormState>();

  String? kulliyyah;
  int? semester;
  double? cgpa;
  String? preferredTime;
  List<String> preferredTypes = [];
  final TextEditingController avoidController = TextEditingController();

  final List<String> kulliyyahList = [
    'KICT',
    'KOE',
    'KAED',
    'KENMS',
    'KOED',
    'AIKOL',
    'AHASIRKS',
  ];

  final List<String> courseTypes = [
    'Theory',
    'Practical',
    'Project-based',
    'Research',
  ];

  final List<String> classTimes = [
    'Morning',
    'Afternoon',
    'Evening',
    'No preference',
  ];

  void _savePreferences() async {
    if (!_formKey.currentState!.validate()) return;

    final data = {
      'kulliyyah': kulliyyah,
      'semester': semester,
      'cgpa': cgpa,
      'preferredTypes': preferredTypes,
      'preferredTime': preferredTime,
      'coursesToAvoid':
          avoidController.text.isEmpty ? [] : [avoidController.text],
    };

    try {
      await PreferencesService.savePreferences(data);

      if (!mounted) return;

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => const RecommendationResultsPage(),
        ),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Failed to save preferences')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Input Course Preference'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              _dropdown(
                label: 'Kulliyyah',
                value: kulliyyah,
                items: kulliyyahList,
                onChanged: (val) => setState(() => kulliyyah = val),
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: _dropdown(
                      label: 'Semester',
                      value: semester?.toString(),
                      items: List.generate(8, (i) => '${i + 1}'),
                      onChanged: (val) =>
                          setState(() => semester = int.parse(val!)),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: TextFormField(
                      keyboardType:
                          const TextInputType.numberWithOptions(decimal: true),
                      decoration: const InputDecoration(
                        labelText: 'CGPA',
                        border: OutlineInputBorder(),
                      ),
                      validator: (value) {
                        final v = double.tryParse(value ?? '');
                        if (v == null || v < 0 || v > 4) {
                          return '0.00 - 4.00';
                        }
                        return null;
                      },
                      onChanged: (v) => cgpa = double.tryParse(v),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              _dropdown(
                label: 'Preferred class timing',
                value: preferredTime,
                items: classTimes,
                onChanged: (val) => setState(() => preferredTime = val),
              ),
              const SizedBox(height: 16),
              Align(
                alignment: Alignment.centerLeft,
                child: Wrap(
                  spacing: 8,
                  children: courseTypes.map((type) {
                    final selected = preferredTypes.contains(type);
                    return FilterChip(
                      label: Text(type),
                      selected: selected,
                      onSelected: (val) {
                        setState(() {
                          val
                              ? preferredTypes.add(type)
                              : preferredTypes.remove(type);
                        });
                      },
                    );
                  }).toList(),
                ),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: avoidController,
                decoration: const InputDecoration(
                  labelText: 'Courses to avoid (if any)',
                  hintText: 'e.g. CSCI 3301',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                height: 48,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                  ),
                  onPressed: _savePreferences,
                  child: const Text('Save'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _dropdown({
    required String label,
    required String? value,
    required List<String> items,
    required ValueChanged<String?> onChanged,
  }) {
    return DropdownButtonFormField<String>(
      initialValue: value,
      decoration: InputDecoration(
        labelText: label,
        border: const OutlineInputBorder(),
      ),
      items:
          items.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
      validator: (v) => v == null ? 'Required' : null,
      onChanged: onChanged,
    );
  }
}
