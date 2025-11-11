"""HTML ingestion with trafilatura."""

import argparse
from pathlib import Path
from typing import List
from urllib.parse import urlparse

import httpx
import trafilatura

from backend.rag.splitter import split_with_attribution
from backend.rag.store import add_to_store
from backend.utils.hashing import hash_content


# Curated seed sources - public interviews, essays, transcripts
SEED_URLS = [
    # PBS NOVA interviews and transcripts
    "https://www.pbs.org/wgbh/nova/origins/tyson.html",
    "https://www.pbs.org/wgbh/nova/transcripts/3114_origins.html",
    "https://www.pbs.org/wgbh/nova/transcripts/3111_origins.html",
    
    # Natural History Magazine - Universe column
    "https://naturalhistorymag.com/author/neil-degrasse-tyson",
    "https://www.naturalhistorymag.com/universe/211420/the-perimeter-of-ignorance",
    
    # NDT personal site essays
    "https://neildegrassetyson.com/essays/2006-11-delusions-of-space-enthusiasts/",
    
    # StarTalk transcripts
    "https://startalkmedia.com/show/",
    "https://app.podscribe.com/series/372",
    
    # Podcast transcripts
    "https://tim.blog/2019/10/15/neil-degrasse-tyson-transcript/",
    "https://podcasts.happyscribe.com/smartless/neil-degrasse-tyson",
    "https://singjupost.com/transcript-astrophysicist-neil-degrasse-tyson-on-joe-rogan-podcast-1159/",
    
    # AMNH events and courses
    "https://www.amnh.org/explore/videos/isaac-asimov-memorial-debate/2011",
    "https://www.amnh.org/learn-teach/seminars-on-science/courses/the-solar-system",
]


def fetch_html(url: str, cache_dir: Path | None = None) -> str:
    """Fetch HTML from URL with optional caching."""
    cache_file = None
    if cache_dir:
        cache_file = cache_dir / f"{hash_content(url)}.html"
        if cache_file.exists():
            print(f"Using cached: {url}")
            return cache_file.read_text(encoding="utf-8")
    
    print(f"Fetching: {url}")
    response = httpx.get(url, follow_redirects=True, timeout=30)
    response.raise_for_status()
    
    html = response.text
    if cache_file:
        cache_file.write_text(html, encoding="utf-8")
    
    return html


def extract_text_from_html(html: str, url: str = "") -> tuple[str, dict]:
    """Extract clean text and metadata from HTML."""
    text = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=False,
        favor_precision=True,
    )
    
    # Extract title for better citations
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    path_title = parsed.path.strip("/").split("/")[-1].replace("-", " ").title()
    
    metadata = {
        "url": url,
        "source": url,
        "title": path_title or domain,
        "domain": domain,
    }
    
    return text or "", metadata


def ingest_html(
    url: str,
    cache_dir: Path | None = None,
) -> List[dict]:
    """Ingest a single HTML page."""
    html = fetch_html(url, cache_dir)
    text, metadata = extract_text_from_html(html, url)
    
    # Skip if content too short (likely error page or boilerplate)
    if not text or len(text) < 400:
        print(f"⚠️  No meaningful content extracted from {url}")
        return []
    
    # Split into chunks with rich metadata
    chunks = split_with_attribution(
        text=text,
        source=url,
        metadata=metadata,
    )
    
    print(f"Created {len(chunks)} chunks from {url}")
    return chunks


def ingest_urls_from_file(
    urls_file: Path,
    cache_dir: Path,
    output_dir: Path,
) -> None:
    """Ingest URLs from a seed file."""
    urls = []
    with open(urls_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    all_chunks = []
    for url in urls:
        try:
            chunks = ingest_html(url, cache_dir)
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"❌ Error ingesting {url}: {e}")
    
    # Add to vector store
    if all_chunks:
        print(f"Adding {len(all_chunks)} total chunks to store...")
        add_to_store(all_chunks, output_dir)
        print("✅ HTML ingestion complete")


def main():
    parser = argparse.ArgumentParser(description="Ingest HTML from URLs")
    parser.add_argument(
        "--urls-file",
        type=Path,
        help="File with URLs (one per line). If not provided, uses SEED_URLS.",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("data/cache"),
        help="Directory for HTML caching",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("storage/vector_store"),
        help="Output directory for vector store",
    )
    args = parser.parse_args()
    
    # Use seed URLs if no file provided
    if args.urls_file and args.urls_file.exists():
        ingest_urls_from_file(args.urls_file, args.cache_dir, args.output_dir)
    else:
        print(f"Using {len(SEED_URLS)} curated seed URLs...")
        cache_dir = args.cache_dir
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        all_chunks = []
        for url in SEED_URLS:
            try:
                chunks = ingest_html(url, cache_dir)
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"❌ Error ingesting {url}: {e}")
        
        if all_chunks:
            print(f"Adding {len(all_chunks)} total chunks to store...")
            add_to_store(all_chunks, args.output_dir)
            print("✅ HTML ingestion complete")
        else:
            print("⚠️  No chunks generated from any URL")


if __name__ == "__main__":
    main()
