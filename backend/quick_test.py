"""
Quick test to see if kulliyyah preference works
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# Login
r = requests.post(f"{BASE_URL}/auth/login", json={"email": "test@iium.edu.my", "password": "test123"})
token = r.json()["token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Set KOE preference
print("TEST 1: Setting preference: KOE (Engineering)\n")
requests.post(f"{BASE_URL}/preferences/", headers=headers, json={
    "kulliyyah": "KOE",
    "semester": 3,
    "cgpa": 3.5,
    "preferredTypes": ["Practical"],
    "preferredTime": "Morning"
})

# Get recommendations
rec = requests.get(f"{BASE_URL}/recommend/", headers=headers).json()

print("Top 10 recommendations:")
print("-" * 80)
for i, r in enumerate(rec[:10], 1):
    kull = r.get('kulliyyah', 'N/A')
    match = "✓" if kull == 'KOE' else " "
    print(f"{i:2}. [{match}] [{kull:6s}] {r['course_code']:10s} {r['course_name'][:40]:40s} ({r['score']:.1f}%)")
    
koe_count = sum(1 for r in rec[:10] if r.get('kulliyyah') == 'KOE')
print(f"\nKOE courses in top 10: {koe_count}/10")

# Test KICT
print("\n" + "=" * 80)
print("TEST 2: Changing preference: KICT (ICT)\n")
requests.post(f"{BASE_URL}/preferences/", headers=headers, json={
    "kulliyyah": "KICT",
    "semester": 3,
    "cgpa": 3.5,
    "preferredTypes": ["Theory"],
    "preferredTime": "Morning"
})

rec2 = requests.get(f"{BASE_URL}/recommend/", headers=headers).json()

print("Top 10 recommendations:")
print("-" * 80)
for i, r in enumerate(rec2[:10], 1):
    kull = r.get('kulliyyah', 'N/A')
    match = "✓" if kull == 'KICT' else " "
    print(f"{i:2}. [{match}] [{kull:6s}] {r['course_code']:10s} {r['course_name'][:40]:40s} ({r['score']:.1f}%)")
    
kict_count = sum(1 for r in rec2[:10] if r.get('kulliyyah') == 'KICT')
print(f"\nKICT courses in top 10: {kict_count}/10")
