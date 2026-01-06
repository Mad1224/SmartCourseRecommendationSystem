import 'dart:io' show Platform;

class ApiConfig {
  // ========================================
  // MOBILE HOTSPOT CONFIGURATION
  // ========================================
  // When using mobile hotspot:
  // 1. Connect your computer to your mobile hotspot
  // 2. Run 'ipconfig' in PowerShell
  // 3. Look for "Wireless LAN adapter Wi-Fi" section
  // 4. Copy the IPv4 Address (e.g., 192.168.x.x)
  // 5. Replace the IP below in the Android section
  // ========================================
  
  // Different base URLs for different platforms
  static String get baseUrl {
    if (Platform.isAndroid) {
      // FOR PHYSICAL ANDROID DEVICE - UPDATE THIS IP!
      // Use your computer's IP when connected to mobile hotspot
      // To find IP: Run 'ipconfig' in PowerShell
      return 'http://10.148.236.35:5000';  // 👈 UPDATE THIS!
      
      // Note: Use 10.0.2.2 for Android emulator instead:
      // return 'http://10.0.2.2:5000';
    } else if (Platform.isIOS) {
      // iOS simulator can use localhost
      return 'http://localhost:5000';
    } else {
      // For desktop (Windows, macOS, Linux)
      return 'http://127.0.0.1:5000';
    }
  }
}
