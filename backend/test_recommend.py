"""Test recommendation endpoint"""
import requests
import json

# First, login to get a token
login_response = requests.post(
    "http://127.0.0.1:5000/auth/login",
    json={"email": "student@test.com", "password": "password123"}
)

if login_response.status_code == 200:
    token = login_response.json().get("access_token")
    print(f"✅ Logged in successfully")
    print(f"Token: {token[:20]}...")
    
    # Test recommendation endpoint
    headers = {"Authorization": f"Bearer {token}"}
    rec_response = requests.get(
        "http://127.0.0.1:5000/recommend/",
        headers=headers
    )
    
    print(f"\nRecommendation endpoint status: {rec_response.status_code}")
    print(f"Response:")
    print(json.dumps(rec_response.json(), indent=2))
    
else:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
