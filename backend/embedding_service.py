"""
Embedding service class to handle embedding generation using Cohere
"""
import cohere
import logging
from typing import List, Optional
from config import Config
from models import TextChunk, EmbeddingRecord


logger = logging.getLogger(__name__)


class EmbeddingService:
    """Class to handle embedding generation using Cohere API"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the embedding service

        Args:
            api_key: Cohere API key (if not provided, will use Config.COHERE_API_KEY)
            model: Embedding model name (if not provided, will use Config.EMBEDDING_MODEL)
        """
        self.api_key = api_key or Config.COHERE_API_KEY
        self.model = model or Config.EMBEDDING_MODEL

        if not self.api_key:
            raise ValueError("Cohere API key is required")

        self.client = cohere.Client(self.api_key)

    def generate_embeddings(self, chunks: List[TextChunk]) -> List[EmbeddingRecord]:
        """
        Generate embeddings for a list of text chunks

        Args:
            chunks: List of TextChunk objects to generate embeddings for

        Returns:
            List of EmbeddingRecord objects with generated embeddings
        """
        if not chunks:
            logger.warning("No text chunks provided for embedding generation")
            return []

        logger.info(f"Generating embeddings for {len(chunks)} text chunks using model: {self.model}")

        # Process embeddings in smaller batches to reduce rate limiting
        embedding_records = []

        # Process one chunk at a time to be more conservative with API limits
        for i, chunk in enumerate(chunks):
            logger.info(f"Processing embedding for chunk {i+1}/{len(chunks)}")

            # Implement retry logic for rate limiting
            max_retries = Config.MAX_RETRIES
            for attempt in range(max_retries):
                try:
                    # Generate embeddings using Cohere for a single text
                    response = self.client.embed(
                        texts=[chunk.content],
                        model=self.model,
                        input_type="search_document"  # Using search_document as default input type
                    )

                    embeddings = response.embeddings

                    # Validate the embedding before creating the record
                    if not self.validate_embedding(embeddings[0]):
                        logger.warning(f"Invalid embedding generated for chunk {chunk.id}, skipping...")
                        break  # Move to the next chunk

                    embedding_record = EmbeddingRecord(
                        chunk_id=chunk.id,
                        vector=embeddings[0],
                        collection_name=Config.QDRANT_COLLECTION_NAME,
                        payload={
                            "source_url": chunk.metadata.get("source_url", "") if hasattr(chunk, 'metadata') else "",
                            "chunk_index": chunk.chunk_index,
                            "content": chunk.content[:100] + "..." if len(chunk.content) > 100 else chunk.content,  # Truncate for payload
                            "page_id": chunk.page_id
                        }
                    )
                    embedding_records.append(embedding_record)
                    logger.info(f"Successfully generated embedding for chunk {chunk.id}")

                    # Add a delay between requests to be more respectful to the API
                    import time
                    time.sleep(Config.DELAY_BETWEEN_RETRIES * 2)  # Use the configured delay with a multiplier for better rate limiting

                    break  # Success, move to the next chunk

                except Exception as e:
                    logger.error(f"Error generating embedding for chunk {chunk.id} (attempt {attempt + 1}/{max_retries}): {str(e)}")

                    # Check if it's a rate limit error and implement backoff
                    if "429" in str(e) or "rate limit" in str(e).lower() or "Please wait and try again later" in str(e):
                        if attempt < max_retries - 1:  # Don't sleep on the last attempt
                            import time
                            wait_time = Config.DELAY_BETWEEN_RETRIES * (2 ** attempt)  # Exponential backoff
                            logger.info(f"Rate limited. Waiting {wait_time} seconds before retry {attempt + 2}/{max_retries}")
                            time.sleep(wait_time)
                            continue

                    # If it's not a rate limit error or we've exhausted retries, move to next chunk
                    if attempt == max_retries - 1:
                        logger.error(f"Failed to generate embedding for chunk {chunk.id} after {max_retries} attempts")
                        break
                    else:
                        import time
                        wait_time = Config.DELAY_BETWEEN_RETRIES * (2 ** attempt)  # Exponential backoff
                        logger.info(f"Waiting {wait_time} seconds before retry {attempt + 2}/{max_retries}")
                        time.sleep(wait_time)

        logger.info(f"Successfully generated embeddings for {len(embedding_records)} chunks out of {len(chunks)}")
        return embedding_records

    def generate_embedding_batch(self, texts: List[str], batch_size: int = 96) -> List[List[float]]:
        """
        Generate embeddings for a large list of texts in batches

        Args:
            texts: List of text strings to generate embeddings for
            batch_size: Number of texts to process in each batch (Cohere has limits)

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            logger.info(f"Processing embedding batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")

            # Implement retry logic for rate limiting
            max_retries = Config.MAX_RETRIES
            for attempt in range(max_retries):
                try:
                    response = self.client.embed(
                        texts=batch,
                        model=self.model,
                        input_type="search_document"
                    )
                    all_embeddings.extend(response.embeddings)
                    break  # Success, break out of retry loop
                except Exception as e:
                    logger.error(f"Error generating embeddings for batch {i//batch_size + 1} (attempt {attempt + 1}/{max_retries}): {str(e)}")

                    # Check if it's a rate limit error and implement backoff
                    if "429" in str(e) or "rate limit" in str(e).lower() or "Please wait and try again later" in str(e):
                        if attempt < max_retries - 1:  # Don't sleep on the last attempt
                            import time
                            wait_time = Config.DELAY_BETWEEN_RETRIES * (2 ** attempt)  # Exponential backoff
                            logger.info(f"Rate limited. Waiting {wait_time} seconds before retry {attempt + 2}/{max_retries}")
                            time.sleep(wait_time)
                            continue

                    # If it's not a rate limit error or we've exhausted retries, re-raise
                    if attempt == max_retries - 1:  # Last attempt
                        raise
                    else:
                        import time
                        wait_time = Config.DELAY_BETWEEN_RETRIES * (2 ** attempt)  # Exponential backoff
                        logger.info(f"Waiting {wait_time} seconds before retry {attempt + 2}/{max_retries}")
                        time.sleep(wait_time)

        return all_embeddings

    def validate_embedding(self, embedding: List[float]) -> bool:
        """
        Validate that an embedding is properly formed

        Args:
            embedding: Embedding vector to validate

        Returns:
            True if embedding is valid, False otherwise
        """
        if not embedding:
            return False

        if not isinstance(embedding, list):
            return False

        # Check if all elements are numbers
        if not all(isinstance(val, (int, float)) for val in embedding):
            return False

        # Embeddings should have consistent dimensions (though we don't know the exact expected size)
        if len(embedding) == 0:
            return False

        return True