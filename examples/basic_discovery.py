"""
Basic Usage Example for PodCrawlerMCP.

This example demonstrates how to use the PodCrawlerMCP server programmatically.
"""
import asyncio
from podcrawler import PodCrawlerServer


async def main():
    """Run a basic podcast discovery example."""
    # Create server instance
    server = PodCrawlerServer()
    
    # Get the discover_podcasts tool from the server
    discover_podcasts = server.mcp.get_tool('discover_podcasts')
    
    # Example topic
    topic = "artificial intelligence"
    
    print(f"Searching for podcasts about '{topic}'...")
    
    # Call the tool
    results = await discover_podcasts(topic=topic, max_results=5)
    
    # Print the results
    print(results)


if __name__ == "__main__":
    # Run the async function
    asyncio.run(main())