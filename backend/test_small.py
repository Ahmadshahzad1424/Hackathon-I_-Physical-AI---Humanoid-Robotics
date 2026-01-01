#!/usr/bin/env python3
"""
Test script to run a small subset of URLs to test the full pipeline
"""
from config import Config
from pipeline import IngestionPipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_small_pipeline():
    """Test the full pipeline with a small subset of URLs"""
    print("Starting small pipeline test...")

    # Initialize the ingestion pipeline
    pipeline = IngestionPipeline()
    logger.info("Ingestion pipeline initialized successfully")

    # Use a small subset of documentation URLs
    test_urls = [
        "https://hackathon-i-physical-ai-humanoid-ro-tau.vercel.app/docs/intro",
        "https://hackathon-i-physical-ai-humanoid-ro-tau.vercel.app/docs/introduction/what-is-ros2",
        "https://hackathon-i-physical-ai-humanoid-ro-tau.vercel.app/docs/vla/intro",
        "https://hackathon-i-physical-ai-humanoid-ro-tau.vercel.app/docs/digital-twin/introduction"
    ]

    print(f"Testing with {len(test_urls)} URLs from documentation...")
    for i, url in enumerate(test_urls):
        print(f"  {i+1}. {url}")

    # Run the pipeline
    job_id = pipeline.run_pipeline(test_urls)

    # Print final job status
    job_status = pipeline.get_job_status(job_id)
    print(f"Pipeline execution completed with job ID: {job_id}")
    print(f"Final job status: {job_status}")

    logger.info("Pipeline completed successfully")

if __name__ == "__main__":
    test_small_pipeline()