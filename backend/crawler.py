"""
URL crawler class to handle URL fetching and content extraction
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
from urllib.parse import urljoin, urlparse
import time
from copy import deepcopy
import xml.etree.ElementTree as ET

from models import CrawledPage

logger = logging.getLogger(__name__)


class URLCrawler:
    """Class to handle URL fetching and content extraction"""

    def __init__(self, timeout: int = 10, delay: float = 0.5):
        """
        Initialize the crawler with timeout and delay settings

        Args:
            timeout: Request timeout in seconds
            delay: Delay between requests in seconds to be respectful to servers
        """
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def fetch_url(self, url: str) -> Optional[CrawledPage]:
        """
        Fetch a single URL and extract content

        Args:
            url: URL to fetch

        Returns:
            CrawledPage object with extracted content or None if failed
        """
        try:
            logger.info(f"Fetching URL: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            title = "No Title"
            if soup.title and soup.title.string:
                title = soup.title.string.strip()
            elif soup.find('h1'):
                # If no title tag, try to get the first h1 as title
                title = soup.find('h1').get_text().strip()
            elif soup.find('h2'):
                # If no h1, try to get the first h2 as title
                title = soup.find('h2').get_text().strip()

            # Clean the HTML to remove navigation, footer, and other non-content elements
            cleaned_soup = self._clean_html(soup)

            # Extract content from cleaned HTML
            content = cleaned_soup.get_text(separator=' ', strip=True)

            # Create metadata
            metadata = {
                'url': url,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'response_size': len(response.content)
            }

            # Create and return CrawledPage object
            crawled_page = CrawledPage(
                url=url,
                title=title,
                content=content,
                metadata=metadata
            )

            # Add delay to be respectful to the server
            time.sleep(self.delay)

            return crawled_page

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching URL {url}: {str(e)}")
            return None

    def _clean_html(self, soup: BeautifulSoup) -> BeautifulSoup:
        """
        Remove navigation, footer, and other non-content elements from HTML

        Args:
            soup: BeautifulSoup object to clean

        Returns:
            Cleaned BeautifulSoup object
        """
        # Make a copy to avoid modifying the original
        cleaned_soup = deepcopy(soup)

        # Remove common navigation elements
        for element in cleaned_soup.find_all(['nav', 'header', 'footer', 'aside']):
            element.decompose()

        # Remove common non-content elements based on class names and IDs
        non_content_selectors = [
            '[class*="nav"]', '[id*="nav"]',
            '[class*="menu"]', '[id*="menu"]',
            '[class*="sidebar"]', '[id*="sidebar"]',
            '[class*="footer"]', '[id*="footer"]',
            '[class*="header"]', '[id*="header"]',
            '[class*="search"]', '[id*="search"]',
            '[class*="cookie"]', '[id*="cookie"]',
            '[class*="advertisement"]', '[id*="advertisement"]',
            '[class*="ads"]', '[id*="ads"]',
            '[class*="social"]', '[id*="social"]',
            '[class*="share"]', '[id*="share"]'
        ]

        for selector in non_content_selectors:
            for element in cleaned_soup.select(selector):
                element.decompose()

        # For Docusaurus sites, remove common elements
        docusaurus_selectors = [
            '.navbar', '.sidebar', '.toc', '.theme-edit-this-page',
            '.theme-last-updated', '.pagination-nav', '.footer',
            '.theme-admonition', '[data-theme="sidebar"]'
        ]

        for selector in docusaurus_selectors:
            for element in cleaned_soup.select(selector):
                element.decompose()

        return cleaned_soup

    def discover_urls(self, base_url: str) -> List[str]:
        """
        Discover all URLs on a Docusaurus site by finding internal links

        Args:
            base_url: Base URL of the Docusaurus site

        Returns:
            List of discovered URLs
        """
        try:
            logger.info(f"Discovering URLs from: {base_url}")
            discovered_urls = set()
            visited_urls = set()
            urls_to_visit = [base_url]

            while urls_to_visit:
                current_url = urls_to_visit.pop(0)
                if current_url in visited_urls:
                    continue

                visited_urls.add(current_url)

                try:
                    response = self.session.get(current_url, timeout=self.timeout)
                    response.raise_for_status()

                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Find all links on the page
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        full_url = urljoin(current_url, href)

                        # Only add URLs from the same domain and with proper extensions
                        if self._is_valid_docusaurus_url(full_url, base_url):
                            if full_url not in visited_urls and full_url not in urls_to_visit:
                                urls_to_visit.append(full_url)
                                discovered_urls.add(full_url)

                except Exception as e:
                    logger.warning(f"Error discovering URLs from {current_url}: {str(e)}")
                    continue

                # Add delay to be respectful to the server
                time.sleep(self.delay)

            return list(discovered_urls)

        except Exception as e:
            logger.error(f"Error discovering URLs from {base_url}: {str(e)}")
            return [base_url]  # Return the base URL as fallback

    def _is_valid_docusaurus_url(self, url: str, base_url: str) -> bool:
        """
        Check if a URL is a valid Docusaurus page URL

        Args:
            url: URL to check
            base_url: Base URL of the Docusaurus site

        Returns:
            True if the URL is valid for crawling
        """
        parsed_base = urlparse(base_url)
        parsed_url = urlparse(url)

        # Same domain check
        if parsed_base.netloc != parsed_url.netloc:
            return False

        # Check for common Docusaurus file extensions or paths
        path = parsed_url.path.lower()
        if path.endswith(('.html', '.htm', '/')) or not path.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', '.exe')):
            return True

        return False

    def parse_sitemap(self, sitemap_url: str, base_url: str) -> List[str]:
        """
        Parse a sitemap.xml file and extract all URLs

        Args:
            sitemap_url: URL to the sitemap.xml file
            base_url: Base URL of the site (used to fix domain issues in sitemap)

        Returns:
            List of valid URLs extracted from the sitemap
        """
        try:
            logger.info(f"Parsing sitemap: {sitemap_url}")
            response = self.session.get(sitemap_url, timeout=self.timeout)
            response.raise_for_status()

            # Parse the XML content
            root = ET.fromstring(response.content)

            # Handle both regular sitemap and sitemap index formats
            urls = []
            namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            # Get all URL elements
            for url_elem in root.findall('sitemap:url', namespace):
                loc_elem = url_elem.find('sitemap:loc', namespace)
                if loc_elem is not None:
                    url = loc_elem.text.strip()

                    # Fix the domain in the sitemap if it's a placeholder
                    parsed_base = urlparse(base_url)
                    parsed_url = urlparse(url)

                    # If the sitemap URL has a different domain (like placeholder), fix it
                    if parsed_url.netloc != parsed_base.netloc and parsed_url.netloc != 'your-docusaurus-site.example.com':
                        # Keep the path and query from sitemap, but use base domain
                        fixed_url = f"{parsed_base.scheme}://{parsed_base.netloc}{parsed_url.path}"
                        if parsed_url.query:
                            fixed_url += f"?{parsed_url.query}"
                        urls.append(fixed_url)
                    elif parsed_url.netloc == 'your-docusaurus-site.example.com':
                        # Replace the placeholder domain with the actual base URL domain
                        fixed_url = url.replace('your-docusaurus-site.example.com', parsed_base.netloc)
                        urls.append(fixed_url)
                    else:
                        urls.append(url)

            logger.info(f"Found {len(urls)} URLs in sitemap")
            return urls

        except ET.ParseError as e:
            logger.error(f"Error parsing sitemap XML: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error fetching or parsing sitemap {sitemap_url}: {str(e)}")
            return []