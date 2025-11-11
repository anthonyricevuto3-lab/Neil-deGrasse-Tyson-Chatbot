"""
Train the chatbot by ingesting NDT content from curated URLs and text corpus.
Handles both web scraping and text file ingestion.
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple
import time

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

import requests
from bs4 import BeautifulSoup
import trafilatura
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Set API key
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 
    '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'
)
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

def fetch_url_content(url: str) -> Tuple[str, str, bool]:
    """
    Fetch content from URL using multiple methods.
    Returns: (text_content, title, success)
    """
    print(f"\n  Fetching: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    try:
        # Try with requests
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Try trafilatura first (best for article extraction)
        text = trafilatura.extract(response.text, include_comments=False)
        
        if text and len(text) > 500:
            # Get title with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else url.split('/')[-1]
            title = title.strip()
            
            print(f"  ✅ Success via trafilatura: {len(text):,} chars, title: {title}")
            return text, title, True
        
        # Fallback to BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator='\n', strip=True)
        
        # Clean up whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n'.join(lines)
        
        title = soup.title.string if soup.title else url.split('/')[-1]
        title = title.strip()
        
        if len(text) > 500:
            print(f"  ✅ Success via BeautifulSoup: {len(text):,} chars")
            return text, title, True
        else:
            print(f"  ⚠️  Warning: Content too short ({len(text)} chars)")
            return "", "", False
            
    except requests.exceptions.HTTPError as e:
        print(f"  ❌ HTTP Error {e.response.status_code}")
        return "", "", False
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Request failed: {str(e)[:100]}")
        return "", "", False
    except Exception as e:
        print(f"  ❌ Error: {str(e)[:100]}")
        return "", "", False

def load_urls_from_file(filepath: Path) -> List[str]:
    """Load URLs from text file, one per line."""
    urls = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)
    return urls

def chunk_text(text: str, metadata: dict, chunk_size: int = 800) -> List[dict]:
    """Split text into semantic chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = splitter.split_text(text)
    
    return [
        {
            'content': chunk.strip(),
            'metadata': metadata.copy()
        }
        for chunk in chunks
        if len(chunk.strip()) > 200  # Only keep substantial chunks
    ]

