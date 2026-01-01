"""
Qdrant service class to handle vector storage in Qdrant Cloud
"""
import logging
from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from config import Config
from models import EmbeddingRecord


logger = logging.getLogger(__name__)


class QdrantService:
    """Class to handle vector storage in Qdrant Cloud"""

    def __init__(self, url: Optional[str] = None, api_key: Optional[str] = None, collection_name: Optional[str] = None):
        """
        Initialize the Qdrant service

        Args:
            url: Qdrant Cloud URL (if not provided, will use Config.QDRANT_URL)
            api_key: Qdrant API key (if not provided, will use Config.QDRANT_API_KEY)
            collection_name: Collection name (if not provided, will use Config.QDRANT_COLLECTION_NAME)
        """
        self.url = url or Config.QDRANT_URL
        self.api_key = api_key or Config.QDRANT_API_KEY
        self.collection_name = collection_name or Config.QDRANT_COLLECTION_NAME

        if not self.url or not self.api_key:
            raise ValueError("Qdrant URL and API key are required")

        # Initialize Qdrant client
        self.client = QdrantClient(
            url=self.url,
            api_key=self.api_key,
            prefer_grpc=False  # Using REST API for better compatibility
        )

    def create_collection(self, vector_size: int = 1024, distance: str = "Cosine") -> bool:
        """
        Create a collection in Qdrant for storing embeddings

        Args:
            vector_size: Size of the embedding vectors (default 1024 for Cohere embeddings)
            distance: Distance metric to use (default "Cosine")

        Returns:
            True if collection was created successfully, False otherwise
        """
        try:
            # Check if collection already exists
            collections = self.client.get_collections()
            existing_collection_names = [c.name for c in collections.collections]

            if self.collection_name in existing_collection_names:
                logger.info(f"Collection '{self.collection_name}' already exists")
                return True

            # Create new collection with indexing configuration for efficient search
            distance_enum = Distance.COSINE if distance.upper() == "COSINE" else Distance.DOT

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=distance_enum),
                # Configure indexing for efficient search
                optimizers_config=models.OptimizersConfigDiff(
                    indexing_threshold=20000,  # Index vectors in batch for better performance
                    max_optimization_threads=1  # Limit optimization threads
                )
            )

            logger.info(f"Collection '{self.collection_name}' created successfully with {distance} distance metric")
            return True

        except Exception as e:
            logger.error(f"Error creating collection '{self.collection_name}': {str(e)}")
            return False

    def store_embeddings(self, embedding_records: List[EmbeddingRecord]) -> bool:
        """
        Store embedding records in Qdrant collection

        Args:
            embedding_records: List of EmbeddingRecord objects to store

        Returns:
            True if embeddings were stored successfully, False otherwise
        """
        if not embedding_records:
            logger.warning("No embedding records to store")
            return True

        try:
            logger.info(f"Storing {len(embedding_records)} embeddings in collection '{self.collection_name}'")

            # Prepare points for insertion
            points = []
            for record in embedding_records:
                point = PointStruct(
                    id=record.id,
                    vector=record.vector,
                    payload=record.payload
                )
                points.append(point)

            # Insert points into collection
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

            logger.info(f"Successfully stored {len(embedding_records)} embeddings in collection '{self.collection_name}'")
            return True

        except Exception as e:
            logger.error(f"Error storing embeddings in collection '{self.collection_name}': {str(e)}")
            return False

    def search(self, query_vector: List[float], limit: int = 5) -> List[dict]:
        """
        Search for similar vectors in the collection

        Args:
            query_vector: Vector to search for similar vectors
            limit: Number of results to return

        Returns:
            List of search results with payload and similarity scores
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )

            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                })

            return formatted_results

        except Exception as e:
            logger.error(f"Error searching in collection '{self.collection_name}': {str(e)}")
            return []

    def delete_collection(self) -> bool:
        """
        Delete the collection from Qdrant

        Returns:
            True if collection was deleted successfully, False otherwise
        """
        try:
            self.client.delete_collection(collection_name=self.collection_name)
            logger.info(f"Collection '{self.collection_name}' deleted successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting collection '{self.collection_name}': {str(e)}")
            return False

    def get_collection_info(self) -> Optional[dict]:
        """
        Get information about the collection

        Returns:
            Dictionary with collection information or None if error
        """
        try:
            collection_info = self.client.get_collection(collection_name=self.collection_name)
            return {
                "name": collection_info.config.params.vectors.size,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": collection_info.config.params.vectors.distance,
                "point_count": collection_info.points_count
            }
        except Exception as e:
            logger.error(f"Error getting collection info for '{self.collection_name}': {str(e)}")
            return None