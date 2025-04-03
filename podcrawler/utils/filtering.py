"""
Podcast Content Filtering Utilities.

This module provides utilities for filtering podcast content by topic.
"""
from typing import Dict, List, Any
import re


def filter_by_topic(podcast_data: Dict[str, Any], topic: str) -> List[Dict[str, Any]]:
    """Filter podcast episodes by relevance to a topic.
    
    Args:
        podcast_data: Podcast data including episodes
        topic: Topic to filter by
    
    Returns:
        List of episodes relevant to the topic
    """
    if not podcast_data or 'episodes' not in podcast_data:
        return []
    
    # Prepare topic for matching (case insensitive)
    topic_words = set(re.findall(r'\w+', topic.lower()))
    
    # Define stemming function (simple implementation)
    def simple_stem(word: str) -> str:
        """Simple word stemming function."""
        if word.endswith('ing'):
            return word[:-3]
        elif word.endswith('s'):
            return word[:-1]
        elif word.endswith('ed'):
            return word[:-2]
        return word
    
    # Stem the topic words
    stemmed_topics = {simple_stem(word) for word in topic_words}
    
    # Add related words to create a broader match
    expanded_topics = stemmed_topics.copy()
    for word in stemmed_topics:
        # Add some common related forms
        if len(word) > 3:  # Only expand words longer than 3 chars
            expanded_topics.add(word + 's')  # Plural
            expanded_topics.add(word + 'ing')  # Gerund
            expanded_topics.add(word + 'ed')  # Past tense
    
    relevant_episodes = []
    
    for episode in podcast_data.get('episodes', []):
        # Calculate relevance score
        score = _calculate_relevance_score(episode, expanded_topics)
        
        # If score is above threshold, add to results
        if score > 0.2:  # Threshold can be adjusted
            # Add score to episode for sorting
            episode_copy = episode.copy()
            episode_copy['_relevance_score'] = score
            relevant_episodes.append(episode_copy)
    
    # Sort by relevance score (highest first)
    relevant_episodes.sort(key=lambda x: x.get('_relevance_score', 0), reverse=True)
    
    # Remove the temporary score field
    for episode in relevant_episodes:
        if '_relevance_score' in episode:
            del episode['_relevance_score']
    
    return relevant_episodes


def _calculate_relevance_score(episode: Dict[str, Any], topic_words: set) -> float:
    """Calculate relevance score of an episode to a set of topic words.
    
    Args:
        episode: Episode data
        topic_words: Set of topic words to match against
    
    Returns:
        Relevance score between 0.0 and 1.0
    """
    # Extract text fields from episode
    title = episode.get('title', '').lower()
    description = episode.get('description', '').lower()
    
    # Get all words from title and description
    title_words = set(re.findall(r'\w+', title))
    desc_words = set(re.findall(r'\w+', description))
    
    # Title matches are more important
    title_score = len(title_words.intersection(topic_words)) / max(len(title_words), 1)
    desc_score = len(desc_words.intersection(topic_words)) / max(len(desc_words), 1)
    
    # Weight title matches higher
    weighted_score = (title_score * 0.7) + (desc_score * 0.3)
    
    return weighted_score