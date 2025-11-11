"""Ingest training corpus into vector store."""

import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Set API key from environment
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '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')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

def ingest_training_corpus():
    """Read training corpus and add to vector store."""
    
    print("=" * 70)
    print("INGESTING NDT TRAINING CORPUS")
    print("=" * 70)
    
    # Read the training corpus
    corpus_path = Path("data/docs/ndt_training_corpus.txt")
    print(f"\n[1/5] Reading corpus from {corpus_path}...")
    
    with open(corpus_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"✅ Loaded {len(text):,} characters")
    
    # Split into sections by headers
    print("\n[2/5] Splitting into chunks...")
    sections = []
    current_section = []
    current_metadata = {}
    
    for line in text.split('\n'):
        # New section marker
        if line.startswith('## SECTION'):
            if current_section:
                sections.append({
                    'content': '\n'.join(current_section),
                    'metadata': current_metadata.copy()
                })
            current_section = [line]
            section_title = line.replace('## SECTION', '').strip().strip(':').strip('0123456789').strip()
            current_metadata = {'section': section_title}
        
        # Subsection (topic)
        elif line.startswith('### '):
            topic = line.replace('###', '').strip()
            current_metadata['topic'] = topic
            current_section.append(line)
        
        # Source line
        elif line.startswith('Source:'):
            current_metadata['source_description'] = line.replace('Source:', '').strip()
            current_section.append(line)
        
        # URL line
        elif line.startswith('URL:'):
            url = line.replace('URL:', '').strip()
            current_metadata['source'] = url
            current_metadata['url'] = url
            current_section.append(line)
        
        else:
            current_section.append(line)
    
    # Add last section
    if current_section:
        sections.append({
            'content': '\n'.join(current_section),
            'metadata': current_metadata
        })
    
    print(f"✅ Created {len(sections)} sections")
    
    # Further split long sections
    print("\n[3/5] Creating semantic chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    all_chunks = []
    for section in sections:
        if len(section['content']) > 1000:
            # Split long sections
            sub_chunks = text_splitter.split_text(section['content'])
            for chunk in sub_chunks:
                if len(chunk.strip()) > 100:  # Only keep substantial chunks
                    all_chunks.append({
                        'content': chunk.strip(),
                        'metadata': section['metadata']
                    })
        else:
            if len(section['content'].strip()) > 100:
                all_chunks.append(section)
    
    print(f"✅ Created {len(all_chunks)} chunks")
    
    # Create embeddings
    print("\n[4/5] Generating embeddings...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    
    texts = [chunk['content'] for chunk in all_chunks]
    metadatas = [chunk['metadata'] for chunk in all_chunks]
    
    # Add title to metadata
    for i, chunk in enumerate(all_chunks):
        topic = chunk['metadata'].get('topic', '')
        section = chunk['metadata'].get('section', '')
        title = f"{section}: {topic}" if topic else section
        metadatas[i]['title'] = title
    
    # Create or update vector store
    store_path = Path("storage/vector_store")
    
    try:
        # Try loading existing store
        print(f"   Attempting to load existing store from {store_path}...")
        vectorstore = FAISS.load_local(str(store_path), embeddings)
        print(f"   ✅ Loaded existing store")
        
        # Add new documents
        print(f"   Adding {len(texts)} new documents...")
        vectorstore.add_texts(texts, metadatas=metadatas)
        print(f"   ✅ Added documents to existing store")
        
    except Exception as e:
        print(f"   Creating new store (couldn't load existing: {e})")
        vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
        print(f"   ✅ Created new store with {len(texts)} documents")
    
    # Save
    print(f"\n[5/5] Saving vector store to {store_path}...")
    store_path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(store_path))
    
    # Verify
    faiss_size = (store_path / "index.faiss").stat().st_size / 1024
    print(f"✅ Saved! FAISS index size: {faiss_size:.1f} KB")
    
    # Test search
    print("\n" + "=" * 70)
    print("TESTING RETRIEVAL")
    print("=" * 70)
    
    test_query = "Why are we made of stardust?"
    print(f"\nQuery: '{test_query}'")
    results = vectorstore.similarity_search_with_score(test_query, k=3)
    
    print(f"\nTop 3 results:")
    for i, (doc, score) in enumerate(results, 1):
        print(f"\n{i}. Score: {score:.3f}")
        print(f"   Title: {doc.metadata.get('title', 'Unknown')}")
        print(f"   Preview: {doc.page_content[:150]}...")
    
    print("\n" + "=" * 70)
    print("✅ TRAINING COMPLETE!")
    print("=" * 70)
    print(f"\nVector store now contains {len(texts)} chunks of NDT knowledge.")
    print("\nNext steps:")
    print("1. Start the server: uvicorn backend.app:app --port 8000")
    print("2. Test with: python final_test.py")
    print("3. Or visit: http://localhost:8000/docs")

if __name__ == "__main__":
    ingest_training_corpus()
