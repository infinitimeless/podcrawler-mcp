"""
Web Crawler for Podcast Discovery.

This module implements web crawling functionality to discover podcast RSS feeds.
"""
from typing import List, Optional, Dict, Any
import logging
import time
import random

import requests
from scrapy.http import TextResponse

# Configure logging
logger = logging.getLogger(__name__)

# Default podcast directories to crawl
DEFAULT_DIRECTORIES = [
    "https://podcastindex.org/",
    "https://www.listennotes.com/",
    "https://player.fm/",
]

# User agent for requests
USER_AGENT = "PodCrawlerMCP/0.1.0 (+https://github.com/infinitimeless/podcrawler-mcp)"

def crawl_directory(topic: str, directories: Optional[List[str]] = None) -> List[str]:
    """Crawl podcast directories to find RSS feeds related to the topic.
    
    Args:
        topic: The topic to search for
        directories: Optional list of podcast directory URLs to crawl
    
    Returns:
        List of discovered RSS feed URLs
    """
    if directories is None:
        directories = DEFAULT_DIRECTORIES
    
    feed_urls: List[str] = []
    
    for directory_url in directories:
        try:
            # Add the topic to the search URL
            search_url = f"{directory_url.rstrip('/')}/search?q={topic}"
            
            # Respect robots.txt by adding a delay
            time.sleep(random.uniform(1.0, 3.0))
            
            # Make the request
            response = requests.get(
                search_url,
                headers={"User-Agent": USER_AGENT},
                timeout=10
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                # Create a Scrapy TextResponse for easier parsing
                text_response = TextResponse(
                    url=search_url,
                    body=response.content,
                    encoding='utf-8'
                )
                
                # Extract RSS feed URLs using different common patterns
                feed_urls.extend(_extract_feed_urls(text_response))
            else:
                logger.warning(f"Failed to crawl {search_url}: HTTP {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error crawling {directory_url}: {str(e)}")
    
    # Remove duplicates and return
    return list(set(feed_urls))


def _extract_feed_urls(response: TextResponse) -> List[str]:
    """Extract RSS feed URLs from a webpage.
    
    Args:
        response: Scrapy TextResponse object
    
    Returns:
        List of RSS feed URLs
    """
    feed_urls = []
    
    # Look for RSS links in the HTML
    feed_urls.extend(response.css('link[type="application/rss+xml"]::attr(href)').getall())
    feed_urls.extend(response.css('a[href*=".rss"]::attr(href)').getall())
    feed_urls.extend(response.css('a[href*="feed"]::attr(href)').getall())
    
    # Look for podcast-specific patterns
    feed_urls.extend(response.css('a[href*="itunes.apple.com"]::attr(href)').getall())
    feed_urls.extend(response.css('a[href*="podcasts.apple.com"]::attr(href)').getall())
    feed_urls.extend(response.css('a[href*="spotify.com/show"]::attr(href)').getall())
    
    # Process relative URLs
    processed_urls = []
    for url in feed_urls:
        # Convert relative URLs to absolute
        absolute_url = response.urljoin(url)
        
        # Check if it's a valid feed URL
        if (absolute_url.endswith('.rss') or 
            absolute_url.endswith('.xml') or
            'feed' in absolute_url.lower() or
            'rss' in absolute_url.lower() or
            'podcast' in absolute_url.lower()):
            processed_urls.append(absolute_url)
    
    return processed_urls