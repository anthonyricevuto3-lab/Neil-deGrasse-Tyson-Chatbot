"""PDF ingestion with PyPDF."""

import argparse
from pathlib import Path

from pypdf import PdfReader

from backend.rag.splitter import split_with_attribution
from backend.rag.store import add_to_store


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n\n"
    return text


def ingest_pdf(
    pdf_path: Path,
    source_name: str | None = None,
) -> list[dict]:
    """Ingest a single PDF file."""
    if source_name is None:
        source_name = pdf_path.stem

    print(f"Ingesting PDF: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)

    # Split into chunks with attribution
    chunks = split_with_attribution(
        text=text,
        source=source_name,
        metadata={"file_path": str(pdf_path)},
    )

    print(f"Created {len(chunks)} chunks")
    return chunks


def ingest_pdf_directory(
    input_dir: Path,
    output_dir: Path,
) -> None:
    """Ingest all PDFs in a directory."""
    pdf_files = list(input_dir.glob("*.pdf"))

    all_chunks = []
    for pdf_file in pdf_files:
        chunks = ingest_pdf(pdf_file)
        all_chunks.extend(chunks)

    # Add to vector store
    print(f"Adding {len(all_chunks)} total chunks to store...")
    add_to_store(all_chunks, output_dir)
    print("✅ PDF ingestion complete")


def main():
    parser = argparse.ArgumentParser(description="Ingest PDF documents")
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    ingest_pdf_directory(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
