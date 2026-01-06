"""
Quick test to verify API recommendations work
"""
import requests
import json

print("🧪 Testing Recommendation API\n")

# Test if backend is running
try:
    health_check = requests.get("http://127.0.0.1:5000/")
    print("✅ Backend is running")
except:
    print("❌ Backend is not responding")
    exit(1)

# Try to login
print("\n📝 Logging in...")
login_response = requests.post(
    "http://127.0.0.1:5000/auth/login",
    json={"email": "test@iium.edu.my", "password": "test123"}
)

if login_response.status_code == 200:
    token = login_response.json().get("access_token")
    print(f"✅ Logged in successfully")
    
    # Test recommendation endpoint
    print("\n🎯 Testing recommendations...")
    headers = {"Authorization": f"Bearer {token}"}
    rec_response = requests.get(
        "http://127.0.0.1:5000/recommend/",
        headers=headers
    )
    
    if rec_response.status_code == 200:
        data = rec_response.json()
        recommendations = data.get("recommendations", [])
        print(f"✅ Recommendations endpoint working!")
        print(f"   Received {len(recommendations)} recommendations")
        
        if recommendations:
            print("\n📚 Top 3 recommendations:")
            for rec in recommendations[:3]:
                print(f"   • {rec.get('course_code')}: {rec.get('course_name')} (score: {rec.get('final_score', 0):.3f})")
        
        print("\n✅ All systems working! The white screen issue should be fixed.")
    else:
        print(f"❌ Recommendation failed: {rec_response.status_code}")
        print(rec_response.text)
else:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
