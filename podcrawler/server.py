"""
PodCrawlerMCP Server Implementation.

This module provides the main MCP server for podcast discovery.
"""
from typing import Dict, Optional, Any

from mcp.server.fastmcp import FastMCP
from podcrawler.tools.discovery import register_discovery_tool


class PodCrawlerServer:
    """Main MCP server for podcast discovery."""
    
    def __init__(self, name: str = "podcrawler", config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the PodCrawler MCP server.
        
        Args:
            name: Server name
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.mcp = FastMCP(name)
        self._register_tools()
        
    def _register_tools(self) -> None:
        """Register all MCP tools."""
        register_discovery_tool(self.mcp, self.config)
        
    def run(self, transport: str = 'stdio') -> None:
        """Run the MCP server with specified transport.
        
        Args:
            transport: Transport type ('stdio' or 'sse')
        """
        self.mcp.run(transport=transport)


def main() -> None:
    """Run the PodCrawler MCP server."""
    server = PodCrawlerServer()
    server.run()


if __name__ == "__main__":
    main()