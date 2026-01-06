"""
Test that preferences affect recommendations
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# Login
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "test@iium.edu.my", "password": "test123"}
)

if login_response.status_code != 200:
    print("❌ Login failed")
    print(login_response.text)
    exit(1)

token = login_response.json()["token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

print("✅ Logged in successfully\n")

# Test 1: Set preferences for KOE (Engineering)
print("=" * 70)
print("TEST 1: Setting preferences for KOE (Engineering)")
print("=" * 70)

prefs_data = {
    "kulliyyah": "KOE",
    "semester": 3,
    "cgpa": 3.5,
    "preferredTypes": ["Practical", "Project-based"],
    "preferredTime": "Morning"
}

prefs_response = requests.post(
    f"{BASE_URL}/preferences/",
    headers=headers,
    json=prefs_data
)

if prefs_response.status_code == 201:
    print("✅ Preferences saved")
    print(f"   Kulliyyah: {prefs_data['kulliyyah']}")
    print(f"   Preferred Types: {', '.join(prefs_data['preferredTypes'])}")
else:
    print(f"❌ Failed to save preferences: {prefs_response.status_code}")

# Get recommendations
print("\n📊 Getting recommendations...")
rec_response = requests.get(f"{BASE_URL}/recommend/", headers=headers)

if rec_response.status_code == 200:
    recommendations = rec_response.json()
    print(f"✅ Received {len(recommendations)} recommendations\n")
    
    print("Top 5 recommendations for KOE preference:")
    print("-" * 70)
    koe_count = 0
    for i, rec in enumerate(recommendations[:5], 1):
        is_koe = rec.get('kulliyyah') == 'KOE'
        marker = "✓ KOE" if is_koe else f"  {rec.get('kulliyyah', 'N/A')}"
        print(f"{i}. [{marker}] {rec['course_code']}: {rec['course_name']}")
        print(f"   Score: {rec['score']:.1f}% | {rec['reason']}")
        if is_koe:
            koe_count += 1
    
    print(f"\n📈 KOE courses in top 5: {koe_count}/5")
    if koe_count >= 3:
        print("✅ Preferences are working! KOE courses are prioritized")
    else:
        print("⚠️  Fewer KOE courses than expected")
else:
    print(f"❌ Failed to get recommendations: {rec_response.status_code}")
    print(rec_response.text)

# Test 2: Change to KICT preference
print("\n" + "=" * 70)
print("TEST 2: Changing preferences to KICT (ICT)")
print("=" * 70)

prefs_data2 = {
    "kulliyyah": "KICT",
    "semester": 3,
    "cgpa": 3.5,
    "preferredTypes": ["Theory", "Research"],
    "preferredTime": "Afternoon"
}

prefs_response2 = requests.post(
    f"{BASE_URL}/preferences/",
    headers=headers,
    json=prefs_data2
)

if prefs_response2.status_code == 201:
    print("✅ Preferences updated")
    print(f"   Kulliyyah: {prefs_data2['kulliyyah']}")
    print(f"   Preferred Types: {', '.join(prefs_data2['preferredTypes'])}")

# Get new recommendations
print("\n📊 Getting new recommendations...")
rec_response2 = requests.get(f"{BASE_URL}/recommend/", headers=headers)

if rec_response2.status_code == 200:
    recommendations2 = rec_response2.json()
    print(f"✅ Received {len(recommendations2)} recommendations\n")
    
    print("Top 5 recommendations for KICT preference:")
    print("-" * 70)
    kict_count = 0
    for i, rec in enumerate(recommendations2[:5], 1):
        is_kict = rec.get('kulliyyah') == 'KICT'
        marker = "✓ KICT" if is_kict else f"  {rec.get('kulliyyah', 'N/A')}"
        print(f"{i}. [{marker}] {rec['course_code']}: {rec['course_name']}")
        print(f"   Score: {rec['score']:.1f}% | {rec['reason']}")
        if is_kict:
            kict_count += 1
    
    print(f"\n📈 KICT courses in top 5: {kict_count}/5")
    if kict_count >= 3:
        print("✅ Preferences are working! KICT courses are prioritized")
    else:
        print("⚠️  Fewer KICT courses than expected")
else:
    print(f"❌ Failed to get recommendations: {rec_response2.status_code}")

print("\n" + "=" * 70)
print("✅ Test complete! Preferences should now affect recommendations.")
print("=" * 70)
