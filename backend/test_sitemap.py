#!/usr/bin/env python3
"""
Test script to verify sitemap functionality
"""
from pipeline import IngestionPipeline

def test_sitemap():
    """Test sitemap functionality"""
    pipeline = IngestionPipeline()

    print("Testing sitemap parsing...")
    urls = pipeline.get_all_urls_from_sitemap()

    print(f"Found {len(urls)} URLs from sitemap")
    print("Sample URLs:")
    for i, url in enumerate(urls[:5]):  # Show first 5 URLs
        print(f"  {i+1}. {url}")

    if len(urls) > 5:
        print(f"  ... and {len(urls) - 5} more URLs")

    # Test crawling a few URLs to make sure they work
    print("\nTesting crawl of first 3 URLs...")
    test_urls = urls[:3]
    for i, url in enumerate(test_urls):
        print(f"  {i+1}. Crawling: {url}")
        try:
            # Test that we can fetch these URLs
            from job_manager import JobManager
            job_manager = JobManager()
            job = job_manager.create_job([url])
            job_id = job.id

            crawled_pages = pipeline._crawl_urls([url], job_id)
            if crawled_pages:
                print(f"     SUCCESS: Successfully crawled: {crawled_pages[0].title}")
            else:
                print(f"     FAILED: Failed to crawl")
        except Exception as e:
            print(f"     ERROR: {str(e)}")

if __name__ == "__main__":
    test_sitemap()