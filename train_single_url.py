"""
Train (ingest) a single Neil deGrasse Tyson source URL into the existing FAISS vector store.
Usage:
  python train_single_url.py --url https://neildegrassetyson.com/essays/2003-09-in-the-beginning/

If the store exists it will be extended; otherwise a new store will be created with just this URL.
"""
import os
import sys
import argparse
import time
from pathlib import Path
from typing import Tuple, List

sys.path.insert(0, str(Path(__file__).parent))

import requests
from bs4 import BeautifulSoup
import trafilatura
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 
    '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'
)
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

MIN_LENGTH = 200  # accept smaller pages for single-ingest

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache'
}


def fetch_url_content(url: str) -> Tuple[str, str, bool]:
    print(f"\nFetching: {url}")

    # Strategy 1: requests + trafilatura.extract
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        status = r.status_code
        if status >= 400:
            print(f"  ❌ HTTP status {status}")
        else:
            extracted = trafilatura.extract(r.text, include_comments=False)
            if extracted and len(extracted) >= MIN_LENGTH:
                soup = BeautifulSoup(r.text, 'html.parser')
                title = (soup.title.string if soup.title else url.split('/')[-1]).strip()
                print(f"  ✅ Extracted via trafilatura ({len(extracted)} chars)")
                return extracted, title, True
            else:
                print("  ⚠️ trafilatura returned insufficient content; falling back")
    except Exception as e:
        print(f"  ⚠️ requests/trafilatura failed: {e}")

    # Strategy 2: trafilatura.fetch_url directly
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            extracted = trafilatura.extract(downloaded, include_comments=False)
            if extracted and len(extracted) >= MIN_LENGTH:
                soup = BeautifulSoup(downloaded, 'html.parser')
                title = (soup.title.string if soup.title else url.split('/')[-1]).strip()
                print(f"  ✅ Extracted via trafilatura.fetch_url ({len(extracted)} chars)")
                return extracted, title, True
            else:
                print("  ⚠️ fetch_url produced too little content")
        else:
            print("  ⚠️ fetch_url returned None")
    except Exception as e:
        print(f"  ⚠️ trafilatura.fetch_url failed: {e}")

    # Strategy 3: requests + BeautifulSoup cleanup
    try:
        r2 = requests.get(url, headers=HEADERS, timeout=30)
        if r2.status_code < 400:
            soup = BeautifulSoup(r2.text, 'html.parser')
            for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'noscript']):
                tag.decompose()
            text = '\n'.join([line.strip() for line in soup.get_text('\n').split('\n') if line.strip()])
            if len(text) >= MIN_LENGTH:
                title = (soup.title.string if soup.title else url.split('/')[-1]).strip()
                print(f"  ✅ Extracted via BeautifulSoup ({len(text)} chars)")
                return text, title, True
            else:
                print(f"  ❌ Final fallback too short ({len(text)} chars)")
        else:
            print(f"  ❌ Second request HTTP {r2.status_code}")
    except Exception as e:
        print(f"  ❌ Final fallback error: {e}")

    return "", "", False


def chunk_text(text: str, metadata: dict, chunk_size: int = 900) -> List[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_text(text)
    return [
        {"content": c.strip(), "metadata": metadata.copy()} for c in chunks if len(c.strip()) >= 100
    ]


def main(url: str):
    print("=" * 80)
    print("SINGLE URL TRAINING")
    print("=" * 80)
    text, title, ok = fetch_url_content(url)
    if not ok:
        print("\n❌ Could not ingest the URL. It may be blocking scraping (403) or has too little content.")
        print("   Consider manually copying the page text into a file and using the corpus ingestion path.")
        return

    domain = url.split('/')[2]
    metadata = {"source": url, "url": url, "title": title, "domain": domain}
    chunks = chunk_text(text, metadata)
    print(f"\n✅ Created {len(chunks)} chunks from '{title}'")
    if not chunks:
        print("❌ No usable chunks; aborting before embeddings.")
        return

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    texts = [c['content'] for c in chunks]
    metadatas = [c['metadata'] for c in chunks]

    store_path = Path("storage/vector_store")
    store_path.mkdir(parents=True, exist_ok=True)

    try:
        print("\nAttempting to load existing vector store...")
        vs = FAISS.load_local(str(store_path), embeddings)
        print("✅ Loaded existing store")
        before = len(vs.docstore._dict)
        vs.add_texts(texts, metadatas=metadatas)
        after = len(vs.docstore._dict)
        print(f"✅ Added {len(texts)} documents (store size {before} -> {after})")
    except Exception as e:
        print(f"⚠️ Could not load existing store ({e}); creating new one with this URL only.")
        vs = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
        print(f"✅ New store with {len(texts)} documents")

    vs.save_local(str(store_path))
    print("\n💾 Saved vector store.")
    idx_size = (store_path / "index.faiss").stat().st_size / 1024
    pkl_size = (store_path / "index.pkl").stat().st_size / 1024
    print(f"   - index.faiss: {idx_size:.1f} KB")
    print(f"   - index.pkl:   {pkl_size:.1f} KB")

    # Quick retrieval sanity check
    print("\n[Retrieval Test]")
    query = "cosmic beginning" if "beginning" in title.lower() else title.split()[0]
    results = vs.similarity_search_with_score(query, k=2)
    for i, (doc, score) in enumerate(results, 1):
        snippet = doc.page_content[:120].replace('\n', ' ')
        print(f"  {i}. Score={score:.3f} | {snippet}...")

    print("\n✅ Single URL training complete.")
    print("Add the URL to the frontend whitelist if you want it displayed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help='Single URL to ingest')
    args = parser.parse_args()
    main(args.url)
