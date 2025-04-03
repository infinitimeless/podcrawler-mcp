"""
RSS Feed Parser for Podcast Discovery.

This module handles parsing of podcast RSS feeds.
"""
from typing import Dict, Any, List
import logging
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# User agent for requests
USER_AGENT = "PodCrawlerMCP/0.1.0 (+https://github.com/infinitimeless/podcrawler-mcp)"

def parse_feed(feed_url: str) -> Dict[str, Any]:
    """Parse a podcast RSS feed to extract podcast and episode information.
    
    Args:
        feed_url: URL of the RSS feed to parse
    
    Returns:
        Dict containing podcast information and episodes
    """
    try:
        # Make the request
        response = requests.get(
            feed_url,
            headers={"User-Agent": USER_AGENT},
            timeout=10
        )
        
        # Check if the request was successful
        if response.status_code != 200:
            logger.warning(f"Failed to fetch feed {feed_url}: HTTP {response.status_code}")
            return {"title": "Unknown", "description": "", "episodes": []}
        
        # Parse the XML content
        root = ET.fromstring(response.content)
        
        # Find the channel element
        channel = root.find('channel')
        if channel is None:
            logger.warning(f"Invalid RSS feed format for {feed_url}")
            return {"title": "Unknown", "description": "", "episodes": []}
        
        # Extract podcast information
        podcast_info = {
            "title": _get_element_text(channel, 'title', 'Unknown Podcast'),
            "description": _get_element_text(channel, 'description', ''),
            "link": _get_element_text(channel, 'link', ''),
            "language": _get_element_text(channel, 'language', 'en'),
            "copyright": _get_element_text(channel, 'copyright', ''),
            "lastBuildDate": _get_element_text(channel, 'lastBuildDate', ''),
            "episodes": []
        }
        
        # Extract iTunes-specific elements
        itunes_ns = {'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd'}
        podcast_info['author'] = _get_element_text(
            channel, 
            './/itunes:author', 
            '', 
            namespaces=itunes_ns
        )
        podcast_info['explicit'] = _get_element_text(
            channel, 
            './/itunes:explicit', 
            'no', 
            namespaces=itunes_ns
        )
        podcast_info['image'] = _get_element_attr(
            channel, 
            './/itunes:image', 
            'href', 
            '', 
            namespaces=itunes_ns
        )
        
        # Extract episodes
        items = channel.findall('item')
        for item in items:
            episode = {
                "title": _get_element_text(item, 'title', 'Unknown Episode'),
                "description": _get_element_text(item, 'description', ''),
                "link": _get_element_text(item, 'link', ''),
                "guid": _get_element_text(item, 'guid', ''),
                "pubDate": _get_element_text(item, 'pubDate', ''),
                "published_date": _parse_date(_get_element_text(item, 'pubDate', '')),
                "duration": _get_element_text(
                    item, 
                    './/itunes:duration', 
                    '', 
                    namespaces=itunes_ns
                ),
                "explicit": _get_element_text(
                    item, 
                    './/itunes:explicit', 
                    'no', 
                    namespaces=itunes_ns
                ),
                "episode_type": _get_element_text(
                    item, 
                    './/itunes:episodeType', 
                    'full', 
                    namespaces=itunes_ns
                ),
            }
            
            # Get the audio URL from the enclosure
            enclosure = item.find('enclosure')
            if enclosure is not None:
                episode['audio_url'] = enclosure.get('url', '')
                episode['type'] = enclosure.get('type', '')
                episode['length'] = enclosure.get('length', '')
            else:
                episode['audio_url'] = ''
                episode['type'] = ''
                episode['length'] = ''
            
            podcast_info['episodes'].append(episode)
        
        return podcast_info
        
    except Exception as e:
        logger.error(f"Error parsing feed {feed_url}: {str(e)}")
        return {"title": "Unknown", "description": "", "episodes": []}


def _get_element_text(element: ET.Element, path: str, default: str, namespaces: Dict[str, str] = None) -> str:
    """Get the text content of an XML element.
    
    Args:
        element: Parent XML element
        path: XPath to the target element
        default: Default value if element doesn't exist
        namespaces: Optional namespace mapping
    
    Returns:
        Text content of the element or default value
    """
    try:
        child = element.find(path, namespaces)
        if child is not None and child.text is not None:
            return child.text.strip()
    except Exception:
        pass
    
    return default


def _get_element_attr(element: ET.Element, path: str, attr: str, default: str, namespaces: Dict[str, str] = None) -> str:
    """Get an attribute value from an XML element.
    
    Args:
        element: Parent XML element
        path: XPath to the target element
        attr: Attribute name
        default: Default value if element or attribute doesn't exist
        namespaces: Optional namespace mapping
    
    Returns:
        Attribute value or default
    """
    try:
        child = element.find(path, namespaces)
        if child is not None:
            return child.get(attr, default)
    except Exception:
        pass
    
    return default


def _parse_date(date_str: str) -> str:
    """Parse and format a date string from an RSS feed.
    
    Args:
        date_str: Date string in RSS format
    
    Returns:
        Formatted date string (YYYY-MM-DD) or empty string on error
    """
    if not date_str:
        return ""
    
    try:
        # Try to parse various date formats
        for fmt in [
            '%a, %d %b %Y %H:%M:%S %z',  # RFC 822
            '%a, %d %b %Y %H:%M:%S %Z',
            '%a, %d %b %Y %H:%M:%S',
            '%d %b %Y %H:%M:%S %z',
            '%Y-%m-%dT%H:%M:%S%z',        # ISO 8601
            '%Y-%m-%dT%H:%M:%S',
        ]:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
    except Exception:
        pass
    
    return ""