def main():
    """Main training pipeline."""
    
    print("=" * 80)
    print("TRAINING NEIL DEGRASSE TYSON CHATBOT")
    print("=" * 80)
    
    all_chunks = []
    
    # Step 1: Load and process text corpus
    print("\n[STEP 1] Processing text corpus...")
    corpus_path = Path("data/docs/ndt_training_corpus.txt")
    
    if corpus_path.exists():
        print(f"  Reading: {corpus_path}")
        with open(corpus_path, 'r', encoding='utf-8') as f:
            corpus_text = f.read()
        
        print(f"  Loaded {len(corpus_text):,} characters")
        
        # Parse sections
        sections = []
        current_section = []
        current_metadata = {'source': 'https://haydenplanetarium.org/tyson'}
        
        for line in corpus_text.split('\n'):
            if line.startswith('## SECTION'):
                if current_section:
                    content = '\n'.join(current_section)
                    if len(content) > 200:
                        sections.append({'content': content, 'metadata': current_metadata.copy()})
                current_section = [line]
                section_title = line.replace('## SECTION', '').strip().strip(':').strip('0123456789').strip()
                current_metadata = {
                    'source': 'https://haydenplanetarium.org/tyson',
                    'section': section_title,
                    'title': section_title
                }
            elif line.startswith('### '):
                topic = line.replace('###', '').strip()
                current_metadata['topic'] = topic
                current_metadata['title'] = f"{current_metadata.get('section', '')}: {topic}".strip(': ')
                current_section.append(line)
            elif line.startswith('URL:'):
                url = line.replace('URL:', '').strip()
                current_metadata['source'] = url
                current_section.append(line)
            else:
                current_section.append(line)
        
        # Add last section
        if current_section:
            content = '\n'.join(current_section)
            if len(content) > 200:
                sections.append({'content': content, 'metadata': current_metadata})
        
        print(f"  ✅ Parsed {len(sections)} sections from corpus")
        
        # Chunk sections
        for section in sections:
            chunks = chunk_text(section['content'], section['metadata'])
            all_chunks.extend(chunks)
        
        print(f"  ✅ Created {len(all_chunks)} chunks from corpus")
    else:
        print(f"  ⚠️  Corpus not found at {corpus_path}")
    
    # Step 2: Scrape URLs
    print("\n[STEP 2] Scraping training URLs...")
    urls_file = Path("data/urls/training_urls.txt")
    
    if urls_file.exists():
        urls = load_urls_from_file(urls_file)
        print(f"  Loaded {len(urls)} URLs")
        
        successful = 0
        failed = 0
        
        for i, url in enumerate(urls, 1):
            print(f"\n  [{i}/{len(urls)}]", end="")
            
            text, title, success = fetch_url_content(url)
            
            if success:
                # Extract domain for metadata
                domain = url.split('/')[2]
                
                metadata = {
                    'source': url,
                    'url': url,
                    'title': title,
                    'domain': domain
                }
                
                # Chunk the content
                chunks = chunk_text(text, metadata, chunk_size=1000)
                all_chunks.extend(chunks)
                successful += 1
                
                print(f"  ✅ Added {len(chunks)} chunks from {domain}")
            else:
                failed += 1
            
            # Be polite - delay between requests
            if i < len(urls):
                time.sleep(1)
        
        print(f"\n  ✅ Successfully scraped {successful}/{len(urls)} URLs")
        if failed > 0:
            print(f"  ⚠️  Failed to scrape {failed} URLs")
    else:
        print(f"  ⚠️  URLs file not found at {urls_file}")
    
    # Step 3: Create embeddings and build vector store
    print(f"\n[STEP 3] Building vector store from {len(all_chunks)} total chunks...")
    
    if len(all_chunks) == 0:
        print("  ❌ No content to process! Exiting.")
        return
    
    print(f"  Creating embeddings (this may take a while)...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    texts = [chunk['content'] for chunk in all_chunks]
    metadatas = [chunk['metadata'] for chunk in all_chunks]
    
    # Create vector store
    store_path = Path("storage/vector_store")
    
    try:
        print(f"  Attempting to load existing store...")
        vectorstore = FAISS.load_local(str(store_path), embeddings)
        print(f"  ✅ Loaded existing store")
        
        print(f"  Adding {len(texts)} new documents...")
        vectorstore.add_texts(texts, metadatas=metadatas)
        print(f"  ✅ Merged with existing store")
        
    except Exception as e:
        print(f"  Creating new store...")
        vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
        print(f"  ✅ Created new store with {len(texts)} documents")
    
    # Save
    print(f"\n[STEP 4] Saving vector store to {store_path}...")
    store_path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(store_path))
    
    faiss_size = (store_path / "index.faiss").stat().st_size / 1024
    pkl_size = (store_path / "index.pkl").stat().st_size / 1024
    print(f"  ✅ Saved!")
    print(f"     - FAISS index: {faiss_size:.1f} KB")
    print(f"     - PKL file: {pkl_size:.1f} KB")
    
    # Step 5: Test retrieval
    print("\n[STEP 5] Testing retrieval...")
    
    test_queries = [
        "Why are we made of stardust?",
        "What is a black hole?",
        "Should we go to Mars?",
        "What is the cosmic perspective?"
    ]
    
    for query in test_queries:
        print(f"\n  Query: '{query}'")
        results = vectorstore.similarity_search_with_score(query, k=2)
        
        for i, (doc, score) in enumerate(results, 1):
            print(f"    {i}. Score: {score:.3f} | {doc.metadata.get('title', 'Unknown')[:60]}")
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ TRAINING COMPLETE!")
    print("=" * 80)
    print(f"\nVector store contains {len(texts)} knowledge chunks")
    print(f"Sources: {len(set(chunk['metadata'].get('source', '') for chunk in all_chunks))} unique URLs")
    print("\nNext steps:")
    print("  1. Start server: uvicorn backend.app:app --port 8000")
    print("  2. Test: python final_test.py")
    print("  3. Or visit: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
