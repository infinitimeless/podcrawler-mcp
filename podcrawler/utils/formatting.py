"""
Output Formatting Utilities.

This module provides utilities for formatting podcast data into readable output.
"""
from typing import Dict, List, Any


def format_podcast_results(results: List[Dict[str, Any]]) -> str:
    """Format podcast results into a readable string.
    
    Args:
        results: List of podcast data with episodes
    
    Returns:
        Formatted string with podcast information
    """
    if not results:
        return "No relevant podcasts found."
    
    output = f"Found {len(results)} relevant podcasts:\n\n"
    
    for i, podcast in enumerate(results, 1):
        # Podcast title and description
        output += f"📌 {i}. {podcast.get('title', 'Unknown Podcast')}\n"
        
        # Add description (truncated if too long)
        description = podcast.get('description', '')
        if len(description) > 200:
            description = description[:197] + "..."
        if description:
            output += f"   {description}\n"
        
        # Add episodes
        episodes = podcast.get('episodes', [])
        if episodes:
            output += f"\n   🎙️ Latest relevant episodes:\n"
            
            for j, episode in enumerate(episodes, 1):
                # Episode title
                output += f"   {j}. {episode.get('title', 'Unknown Episode')}\n"
                
                # Published date
                pub_date = episode.get('published_date', '')
                if pub_date:
                    output += f"      Published: {pub_date}\n"
                
                # Episode description (shortened)
                ep_desc = episode.get('description', '')
                if len(ep_desc) > 150:
                    ep_desc = ep_desc[:147] + "..."
                if ep_desc:
                    output += f"      {ep_desc}\n"
                
                # Audio URL
                audio_url = episode.get('audio_url', '')
                if audio_url:
                    output += f"      🔊 Listen: {audio_url}\n"
                
                output += "\n"
        else:
            output += "   No relevant episodes found.\n"
        
        output += "\n" + "-" * 60 + "\n\n"
    
    return output


def format_error(message: str) -> str:
    """Format an error message.
    
    Args:
        message: Error message
    
    Returns:
        Formatted error message
    """
    return f"⚠️ Error: {message}"


def format_status(message: str) -> str:
    """Format a status message.
    
    Args:
        message: Status message
    
    Returns:
        Formatted status message
    """
    return f"ℹ️ {message}"