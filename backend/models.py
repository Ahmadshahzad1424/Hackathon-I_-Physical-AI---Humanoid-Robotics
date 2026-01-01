"""
Data models for the RAG ingestion pipeline
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
import uuid


@dataclass
class CrawledPage:
    """Entity representing a crawled page from a Docusaurus site"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    url: str = ""
    title: str = ""
    content: str = ""
    metadata: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate the CrawledPage after initialization"""
        if not self.url:
            raise ValueError("URL must be provided")
        if not self.content.strip():
            raise ValueError("Content must not be empty after cleaning")
        # Title is now optional - if no title is provided, we'll use the first part of content or URL
        if not self.title.strip():
            # If no title, use first 50 chars of content or the URL as title
            if self.content.strip():
                self.title = self.content.strip()[:50] + "..." if len(self.content.strip()) > 50 else self.content.strip()
            else:
                self.title = self.url


@dataclass
class TextChunk:
    """Entity representing a chunk of text from a crawled page"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    page_id: str = ""
    content: str = ""
    chunk_index: int = 0
    token_count: int = 0
    embedding: Optional[List[float]] = None
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate the TextChunk after initialization"""
        if not self.page_id:
            raise ValueError("page_id must be provided")
        if not self.content.strip():
            raise ValueError("Content must not be empty")
        if self.chunk_index < 0:
            raise ValueError("chunk_index must be non-negative")
        if self.token_count <= 0:
            raise ValueError("token_count must be positive")

        # Check if content exceeds maximum token length for embedding model
        # (This is a simplified check - in practice, you'd use a proper token counter)
        if len(self.content) > 2048:  # Approximate max for most embedding models
            raise ValueError("Content exceeds maximum token length for embedding model")


@dataclass
class EmbeddingRecord:
    """Entity representing an embedding record in Qdrant"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    chunk_id: str = ""
    vector: List[float] = field(default_factory=list)
    collection_name: str = ""
    payload: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Validate the EmbeddingRecord after initialization"""
        if not self.chunk_id:
            raise ValueError("chunk_id must be provided")
        if not self.vector:
            raise ValueError("vector must not be empty")
        if not self.collection_name:
            raise ValueError("collection_name must be provided")
        if not self.payload:
            raise ValueError("payload must not be empty")


@dataclass
class ProcessingJob:
    """Entity representing a processing job for the ingestion pipeline"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "PENDING"  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    urls: List[str] = field(default_factory=list)
    processed_count: int = 0
    total_count: int = 0
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate the ProcessingJob after initialization"""
        valid_statuses = ["PENDING", "IN_PROGRESS", "COMPLETED", "FAILED"]
        if self.status not in valid_statuses:
            raise ValueError(f"status must be one of {valid_statuses}")

        if self.processed_count > self.total_count:
            raise ValueError("processed_count must not exceed total_count")

        if self.error_message and self.status != "FAILED":
            raise ValueError("error_message should only be present when status is FAILED")