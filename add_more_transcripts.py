"""
Add additional Neil deGrasse Tyson transcripts to vector store.
"""

import asyncio
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.rag.ingest_html import ingest_html
from backend.rag.store import add_to_store
from backend.settings import get_settings


# New transcript URLs to add
NEW_URLS = [
    # Point of Inquiry - Communicating Science to the Public
    "https://pointofinquiry.org/2007/11/neil-degrasse-tyson-communicating-science-to-the-public/",
    
    # Rev.com - Artemis I questions
    "https://www.rev.com/transcripts/neil-degrasse-tyson-answers-artemis-i-questions-transcript",
    
    # Speakola - Science in America 2017
    "https://speakola.com/ideas/neil-degrasse-tyson-science-in-america-2017",
]


async def scrape_and_add_url(url: str, settings):
    """Scrape a URL and add to vector store."""
    print(f"\n📄 Processing: {url}")
    print("─" * 80)
    
    try:
        # Ingest the URL (scrape and chunk) - run in executor since it's sync
        loop = asyncio.get_event_loop()
        chunks = await loop.run_in_executor(
            None, 
            ingest_html, 
            url, 
            Path("data/cache")  # Cache directory
        )
        
        if not chunks:
            print(f"⚠️  No content extracted from {url}")
            return 0
        
        print(f"✅ Extracted {len(chunks)} chunks")
        
        # Add to vector store
        store_path = Path(settings.vector_store_path)
        add_to_store(chunks, store_path)
        
        print(f"✅ Added {len(chunks)} chunks to vector store")
        return len(chunks)
        
    except Exception as e:
        print(f"❌ Error processing {url}: {e}")
        return 0


async def main():
    """Main function to scrape all URLs."""
    print("=" * 80)
    print("🚀 Adding Additional NDT Transcripts")
    print("=" * 80)
    
    settings = get_settings()
    
    total_chunks = 0
    successful_urls = 0
    failed_urls = []
    
    for url in NEW_URLS:
        chunks_added = await scrape_and_add_url(url, settings)
        
        if chunks_added > 0:
            successful_urls += 1
            total_chunks += chunks_added
        else:
            failed_urls.append(url)
        
        # Small delay between requests
        await asyncio.sleep(2)
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 Ingestion Summary")
    print("=" * 80)
    print(f"✅ Successfully processed: {successful_urls}/{len(NEW_URLS)} URLs")
    print(f"📦 Total NEW chunks added: {total_chunks}")
    print(f"📍 Vector store location: {settings.vector_store_path}")
    
    if failed_urls:
        print(f"\n⚠️  Failed URLs ({len(failed_urls)}):")
        for url in failed_urls:
            print(f"   - {url}")
    
    print("\n💡 Next steps:")
    print("   1. Restart the backend server to clear vector store cache")
    print("   2. Your chatbot now has even more comprehensive NDT content!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Ingestion interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Ingestion failed: {e}")
        import traceback
        traceback.print_exc()
