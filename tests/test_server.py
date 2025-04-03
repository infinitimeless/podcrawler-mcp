"""
Unit tests for the PodCrawler MCP server.
"""
import pytest
from podcrawler import PodCrawlerServer


def test_server_initialization():
    """Test that the server initializes correctly."""
    server = PodCrawlerServer()
    assert server.mcp is not None


def test_server_config():
    """Test that server configuration works."""
    config = {"test_key": "test_value"}
    server = PodCrawlerServer(config=config)
    assert server.config == config


def test_server_name():
    """Test that server name can be set."""
    name = "test-server"
    server = PodCrawlerServer(name=name)
    assert server.mcp.name == name


def test_tools_registration():
    """Test that tools are registered."""
    server = PodCrawlerServer()
    # Check that the discover_podcasts tool is registered
    assert hasattr(server.mcp, "get_tool")
    tool = server.mcp.get_tool('discover_podcasts')
    assert tool is not None