"""Simple health check test - no API key needed."""

import httpx
import asyncio


async def test_health():
    """Test if the server is running."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/api/healthz")
            print(f"✅ Health check: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"❌ Server not running: {e}")
            print("\nTo start the server, run:")
            print("  uvicorn backend.app:app --reload --port 8000")


async def test_ready():
    """Test if the server is ready (has vector store)."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/api/ready")
            print(f"\n✅ Ready check: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"\n⚠️  Ready check failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_health())
    asyncio.run(test_ready())
