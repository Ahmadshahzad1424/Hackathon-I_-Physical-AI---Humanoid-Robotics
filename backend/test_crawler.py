"""
Test script to isolate the crawler issue
"""
import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_basic_crawling():
    """Test basic crawling functionality"""
    url = "https://hackathon-i-physical-ai-humanoid-ro-tau.vercel.app/"

    try:
        logger.info(f"Testing basic crawling for URL: {url}")

        # Create session
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        # Make request
        response = session.get(url, timeout=10)
        response.raise_for_status()
        logger.info(f"Successfully fetched URL, status code: {response.status_code}")

        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        logger.info("Successfully parsed HTML with BeautifulSoup")

        # Test title extraction (the problematic part)
        title = "No Title"
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
            logger.info(f"Title found: {title}")
        else:
            logger.info("No title tag found")

        # Test content extraction
        content = soup.get_text(separator=' ', strip=True)
        logger.info(f"Content length: {len(content)} characters")

        # Test other soup operations that might be causing the issue
        logger.info("Testing soup operations...")

        # Test find operations
        h1_tag = soup.find('h1')
        if h1_tag:
            h1_text = h1_tag.get_text().strip()
            logger.info(f"H1 tag found: {h1_text}")
        else:
            logger.info("No H1 tag found")

        # Test select operations (these could be causing the issue)
        elements = soup.select('[class*="nav"]')
        logger.info(f"Found {len(elements)} navigation elements")

        logger.info("All operations completed successfully!")

    except Exception as e:
        logger.error(f"Error in test: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    test_basic_crawling()