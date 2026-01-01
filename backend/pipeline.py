"""
Pipeline orchestration class to coordinate the full ingestion pipeline
"""
import logging
from typing import List, Optional
from datetime import datetime

from config import Config
from crawler import URLCrawler
from chunker import TextChunker
from embedding_service import EmbeddingService
from qdrant_service import QdrantService
from job_manager import JobManager
from models import CrawledPage, TextChunk, EmbeddingRecord


logger = logging.getLogger(__name__)


class IngestionPipeline:
    """Class to orchestrate the full ingestion pipeline from URL crawling to vector storage"""

    def __init__(self):
        """Initialize the ingestion pipeline with all required services"""
        self.crawler = URLCrawler()
        self.chunker = TextChunker(chunk_size=Config.CHUNK_SIZE, chunk_overlap=Config.CHUNK_OVERLAP)
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()
        self.job_manager = JobManager()

        # Verify Qdrant collection exists or create it
        collection_created = self.qdrant_service.create_collection()
        if not collection_created:
            raise Exception("Failed to create or verify Qdrant collection")

    def get_default_urls(self) -> List[str]:
        """
        Get default URLs from configuration

        Returns:
            List of URLs configured in the environment
        """
        return Config.VERCEL_URLS

    def get_all_urls_from_sitemap(self) -> List[str]:
        """
        Get all URLs from the sitemap

        Returns:
            List of all URLs from the sitemap
        """
        from crawler import URLCrawler
        crawler = URLCrawler()

        sitemap_urls = crawler.parse_sitemap(Config.SITEMAP_URL, Config.VERCEL_URLS[0] if Config.VERCEL_URLS else "https://hackathon-i-physical-ai-humanoid-ro-tau.vercel.app/")
        return sitemap_urls

    def run_pipeline(self, urls: List[str], job_id: Optional[str] = None) -> str:
        """
        Run the full ingestion pipeline from start to finish

        Args:
            urls: List of URLs to process
            job_id: Optional job ID (if not provided, one will be created)

        Returns:
            Job ID for tracking the pipeline execution
        """
        # Create a job to track this pipeline execution
        if not job_id:
            job = self.job_manager.create_job(urls)
            job_id = job.id
        else:
            # Update existing job with new URLs if needed
            self.job_manager.update_job_status(job_id, "PENDING")

        logger.info(f"Starting ingestion pipeline for job {job_id} with {len(urls)} URLs")

        try:
            # Update job status to IN_PROGRESS
            self.job_manager.update_job_status(job_id, "IN_PROGRESS")

            # Step 1: Crawl URLs
            logger.info(f"Job {job_id}: Starting URL crawling...")
            crawled_pages = self._crawl_urls(urls, job_id)

            if not crawled_pages:
                error_msg = f"Job {job_id}: No pages were successfully crawled"
                logger.error(error_msg)
                self.job_manager.update_job_status(job_id, "FAILED", error_msg)
                return job_id

            logger.info(f"Job {job_id}: Completed crawling {len(crawled_pages)} pages")

            # Step 2: Chunk content
            logger.info(f"Job {job_id}: Starting content chunking...")
            all_text_chunks = self._chunk_content(crawled_pages, job_id)

            if not all_text_chunks:
                error_msg = f"Job {job_id}: No text chunks were generated"
                logger.error(error_msg)
                self.job_manager.update_job_status(job_id, "FAILED", error_msg)
                return job_id

            logger.info(f"Job {job_id}: Completed chunking into {len(all_text_chunks)} chunks")

            # Step 3: Generate embeddings
            logger.info(f"Job {job_id}: Starting embedding generation...")
            embedding_records = self._generate_embeddings(all_text_chunks, job_id)

            if not embedding_records:
                error_msg = f"Job {job_id}: No embeddings were generated"
                logger.error(error_msg)
                self.job_manager.update_job_status(job_id, "FAILED", error_msg)
                return job_id

            logger.info(f"Job {job_id}: Completed embedding generation for {len(embedding_records)} chunks")

            # Step 4: Store in Qdrant
            logger.info(f"Job {job_id}: Starting vector storage...")
            storage_success = self._store_embeddings(embedding_records, job_id)

            if not storage_success:
                error_msg = f"Job {job_id}: Failed to store embeddings in Qdrant"
                logger.error(error_msg)
                self.job_manager.update_job_status(job_id, "FAILED", error_msg)
                return job_id

            logger.info(f"Job {job_id}: Completed vector storage in Qdrant")

            # Update job status to COMPLETED
            self.job_manager.update_job_status(job_id, "COMPLETED")
            logger.info(f"Job {job_id}: Pipeline completed successfully")

        except Exception as e:
            error_msg = f"Job {job_id}: Pipeline failed with error: {str(e)}"
            logger.error(error_msg)
            self.job_manager.update_job_status(job_id, "FAILED", error_msg)

        return job_id

    def _crawl_urls(self, urls: List[str], job_id: str) -> List[CrawledPage]:
        """
        Crawl a list of URLs and return crawled pages

        Args:
            urls: List of URLs to crawl
            job_id: Job ID for tracking progress

        Returns:
            List of CrawledPage objects
        """
        crawled_pages = []
        for i, url in enumerate(urls):
            if url.strip():
                logger.info(f"Job {job_id}: Crawling {url} ({i+1}/{len(urls)})")
                crawled_page = self.crawler.fetch_url(url.strip())
                if crawled_page:
                    crawled_pages.append(crawled_page)
                    logger.info(f"Job {job_id}: Successfully crawled {crawled_page.title}")
                else:
                    logger.warning(f"Job {job_id}: Failed to crawl {url}")

                # Update job progress
                self.job_manager.update_job_progress(job_id, i + 1)

        return crawled_pages

    def _chunk_content(self, pages: List[CrawledPage], job_id: str) -> List[TextChunk]:
        """
        Chunk the content from crawled pages

        Args:
            pages: List of CrawledPage objects to chunk
            job_id: Job ID for tracking progress

        Returns:
            List of TextChunk objects
        """
        all_text_chunks = []
        total_pages = len(pages)

        for i, page in enumerate(pages):
            logger.info(f"Job {job_id}: Chunking content for page {page.title} ({i+1}/{total_pages})")
            text_chunks = self.chunker.chunk_page(page)
            all_text_chunks.extend(text_chunks)
            logger.info(f"Job {job_id}: Generated {len(text_chunks)} chunks for page: {page.title}")

        return all_text_chunks

    def _generate_embeddings(self, chunks: List[TextChunk], job_id: str) -> List[EmbeddingRecord]:
        """
        Generate embeddings for text chunks

        Args:
            chunks: List of TextChunk objects to embed
            job_id: Job ID for tracking progress

        Returns:
            List of EmbeddingRecord objects
        """
        logger.info(f"Job {job_id}: Generating embeddings for {len(chunks)} text chunks")
        embedding_records = self.embedding_service.generate_embeddings(chunks)
        return embedding_records

    def _store_embeddings(self, records: List[EmbeddingRecord], job_id: str) -> bool:
        """
        Store embedding records in Qdrant

        Args:
            records: List of EmbeddingRecord objects to store
            job_id: Job ID for tracking progress

        Returns:
            True if storage was successful, False otherwise
        """
        logger.info(f"Job {job_id}: Storing {len(records)} embeddings in Qdrant")
        success = self.qdrant_service.store_embeddings(records)
        return success

    def get_job_status(self, job_id: str) -> Optional[dict]:
        """
        Get the status of a specific job

        Args:
            job_id: ID of the job to check

        Returns:
            Dictionary with job status information or None if not found
        """
        return self.job_manager.get_job_status(job_id)