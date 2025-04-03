# PodCrawlerMCP

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An MCP (Model Context Protocol) server for podcast discovery through web crawling. PodCrawlerMCP enables AI assistants to find podcast episodes on specific topics by crawling the web for RSS feeds.

## Features

- 🕸️ Crawls podcast directories to discover RSS feeds
- 🎙️ Parses RSS feeds to extract episode data
- 🔍 Filters episodes by topic or domain
- 🔌 Exposes functionality through MCP tools
- 🤖 Seamlessly integrates with AI assistants like Claude

## Installation

```bash
pip install podcrawler-mcp
```

Or with Poetry:

```bash
poetry add podcrawler-mcp
```

## Quick Start

Run the server directly:

```bash
python -m podcrawler.server
```

Or in your Python code:

```python
from podcrawler import PodCrawlerServer

server = PodCrawlerServer()
server.run()
```

## Integrating with Claude Desktop

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "podcrawler": {
      "command": "python",
      "args": ["-m", "podcrawler.server"]
    }
  }
}
```

## Available Tools

### discover_podcasts

Discovers podcasts on a specific topic.

**Parameters:**

- `topic` (string): The topic to search for (e.g., "technology", "history")
- `max_results` (integer, optional): Maximum number of results to return (default: 10)

**Example Usage:**

What are some science podcasts about black holes?

## Project Structure

```
podcrawler-mcp/
├── podcrawler/                # Main package
│   ├── __init__.py            # Package initialization
│   ├── server.py              # MCP server implementation
│   ├── tools/                 # MCP tools
│   │   ├── __init__.py
│   │   └── discovery.py       # Podcast discovery tool
│   ├── crawler/               # Web crawling components
│   │   ├── __init__.py
│   │   ├── spider.py          # Web crawler implementation
│   │   └── parser.py          # RSS feed parser
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       ├── filtering.py       # Topic filtering utilities
│       └── formatting.py      # Output formatting utilities
├── tests/                     # Tests
│   ├── __init__.py
│   └── test_server.py         # Server tests
├── examples/                  # Usage examples
│   └── basic_discovery.py     # Basic discovery example
├── pyproject.toml             # Project configuration
├── README.md                  # Project documentation
├── LICENSE                    # MIT License
└── CONTRIBUTING.md            # Contribution guidelines
```

## Development

1. Clone the repository
    
    ```bash
    git clone https://github.com/infinitimeless/podcrawler-mcp.git
    cd podcrawler-mcp
    ```
    
2. Install dependencies using Poetry
    
    ```bash
    poetry install
    ```
    
3. Run tests
    
    ```bash
    poetry run pytest
    ```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.