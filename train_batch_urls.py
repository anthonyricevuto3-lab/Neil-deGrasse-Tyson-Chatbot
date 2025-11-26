"""
Batch-ingest a set of Neil deGrasse Tyson URLs into the FAISS vector store.
Usage:
  python train_batch_urls.py
The URL list is embedded below per user request.
"""
import os
from pathlib import Path
from typing import List, Tuple
import time

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

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache'
}

URLS: List[str] = [
    "https://neildegrassetyson.com/essays/2002-05-on-being-baffled/",
    "https://neildegrassetyson.com/essays/1998-10-certain-uncertainties-part-1/",
    "https://neildegrassetyson.com/essays/2004-04-launching-the-right-stuff/",
    "https://neildegrassetyson.com/essays/1996-07-onward-to-the-edge/",
    "https://neildegrassetyson.com/essays/2005-06-fueling-up/",
    "https://neildegrassetyson.com/essays/1996-11-outward-bound/",
    "https://neildegrassetyson.com/essays/2005-07-heading-out/",
    "https://neildegrassetyson.com/essays/1998-11-certain-uncertainties-part-2/",
    "https://neildegrassetyson.com/essays/2008-04-spacecraft-behaving-badly/",
    "https://neildegrassetyson.com/essays/2001-03-coming-to-our-senses/",
    "https://neildegrassetyson.com/essays/2001-09-over-the-rainbow/",
    "https://neildegrassetyson.com/essays/2002-03-colors-of-the-cosmos/",
    "https://neildegrassetyson.com/essays/2007-06-plutos-requiem/",
    "https://neildegrassetyson.com/commentary/2022-11-17-navigate-arguments-during-holidays/",
    "https://neildegrassetyson.com/commentary/2022-05-04-few-words-on-abortion/",
    "https://neildegrassetyson.com/commentary/2021-03-18-because-of-science/",
    "https://neildegrassetyson.com/commentary/2020-06-03-reflections-on-color-of-my-skin/",
    "https://neildegrassetyson.com/commentary/2019-09-25-hawaiis-conduit-to-cosmos/",
    "https://neildegrassetyson.com/commentary/2017-04-21-science-in-america/",
    "https://neildegrassetyson.com/commentary/2016-08-07-reflections-on-rationalia/",
    "https://neildegrassetyson.com/commentary/2016-01-23-what-science-is/",
    "https://neildegrassetyson.com/commentary/2015-12-17-dark-matter/",
    "https://neildegrassetyson.com/commentary/2012-03-07-past-present-and-future-of-nasa/",
    "https://neildegrassetyson.com/commentary/2011-08-21-if-i-were-president/",
    "https://neildegrassetyson.com/commentary/2008-06-22-for-the-love-of-hubble/",
    "https://neildegrassetyson.com/commentary/2008-06-06-vote-by-numbers/",
    "https://neildegrassetyson.com/commentary/2007-08-05-why-america-needs-to-explore-space/",
    "https://neildegrassetyson.com/commentary/2002-11-25-where-even-the-sky-is-no-limit/",
    "https://neildegrassetyson.com/commentary/2001-01-01-destiny-in-space/",
    "https://neildegrassetyson.com/commentary/1998-07-22-misaligned-stars/",
]


def fetch(url: str) -> Tuple[str, str, bool]:
    print(f"\nFetching: {url}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code >= 400:
            print(f"  ❌ HTTP {r.status_code}")
            return "", "", False
        txt = trafilatura.extract(r.text, include_comments=False)
        if txt and len(txt) > 400:
            soup = BeautifulSoup(r.text, 'html.parser')
            title = (soup.title.string if soup.title else url.split('/')[-1]).strip()
            print(f"  ✅ trafilatura {len(txt)} chars")
            return txt, title, True
        # fallback
        soup = BeautifulSoup(r.text, 'html.parser')
        for tag in soup(['script','style','nav','footer','header']):
            tag.decompose()
        text2 = '\n'.join([ln.strip() for ln in soup.get_text('\n').split('\n') if ln.strip()])
        if len(text2) > 400:
            title = (soup.title.string if soup.title else url.split('/')[-1]).strip()
            print(f"  ✅ BeautifulSoup {len(text2)} chars")
            return text2, title, True
        print("  ⚠️ Too little content")
        return "", "", False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return "", "", False


def chunk(text: str, metadata: dict) -> List[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=120,
        separators=["\n\n","\n",". "," ",""]
    )
    parts = splitter.split_text(text)
    return [{"content": p.strip(), "metadata": metadata.copy()} for p in parts if len(p.strip()) >= 120]


def main():
    all_chunks: List[dict] = []
    successes = 0
    failures = 0

    # Deduplicate
    uniq_urls = []
    seen = set()
    for u in URLS:
        if u not in seen:
            uniq_urls.append(u)
            seen.add(u)

    print(f"Processing {len(uniq_urls)} URLs (deduplicated)")

    for i, url in enumerate(uniq_urls, 1):
        print(f"  [{i}/{len(uniq_urls)}]")
        text, title, ok = fetch(url)
        if not ok:
            failures += 1
        else:
            metadata = {"source": url, "url": url, "title": title, "domain": url.split('/')[2]}
            pieces = chunk(text, metadata)
            all_chunks.extend(pieces)
            successes += 1
            print(f"  ✅ Added {len(pieces)} chunks")
        time.sleep(0.8)

    print(f"\nSummary: {successes} success, {failures} failed")
    if not all_chunks:
        print("❌ No chunks to embed; exiting")
        return

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    texts = [c['content'] for c in all_chunks]
    metas = [c['metadata'] for c in all_chunks]

    store_path = Path("storage/vector_store")
    store_path.mkdir(parents=True, exist_ok=True)

    try:
        print("Loading existing store...")
        vs = FAISS.load_local(str(store_path), embeddings)
        before = len(vs.docstore._dict)
        vs.add_texts(texts, metadatas=metas)
        after = len(vs.docstore._dict)
        print(f"✅ Store size {before} -> {after}")
    except Exception as e:
        print(f"Creating new store: {e}")
        vs = FAISS.from_texts(texts, embeddings, metadatas=metas)
        print(f"✅ New store with {len(texts)} documents")

    vs.save_local(str(store_path))
    print("💾 Saved vector store.")
    idx = (store_path/"index.faiss").stat().st_size/1024
    pkl = (store_path/"index.pkl").stat().st_size/1024
    print(f"   - index.faiss: {idx:.1f} KB")
    print(f"   - index.pkl:   {pkl:.1f} KB")

    print("\nDone.")


if __name__ == "__main__":
    main()
