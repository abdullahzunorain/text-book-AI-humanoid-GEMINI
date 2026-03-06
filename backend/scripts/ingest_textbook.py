"""
Textbook content ingestion script.
Reads markdown files from the Docusaurus docs folder, chunks them,
and upserts them to Qdrant vector database.

Usage:
    python ingest_textbook.py [--docs-dir PATH] [--chunk-size SIZE] [--chunk-overlap OVERLAP]
"""
import os
import re
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

from src.services.vector_store import get_qdrant_client, init_collection as init_qdrant_collection, TEXTBOOK_COLLECTION
from src.db.crud_vectors import upsert_textbook_segments_batch, get_collection_stats


# Chunking configuration
DEFAULT_CHUNK_SIZE = 500  # characters
DEFAULT_CHUNK_OVERLAP = 50  # characters


def read_markdown_file(file_path: Path) -> str:
    """
    Read a markdown file and return its content.
    
    Args:
        file_path: Path to the markdown file
    
    Returns:
        File content as string
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_frontmatter(content: str) -> Dict[str, Any]:
    """
    Extract frontmatter metadata from markdown content.
    
    Args:
        content: Markdown content
    
    Returns:
        Dictionary with metadata
    """
    metadata = {}
    
    # Check for frontmatter (YAML between ---)
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            # Simple YAML parsing for common fields
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip('"\'')
    
    return metadata


def extract_title_from_content(content: str) -> str:
    """
    Extract the title from markdown content (first # heading).
    
    Args:
        content: Markdown content
    
    Returns:
        Title or empty string
    """
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: Text to chunk
        chunk_size: Maximum chunk size in characters
        chunk_overlap: Overlap between chunks in characters
    
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        
        # If we're not at the end, try to break at a sentence or paragraph
        if end < text_length:
            # Try to break at paragraph
            break_point = text.rfind('\n\n', start, end)
            if break_point == -1 or break_point < start + chunk_size // 2:
                # Try to break at sentence
                break_point = text.rfind('. ', start, end)
            if break_point == -1 or break_point < start + chunk_size // 2:
                # Try to break at space
                break_point = text.rfind(' ', start, end)
            
            if break_point > start:
                end = break_point + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - chunk_overlap
        if start >= text_length:
            break
    
    return chunks


def extract_sections(content: str) -> List[Dict[str, str]]:
    """
    Extract sections from markdown content based on headings.
    
    Args:
        content: Markdown content
    
    Returns:
        List of dicts with 'heading' and 'content' keys
    """
    sections = []
    
    # Split by level 2 headings (##)
    parts = re.split(r'\n(?=##\s)', content)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Extract heading
        heading_match = re.match(r'^##\s+(.+)$', part, re.MULTILINE)
        if heading_match:
            heading = heading_match.group(1).strip()
            section_content = part[part.find('\n'):].strip()
            sections.append({
                'heading': heading,
                'content': section_content
            })
        else:
            # Content before first heading
            sections.append({
                'heading': 'Introduction',
                'content': part
            })
    
    return sections


def process_markdown_file(
    file_path: Path,
    docs_root: Path,
    chunk_size: int,
    chunk_overlap: int
) -> List[Dict[str, Any]]:
    """
    Process a single markdown file and return segments for ingestion.
    
    Args:
        file_path: Path to the markdown file
        docs_root: Root directory of docs
        chunk_size: Chunk size
        chunk_overlap: Chunk overlap
    
    Returns:
        List of segment dicts ready for ingestion
    """
    segments = []
    
    # Read file
    content = read_markdown_file(file_path)
    
    # Extract metadata
    frontmatter = extract_frontmatter(content)
    
    # Remove frontmatter from content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2].strip()
    
    # Extract title
    title = extract_title_from_content(content)
    if not title:
        title = frontmatter.get('title', file_path.stem)
    
    # Calculate relative path for URL
    try:
        relative_path = file_path.relative_to(docs_root)
        url = f"/docs/{relative_path.with_suffix('')}"
    except ValueError:
        url = f"/docs/{file_path.stem}"
    
    # Determine module name from path
    relative_parts = relative_path.parts if 'relative_path' in locals() else [file_path.name]
    module_name = relative_parts[0] if len(relative_parts) > 1 else "general"
    
    # Extract sections
    sections = extract_sections(content)
    
    if sections:
        # Process by sections
        for section in sections:
            section_text = f"{title}\n\n## {section['heading']}\n\n{section['content']}"
            chunks = chunk_text(section_text, chunk_size, chunk_overlap)
            
            for i, chunk in enumerate(chunks):
                segments.append({
                    'text': chunk,
                    'chapter_title': title,
                    'module_name': module_name,
                    'url': url,
                    'metadata': {
                        'section': section['heading'],
                        'chunk_index': i,
                        'total_chunks': len(chunks)
                    }
                })
    else:
        # No sections, chunk the entire content
        chunks = chunk_text(content, chunk_size, chunk_overlap)
        
        for i, chunk in enumerate(chunks):
            segments.append({
                'text': chunk,
                'chapter_title': title,
                'module_name': module_name,
                'url': url,
                'metadata': {
                    'chunk_index': i,
                    'total_chunks': len(chunks)
                }
            })
    
    return segments


def find_markdown_files(docs_dir: Path) -> List[Path]:
    """
    Find all markdown files in the docs directory.
    
    Args:
        docs_dir: Docs directory path
    
    Returns:
        List of markdown file paths
    """
    markdown_files = []
    
    for ext in ['*.md', '*.mdx']:
        markdown_files.extend(docs_dir.rglob(ext))
    
    # Filter out node_modules and build directories
    markdown_files = [
        f for f in markdown_files
        if 'node_modules' not in str(f) and 'build' not in str(f)
    ]
    
    return sorted(markdown_files)


def ingest_textbook(
    docs_dir: Path,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    clear_existing: bool = False
) -> Dict[str, Any]:
    """
    Main ingestion function.
    
    Args:
        docs_dir: Path to docs directory
        chunk_size: Chunk size in characters
        chunk_overlap: Overlap between chunks
        clear_existing: Whether to clear existing data
    
    Returns:
        Ingestion statistics
    """
    print("🔧 Starting textbook ingestion...")
    print(f"   Docs directory: {docs_dir}")
    print(f"   Chunk size: {chunk_size}")
    print(f"   Chunk overlap: {chunk_overlap}")
    
    # Initialize Qdrant
    client = get_qdrant_client()
    success = init_qdrant_collection(client)
    
    if not success:
        print("❌ Failed to initialize Qdrant collection")
        return {"status": "error", "message": "Failed to initialize Qdrant"}
    
    # Find markdown files
    markdown_files = find_markdown_files(docs_dir)
    
    if not markdown_files:
        print("⚠️  No markdown files found")
        return {"status": "warning", "message": "No markdown files found"}
    
    print(f"\n📚 Found {len(markdown_files)} markdown files")
    
    # Process files
    all_segments = []
    processed_files = 0
    total_segments = 0
    
    for file_path in markdown_files:
        print(f"   Processing: {file_path.name}...")
        
        try:
            segments = process_markdown_file(
                file_path,
                docs_dir,
                chunk_size,
                chunk_overlap
            )
            all_segments.extend(segments)
            total_segments += len(segments)
            processed_files += 1
            print(f"      → {len(segments)} segments")
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    if not all_segments:
        print("\n⚠️  No segments generated")
        return {"status": "warning", "message": "No segments generated"}
    
    # Upsert to Qdrant
    print(f"\n📤 Upserting {total_segments} segments to Qdrant...")
    
    # Process in batches of 100
    batch_size = 100
    upserted_count = 0
    
    for i in range(0, len(all_segments), batch_size):
        batch = all_segments[i:i + batch_size]
        try:
            point_ids = upsert_textbook_segments_batch(client, batch)
            upserted_count += len(point_ids)
            print(f"   Batch {i//batch_size + 1}: {len(point_ids)} segments upserted")
        except Exception as e:
            print(f"   ❌ Batch {i//batch_size + 1} failed: {e}")
    
    # Get final stats
    stats = get_collection_stats(client)
    
    result = {
        "status": "success",
        "files_processed": processed_files,
        "segments_created": total_segments,
        "segments_upserted": upserted_count,
        "collection_stats": stats
    }
    
    print(f"\n✅ Ingestion complete!")
    print(f"   Files processed: {processed_files}")
    print(f"   Segments created: {total_segments}")
    print(f"   Segments upserted: {upserted_count}")
    
    if stats["status"] == "ok":
        print(f"   Total vectors in collection: {stats.get('vectors_count', 0)}")
    
    return result


def main():
    """
    CLI entry point.
    """
    parser = argparse.ArgumentParser(
        description="Ingest textbook content into Qdrant vector database"
    )
    parser.add_argument(
        "--docs-dir",
        type=str,
        default="../frontend/docs",
        help="Path to docs directory (default: ../frontend/docs)"
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=DEFAULT_CHUNK_SIZE,
        help=f"Chunk size in characters (default: {DEFAULT_CHUNK_SIZE})"
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=DEFAULT_CHUNK_OVERLAP,
        help=f"Chunk overlap in characters (default: {DEFAULT_CHUNK_OVERLAP})"
    )
    parser.add_argument(
        "--clear-existing",
        action="store_true",
        help="Clear existing data before ingestion"
    )
    
    args = parser.parse_args()
    
    # Resolve paths
    script_dir = Path(__file__).parent
    docs_dir = Path(args.docs_dir)
    
    if not docs_dir.is_absolute():
        docs_dir = script_dir / docs_dir
    
    docs_dir = docs_dir.resolve()
    
    if not docs_dir.exists():
        print(f"❌ Docs directory not found: {docs_dir}")
        return 1
    
    # Run ingestion
    result = ingest_textbook(
        docs_dir,
        args.chunk_size,
        args.chunk_overlap,
        args.clear_existing
    )
    
    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
