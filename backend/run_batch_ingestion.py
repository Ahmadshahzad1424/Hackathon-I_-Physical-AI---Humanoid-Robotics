#!/usr/bin/env python3
"""
Script to run ingestion pipeline in smaller batches to better handle rate limits
"""
import time
from pipeline import IngestionPipeline
from qdrant_service import QdrantService


def run_batch_ingestion():
    """Run ingestion in smaller batches to handle rate limits better"""
    print("Starting batch ingestion process...")

    pipeline = IngestionPipeline()
    all_urls = pipeline.get_all_urls_from_sitemap()

    print(f"Found {len(all_urls)} URLs from sitemap")

    # Process in smaller batches to reduce rate limiting
    batch_size = 5  # Small batch size to avoid rate limits
    total_processed = 0

    for i in range(0, len(all_urls), batch_size):
        batch = all_urls[i:i + batch_size]
        print(f"\nProcessing batch {i//batch_size + 1}: {len(batch)} URLs")
        print(f"URLs: {batch}")

        # Run pipeline for this batch
        job_id = pipeline.run_pipeline(batch)
        job_status = pipeline.get_job_status(job_id)

        print(f"Batch status: {job_status['status']}")
        if job_status['error_message']:
            print(f"Error in batch: {job_status['error_message']}")

        total_processed += len(batch)
        print(f"Progress: {total_processed}/{len(all_urls)} URLs processed")

        # Check current point count in Qdrant
        qdrant_service = QdrantService()
        collection_info = qdrant_service.get_collection_info()
        if collection_info:
            print(f"Current point count in Qdrant: {collection_info.get('point_count', 0)}")

        # Add delay between batches to be respectful to APIs
        print(f"Waiting 30 seconds before next batch...")
        time.sleep(30)

    # Final check
    print("\nFinal status check:")
    final_collection_info = qdrant_service.get_collection_info()
    if final_collection_info:
        print(f"Final point count in Qdrant: {final_collection_info.get('point_count', 0)}")

    print("Batch ingestion completed!")


if __name__ == "__main__":
    run_batch_ingestion()