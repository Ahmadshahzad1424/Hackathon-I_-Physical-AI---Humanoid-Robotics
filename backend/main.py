#!/usr/bin/env python3
"""
URL Ingestion & Embedding Pipeline

This script crawls Docusaurus URLs, extracts and cleans content,
chunks the text, generates embeddings using Cohere, and stores
them in Qdrant Cloud.
"""

import asyncio
import logging
from typing import List, Optional

from config import Config
from pipeline import IngestionPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to run the full ingestion pipeline end-to-end
    """
    logger.info("Starting URL Ingestion & Embedding Pipeline")

    # Validate configuration
    config_errors = Config.validate()
    if config_errors:
        logger.error(f"Configuration validation failed: {config_errors}")
        return

    logger.info("Configuration validated successfully")

    # Get URLs to crawl from configuration
    urls_to_crawl = Config.VERCEL_URLS
    logger.info(f"URLs to crawl: {urls_to_crawl}")

    # Additional configuration options can be customized here
    logger.info(f"Chunk size: {Config.CHUNK_SIZE}")
    logger.info(f"Chunk overlap: {Config.CHUNK_OVERLAP}")
    logger.info(f"Embedding model: {Config.EMBEDDING_MODEL}")
    logger.info(f"Qdrant collection: {Config.QDRANT_COLLECTION_NAME}")

    # Initialize the ingestion pipeline
    try:
        pipeline = IngestionPipeline()
        logger.info("Ingestion pipeline initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize ingestion pipeline: {str(e)}")
        return

    # Run the full pipeline
    try:
        job_id = pipeline.run_pipeline(urls_to_crawl)
        logger.info(f"Pipeline execution completed with job ID: {job_id}")

        # Get and display final job status
        job_status = pipeline.get_job_status(job_id)
        if job_status:
            logger.info(f"Final job status: {job_status}")
    except Exception as e:
        logger.error(f"Failed to run ingestion pipeline: {str(e)}")
        return

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()