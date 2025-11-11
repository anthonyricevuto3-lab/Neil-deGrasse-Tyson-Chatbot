"""Simple health check test."""
import requests

try:
    response = requests.get("http://localhost:8000/api/health", timeout=5)
    print(f"Health check: {response.status_code}")
    print(response.json())
except Exception as e:
    print(f"Error: {e}")
