class User {
  final String id;
  final String email;
  final String name;
  final String matricNumber;
  final String role;

  User({
    required this.id,
    required this.email,
    required this.name,
    required this.matricNumber,
    required this.role,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['_id'] ?? '',
      email: json['email'] ?? '',
      name: json['name'] ?? '',
      matricNumber: json['matric_number'] ?? '',
      role: json['role'] ?? 'student',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      '_id': id,
      'email': email,
      'name': name,
      'matric_number': matricNumber,
      'role': role,
    };
  }
}
