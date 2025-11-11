"""Quick demo script to create sample knowledge base and test the chatbot."""

import os
from pathlib import Path

# Sample NDT-style content for testing
SAMPLE_CONTENT = [
    {
        "text": """Neil deGrasse Tyson often explains that we are made of stardust. This isn't just poetry—it's scientific fact. The atoms that make up our bodies, particularly the heavy elements like carbon, nitrogen, and oxygen, were forged in the cores of massive stars billions of years ago. When those stars exploded as supernovae, they scattered these elements across the galaxy. Over time, those atoms came together to form new stars, planets, and eventually us. As Tyson loves to say, "We are not figuratively, but literally stardust." This cosmic perspective reminds us of our deep connection to the universe.""",
        "source": "https://example.com/stardust",
        "title": "Stardust Explanation"
    },
    {
        "text": """Black holes are regions of spacetime where gravity is so strong that nothing, not even light, can escape. They form when massive stars collapse at the end of their life cycles. The boundary around a black hole is called the event horizon—cross that line, and there's no coming back. Neil deGrasse Tyson describes them as "the universe's ultimate one-way ticket." Despite their name, black holes aren't actually holes—they're incredibly dense objects with mass compressed into an infinitesimally small space. Einstein's theory of general relativity predicts their existence, and we've now observed them directly through gravitational wave detection and imaging.""",
        "source": "https://example.com/blackholes",
        "title": "Black Hole Basics"
    },
    {
        "text": """The universe began approximately 13.8 billion years ago with the Big Bang. This wasn't an explosion in space, but rather an expansion of space itself. In the first fraction of a second, the universe underwent rapid inflation, expanding faster than the speed of light. As it cooled, fundamental particles formed, then atoms, and eventually stars and galaxies. Neil deGrasse Tyson emphasizes that the Big Bang theory is supported by multiple lines of evidence: the cosmic microwave background radiation, the abundance of light elements, and the observed expansion of the universe. We're still learning about what triggered the Big Bang and what, if anything, came before it.""",
        "source": "https://example.com/bigbang",
        "title": "Big Bang Theory"
    },
    {
        "text": """Dark matter is a mysterious substance that makes up about 27% of the universe's mass-energy content, yet we can't see it directly. We know it exists because of its gravitational effects on visible matter—galaxies rotate too fast to be held together by just the matter we can see. Dark matter doesn't emit, absorb, or reflect light, making it invisible to our telescopes. Neil deGrasse Tyson calls it "the most humbling discovery in modern astrophysics" because it reminds us that most of the universe is made of something we don't yet understand. Scientists are actively searching for dark matter particles using sensitive detectors deep underground.""",
        "source": "https://example.com/darkmatter",
        "title": "Dark Matter Mystery"
    },
    {
        "text": """In 2006, Pluto was reclassified from a planet to a "dwarf planet" by the International Astronomical Union. This wasn't about demoting Pluto, but about creating clear definitions. To be a full planet, an object must orbit the Sun, be massive enough to be rounded by its own gravity, and have "cleared its neighborhood" of other debris. Pluto meets the first two criteria but not the third—it shares its orbital zone with thousands of other objects in the Kuiper Belt. Neil deGrasse Tyson, who was involved in this decision as director of the Hayden Planetarium, reminds us that science isn't about nostalgia. As we discover more about the universe, our classifications evolve. Pluto is still fascinating, just in a different category.""",
        "source": "https://example.com/pluto",
        "title": "Pluto Reclassification"
    }
]


def create_sample_vectorstore():
    """Create a sample vector store with NDT-style content."""
    from dotenv import load_dotenv
    from langchain.schema import Document
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    from backend.settings import get_settings
    
    # Load environment variables
    load_dotenv()
    
    settings = get_settings()
    
    # Create documents
    documents = []
    for item in SAMPLE_CONTENT:
        doc = Document(
            page_content=item["text"],
            metadata={
                "source": item["source"],
                "title": item["title"],
                "domain": "example.com"
            }
        )
        documents.append(doc)
    
    print(f"Creating vector store with {len(documents)} sample documents...")
    
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        openai_api_key=settings.openai_api_key
    )
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    # Save
    output_path = Path(settings.vector_store_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(output_path))
    
    print(f"✅ Sample vector store created at {output_path}")
    print("\nTopics covered:")
    for item in SAMPLE_CONTENT:
        print(f"  - {item['title']}")


if __name__ == "__main__":
    create_sample_vectorstore()
