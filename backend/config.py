"""
Configuration module to handle environment variables and application settings
"""
import os
from typing import List
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class to manage application settings"""

    # Cohere configuration
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")

    # OpenAI configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Qdrant configuration
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")
    QDRANT_COLLECTION_NAME: str = os.getenv("QDRANT_COLLECTION_NAME", "book_embeddings")

    # Vercel URLs to crawl (Updated from DOCUSAURUS_URLS)
    VERCEL_URLS: List[str] = os.getenv("VERCEL_URLS", "").split(",") if os.getenv("VERCEL_URLS") else []

    # Sitemap URL for discovering all pages
    SITEMAP_URL: str = os.getenv("SITEMAP_URL", "https://hackathon-i-physical-ai-humanoid-ro-tau.vercel.app/sitemap.xml")

    # Chunking parameters
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "512"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))

    # Embedding parameters
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "embed-english-v3.0")

    # Retry Logic (New)
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))

    # Checks for 'DELAY' first, falls back to 'DEPAY' (typo in env), defaults to 1
    DELAY_BETWEEN_RETRIES: int = int(os.getenv("DELAY_BETWEEN_RETRIES", os.getenv("DEPAY_BETWEEN_RETRIES", "1")))

    # Validation
    @classmethod
    def validate(cls) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []

        if not cls.COHERE_API_KEY or cls.COHERE_API_KEY.strip() == "":
            errors.append("COHERE_API_KEY is required")

        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY.strip() == "":
            errors.append("OPENAI_API_KEY is required")

        if not cls.QDRANT_URL or cls.QDRANT_URL.strip() == "":
            errors.append("QDRANT_URL is required")

        if not cls.QDRANT_API_KEY or cls.QDRANT_API_KEY.strip() == "":
            errors.append("QDRANT_API_KEY is required")

        if not cls.VERCEL_URLS or cls.VERCEL_URLS == [""] or all(url.strip() == "" for url in cls.VERCEL_URLS):
            errors.append("VERCEL_URLS is required")

        # Validate numeric values
        if cls.CHUNK_SIZE <= 0:
            errors.append("CHUNK_SIZE must be a positive integer")

        if cls.CHUNK_OVERLAP < 0:
            errors.append("CHUNK_OVERLAP must be a non-negative integer")

        if cls.CHUNK_OVERLAP >= cls.CHUNK_SIZE:
            errors.append("CHUNK_OVERLAP must be less than CHUNK_SIZE")

        if cls.MAX_RETRIES <= 0:
            errors.append("MAX_RETRIES must be a positive integer")

        if cls.DELAY_BETWEEN_RETRIES < 0:
            errors.append("DELAY_BETWEEN_RETRIES must be a non-negative integer")

        # Validate URLs
        for url in cls.VERCEL_URLS:
            if url.strip() and not url.strip().startswith(('http://', 'https://')):
                errors.append(f"URL must start with http:// or https://: {url}")

        return errors

    @classmethod
    def is_valid(cls) -> bool:
        """Check if configuration is valid"""
        return len(cls.validate()) == 0