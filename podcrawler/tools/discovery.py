"""
Podcast Discovery Tool for MCP.

This module implements the podcast discovery tool for the MCP server.
"""
from typing import Dict, List, Any, Optional

from mcp.server.fastmcp import FastMCP

from podcrawler.crawler.spider import crawl_directory
from podcrawler.crawler.parser import parse_feed
from podcrawler.utils.filtering import filter_by_topic
from podcrawler.utils.formatting import format_podcast_results


def register_discovery_tool(mcp: FastMCP, config: Optional[Dict[str, Any]] = None) -> None:
    """Register the podcast discovery tool with the MCP server.
    
    Args:
        mcp: The MCP server instance
        config: Optional configuration
    """
    config = config or {}
    
    @mcp.tool()
    async def discover_podcasts(topic: str, max_results: int = 10) -> str:
        """Discover podcasts on a specific topic.
        
        Args:
            topic: The topic to search for (e.g., "technology", "history")
            max_results: Maximum number of results to return (default: 10)
        
        Returns:
            A formatted list of podcasts with their episodes and audio URLs
        """
        try:
            # Step 1: Crawl podcast directory for RSS feeds
            feeds = crawl_directory(topic, config.get('directories'))
            
            if not feeds:
                return f"No podcast feeds found for topic: {topic}"
            
            results: List[Dict[str, Any]] = []
            total_episodes = 0
            
            # Step 2: Parse feeds and filter by topic
            for feed_url in feeds[:max_results]:
                try:
                    podcast_data = parse_feed(feed_url)
                    
                    # Step 3: Filter episodes by topic
                    relevant_episodes = filter_by_topic(podcast_data, topic)
                    
                    if relevant_episodes:
                        podcast_info = {
                            "title": podcast_data.get("title", "Unknown"),
                            "description": podcast_data.get("description", ""),
                            "episodes": [
                                {
                                    "title": episode.get("title", ""),
                                    "description": episode.get("description", ""),
                                    "audio_url": episode.get("audio_url", ""),
                                    "published_date": episode.get("published_date", "")
                                }
                                for episode in relevant_episodes[:3]  # Limit to 3 episodes per podcast
                            ]
                        }
                        
                        results.append(podcast_info)
                        total_episodes += len(podcast_info["episodes"])
                        
                        if total_episodes >= max_results:
                            break
                            
                except Exception as e:
                    continue  # Skip problematic feeds
            
            # Format results as readable text
            return format_podcast_results(results)
            
        except Exception as e:
            return f"Error discovering podcasts: {str(e)}"