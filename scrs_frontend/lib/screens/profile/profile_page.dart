import 'package:flutter/material.dart';
import '../../services/user_service.dart';
import '../../services/session.dart';
import '../login/login_page.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  Map<String, dynamic>? user;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadProfile();
  }

  void loadProfile() async {
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  const SizedBox(height: 24),
                  const CircleAvatar(
                    radius: 50,
                    backgroundColor: Colors.grey,
                    child: Icon(Icons.person, size: 50, color: Colors.white),
                  ),
                  const SizedBox(height: 24),
                  _infoBox('Name', user?['name'] ?? '-'),
                  _infoBox('Matric Number', user?['matric_number'] ?? '-'),
                  _infoBox('Email', user?['email'] ?? '-'),
                  _infoBox('Role', user?['role'] ?? '-'),
                  const Spacer(),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.red,
                      ),
                      onPressed: () {
                        Session.token = null;

                        Navigator.pushAndRemoveUntil(
                          context,
                          MaterialPageRoute(
                            builder: (context) => const LoginPage(),
                          ),
                          (route) => false,
                        );
                      },
                      child: const Text('Logout'),
                    ),
                  ),
                ],
              ),
            ),
    );
  }

  Widget _infoBox(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: TextField(
        readOnly: true,
        decoration: InputDecoration(
          labelText: label,
          border: const OutlineInputBorder(),
        ),
        controller: TextEditingController(text: value),
      ),
    );
  }
}
