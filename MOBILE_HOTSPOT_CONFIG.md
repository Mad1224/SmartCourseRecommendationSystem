# Mobile Hotspot Configuration Guide

## Steps to Configure for Mobile Hotspot:

### 1. Find Your Computer's IP Address
Open PowerShell and run:
```powershell
ipconfig
```

Look for **"Wireless LAN adapter Wi-Fi"** section and find the **IPv4 Address**.

Common mobile hotspot IP addresses:
- `192.168.137.1` (Windows hotspot default)
- `192.168.43.1` (Android hotspot default)
- `172.20.10.x` (iPhone hotspot default)

### 2. Update the Flutter App Configuration

File: `scrs_frontend\lib\config\api.dart`

Change this line:
```dart
return 'http://192.168.137.1:5000';  // 👈 Replace with your actual IP
```

**Example:**
If your IP is `192.168.43.100`, change to:
```dart
return 'http://192.168.43.100:5000';
```

### 3. Make Sure Backend is Running on All Interfaces

The backend (`app.py`) should already be configured to listen on `0.0.0.0:5000`, which allows connections from any network interface.

Verify in `backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### 4. Configure Windows Firewall

**Option A: Allow Python through firewall (Recommended)**
1. Open Windows Defender Firewall
2. Click "Allow an app or feature through Windows Defender Firewall"
3. Click "Change settings"
4. Find Python or add it if not listed
5. Check both "Private" and "Public" boxes

**Option B: Create firewall rule**
```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "Python Backend" -Direction Inbound -Program "C:\Python312\python.exe" -Action Allow
```

### 5. Restart Backend Server
```bash
cd backend
python app.py
```

The server should show:
```
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://YOUR_IP:5000
```

### 6. Test Connection

**From your computer:**
```bash
curl http://127.0.0.1:5000/
```

**From your phone's browser:**
```
http://YOUR_IP:5000/
```

You should see:
```json
{"msg": "SCRS Backend API", "version": "1.0", "status": "running"}
```

### 7. Rebuild Flutter App

After changing the API config:
```bash
cd scrs_frontend
flutter clean
flutter pub get
flutter run
```

## Troubleshooting

### Cannot connect from phone:
1. ✓ Check firewall settings
2. ✓ Verify IP address is correct
3. ✓ Make sure both devices on same hotspot
4. ✓ Backend is running and accessible
5. ✓ Try disabling Windows Firewall temporarily to test

### Connection timeout:
- Backend might not be running
- IP address changed
- Firewall blocking

### "Network unreachable":
- Wrong IP address
- Devices not on same network
- Mobile data might be active instead of hotspot WiFi

## Quick Test Commands

```powershell
# Find your IP
ipconfig | findstr "IPv4"

# Test backend locally
curl http://127.0.0.1:5000/

# Check if port is open
Test-NetConnection -ComputerName 127.0.0.1 -Port 5000
```
