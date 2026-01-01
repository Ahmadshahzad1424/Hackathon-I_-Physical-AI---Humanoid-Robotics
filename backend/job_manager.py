"""
Processing job management class to handle pipeline execution tracking
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from models import ProcessingJob


logger = logging.getLogger(__name__)


class JobManager:
    """Class to manage processing jobs for the ingestion pipeline"""

    def __init__(self):
        """Initialize the job manager"""
        self.jobs: Dict[str, ProcessingJob] = {}

    def create_job(self, urls: List[str]) -> ProcessingJob:
        """
        Create a new processing job

        Args:
            urls: List of URLs to process

        Returns:
            ProcessingJob object
        """
        job = ProcessingJob(
            status="PENDING",
            urls=urls,
            total_count=len(urls),
            processed_count=0
        )

        self.jobs[job.id] = job
        logger.info(f"Created new job {job.id} to process {len(urls)} URLs")

        return job

    def get_job(self, job_id: str) -> Optional[ProcessingJob]:
        """
        Get a processing job by ID

        Args:
            job_id: ID of the job to retrieve

        Returns:
            ProcessingJob object or None if not found
        """
        return self.jobs.get(job_id)

    def update_job_status(self, job_id: str, status: str, error_message: Optional[str] = None) -> bool:
        """
        Update the status of a processing job

        Args:
            job_id: ID of the job to update
            status: New status for the job
            error_message: Error message if job failed

        Returns:
            True if update was successful, False otherwise
        """
        job = self.jobs.get(job_id)
        if not job:
            logger.error(f"Job {job_id} not found")
            return False

        job.status = status
        if error_message:
            job.error_message = error_message

        if status in ["COMPLETED", "FAILED"]:
            job.completed_at = datetime.now()

        logger.info(f"Updated job {job_id} status to {status}")
        return True

    def update_job_progress(self, job_id: str, processed_count: int) -> bool:
        """
        Update the progress of a processing job

        Args:
            job_id: ID of the job to update
            processed_count: Number of URLs processed

        Returns:
            True if update was successful, False otherwise
        """
        job = self.jobs.get(job_id)
        if not job:
            logger.error(f"Job {job_id} not found")
            return False

        job.processed_count = processed_count

        # Automatically update status based on progress
        if processed_count == 0 and job.status == "PENDING":
            job.status = "IN_PROGRESS"
        elif processed_count == job.total_count and job.status == "IN_PROGRESS":
            job.status = "COMPLETED"
        elif processed_count > job.total_count:
            logger.warning(f"Processed count ({processed_count}) exceeds total count ({job.total_count}) for job {job_id}")

        logger.info(f"Updated job {job_id} progress: {processed_count}/{job.total_count}")
        return True

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed status information for a job

        Args:
            job_id: ID of the job to check

        Returns:
            Dictionary with job status information or None if not found
        """
        job = self.jobs.get(job_id)
        if not job:
            return None

        progress_percentage = 0
        if job.total_count > 0:
            progress_percentage = int((job.processed_count / job.total_count) * 100)

        return {
            "job_id": job.id,
            "status": job.status,
            "processed_count": job.processed_count,
            "total_count": job.total_count,
            "progress_percentage": progress_percentage,
            "error_message": job.error_message,
            "created_at": job.created_at.isoformat() if job.created_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None
        }