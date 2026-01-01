"""
Text chunking class to split content into manageable chunks for embedding
"""
import re
import logging
from typing import List
from models import TextChunk, CrawledPage


logger = logging.getLogger(__name__)


class TextChunker:
    """Class to handle text chunking for embedding preparation"""

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        """
        Initialize the chunker with size and overlap settings

        Args:
            chunk_size: Maximum size of each chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_page(self, page: CrawledPage) -> List[TextChunk]:
        """
        Chunk a single crawled page into multiple text chunks

        Args:
            page: CrawledPage object to chunk

        Returns:
            List of TextChunk objects
        """
        if not page.content.strip():
            logger.warning(f"Page {page.id} has no content to chunk")
            return []

        logger.info(f"Starting to chunk page: {page.title} (id: {page.id})")

        # Split the content into chunks
        content_chunks = self._split_content(page.content)

        logger.info(f"Page {page.title} split into {len(content_chunks)} initial chunks")

        # Create TextChunk objects
        text_chunks = []
        for idx, chunk_content in enumerate(content_chunks):
            text_chunk = TextChunk(
                page_id=page.id,
                content=chunk_content,
                chunk_index=idx,
                token_count=len(chunk_content)  # Approximate token count
            )
            text_chunks.append(text_chunk)

        logger.info(f"Created {len(text_chunks)} TextChunk objects for page: {page.title}")
        return text_chunks

    def _split_content(self, content: str) -> List[str]:
        """
        Split content into chunks based on semantic boundaries

        Args:
            content: Content to split

        Returns:
            List of content chunks
        """
        # First, try to split by semantic boundaries (headings, paragraphs)
        chunks = self._split_by_semantic_boundaries(content)

        # If any chunks are still too large, split them further
        final_chunks = []
        for chunk in chunks:
            if len(chunk) <= self.chunk_size:
                final_chunks.append(chunk)
            else:
                # Split large chunks further using sliding window
                sub_chunks = self._split_large_chunk(chunk)
                final_chunks.extend(sub_chunks)

        return final_chunks

    def _split_by_semantic_boundaries(self, content: str) -> List[str]:
        """
        Split content by semantic boundaries like headings and paragraphs

        Args:
            content: Content to split

        Returns:
            List of content chunks split by semantic boundaries
        """
        # Split by common heading patterns
        # This regex looks for common heading patterns in documentation
        heading_pattern = r'(\n\s*#+\s+.*?\n|\n\s*={2,}\s*\n|\n\s*-+\s*\n)'
        parts = re.split(heading_pattern, content)

        # Group parts back together to form coherent chunks
        chunks = []
        current_chunk = ""

        for part in parts:
            # Check if this part is a heading
            if re.match(r'(\n\s*#+\s+.*?\n|\n\s*={2,}\s*\n|\n\s*-+\s*\n)', part):
                # If current chunk would be too large with this heading, start a new chunk
                if len(current_chunk) + len(part) > self.chunk_size and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = part
                else:
                    current_chunk += part
            else:
                # If adding this part would exceed chunk size, start a new chunk
                if len(current_chunk) + len(part) > self.chunk_size and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = part
                else:
                    current_chunk += part

        # Add the last chunk if it exists
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # Filter out empty chunks
        chunks = [chunk for chunk in chunks if chunk.strip()]

        return chunks

    def _split_large_chunk(self, chunk: str) -> List[str]:
        """
        Split a large chunk using a sliding window approach

        Args:
            chunk: Large chunk to split

        Returns:
            List of smaller chunks
        """
        if len(chunk) <= self.chunk_size:
            return [chunk]

        chunks = []
        start = 0

        while start < len(chunk):
            # Determine the end position
            end = start + self.chunk_size

            # If this is not the last chunk, try to break at a sentence or word boundary
            if end < len(chunk):
                # Look for a good breaking point near the end
                search_start = end - self.chunk_overlap
                break_point = end

                # Look for sentence endings
                for i in range(min(end, len(chunk)) - 1, search_start - 1, -1):
                    if chunk[i] in '.!?':
                        break_point = i + 1
                        break
                else:
                    # If no sentence ending found, look for whitespace
                    for i in range(min(end, len(chunk)) - 1, search_start - 1, -1):
                        if chunk[i] in ' \t\n':
                            break_point = i + 1
                            break
                    else:
                        # If no good break point found, just break at the limit
                        break_point = end

                chunks.append(chunk[start:break_point])
                start = break_point - self.chunk_overlap
            else:
                # This is the last chunk
                chunks.append(chunk[start:])
                break

        # Filter out empty chunks
        chunks = [chunk for chunk in chunks if chunk.strip()]

        return chunks