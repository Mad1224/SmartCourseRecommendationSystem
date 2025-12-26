import 'package:flutter/material.dart';
import 'screens/login/login_page.dart';

void main() {
  runApp(const SCRSApp());
}

class SCRSApp extends StatelessWidget {
  const SCRSApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Course Recommendation System',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(primarySwatch: Colors.green),
      home: const LoginPage(),
    );
  }
}
