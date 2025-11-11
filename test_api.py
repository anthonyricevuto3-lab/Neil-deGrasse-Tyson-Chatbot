"""Test the chat API."""

import requests
import json

# Test endpoint
url = "http://localhost:8000/api/chat"

# Test question
payload = {
    "message": "Why are we made of stardust?"
}

print("Sending request to chat API...")
print(f"Question: {payload['message']}\n")

try:
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    print("✅ Response received!\n")
    print("=" * 60)
    print(data.get('response', 'No response field'))
    print("=" * 60)
    
    if 'sources' in data:
        print(f"\n📚 Sources ({len(data['sources'])}):")
        for i, source in enumerate(data['sources'], 1):
            print(f"  {i}. {source.get('title', 'Unknown')} - {source.get('url', 'No URL')}")
    
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to server. Is it running on port 8000?")
except requests.exceptions.Timeout:
    print("❌ Request timed out")
except Exception as e:
    print(f"❌ Error: {e}")
