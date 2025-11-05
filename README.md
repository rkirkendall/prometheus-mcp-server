# Prometheus MCP Server

A [Model Context Protocol][mcp] (MCP) server for Prometheus.

This provides access to your Prometheus metrics and queries through standardized MCP interfaces, allowing AI assistants to execute PromQL queries and analyze your metrics data.

[mcp]: https://modelcontextprotocol.io

## Forked Changes

This fork includes the following enhancements:

- **Automatic timestamp conversion**: All Unix timestamps in query results are automatically converted to human-readable ISO 8601 format (e.g., `2021-04-08T16:14:08Z` instead of `1617898448`)
- **Dashboard visualization links**: Query results include clickable links to view the data graphed in the Prometheus UI
- **Enhanced LLM readability**: Timestamps in readable format allow AI assistants to better reason about time-series data

Original repository: [pab1it0/prometheus-mcp-server](https://github.com/pab1it0/prometheus-mcp-server)

## Features

- [x] Execute PromQL queries against Prometheus
- [x] Discover and explore metrics
  - [x] List available metrics
  - [x] Get metadata for specific metrics
  - [x] View instant query results
  - [x] View range query results with different step intervals
- [x] **Automatic timestamp conversion** - Unix timestamps are automatically converted to ISO 8601 format (e.g., `2021-04-08T16:14:08Z`) for better readability
- [x] **Interactive dashboard links** - Query results include links to visualize data in the Prometheus UI
- [x] Authentication support
  - [x] Basic auth from environment variables
  - [x] Bearer token auth from environment variables
- [x] Docker containerization support

- [x] Provide interactive tools for AI assistants

The list of tools is configurable, so you can choose which tools you want to make available to the MCP client.
This is useful if you don't use certain functionality or if you don't want to take up too much of the context window.

## Installation

### Prerequisites

- Python 3.10+ and [uv](https://github.com/astral-sh/uv) package manager
- Prometheus server accessible from your environment
- Cursor IDE (or other MCP-compatible client)

### Setup

1. **Clone this repository:**

```bash
git clone https://github.com/rkirkendall/prometheus-mcp-server.git
cd prometheus-mcp-server
```

2. **Install dependencies:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install -e .
```

3. **Configure Cursor MCP:**

Add to your `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "prometheus-local": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/prometheus-mcp-server",
        "python",
        "-m",
        "prometheus_mcp_server.main"
      ],
      "env": {
        "PROMETHEUS_URL": "http://localhost:9090"
      }
    }
  }
}
```

Replace `/path/to/prometheus-mcp-server` with the actual path where you cloned this repository.

4. **Restart Cursor** to load the MCP server

### Configuration Options

| Variable | Description | Required |
|----------|-------------|----------|
| `PROMETHEUS_URL` | URL of your Prometheus server | Yes |
| `PROMETHEUS_URL_SSL_VERIFY` | Set to False to disable SSL verification | No |
| `PROMETHEUS_DISABLE_LINKS` | Set to True to disable Prometheus UI links in query results (saves context tokens) | No |
| `PROMETHEUS_USERNAME` | Username for basic authentication | No |
| `PROMETHEUS_PASSWORD` | Password for basic authentication | No |
| `PROMETHEUS_TOKEN` | Bearer token for authentication | No |
| `ORG_ID` | Organization ID for multi-tenant setups | No |
| `PROMETHEUS_MCP_SERVER_TRANSPORT` | Transport mode (stdio, http, sse) | No (default: stdio) |
| `PROMETHEUS_MCP_BIND_HOST` | Host for HTTP transport | No (default: 127.0.0.1) |
| `PROMETHEUS_MCP_BIND_PORT` | Port for HTTP transport | No (default: 8080) |


## Development

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

This project uses [`uv`](https://github.com/astral-sh/uv) to manage dependencies. Install `uv` following the instructions for your platform:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

You can then create a virtual environment and install the dependencies with:

```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
.venv\Scripts\activate     # On Windows
uv pip install -e .
```

### Testing

The project includes a comprehensive test suite that ensures functionality and helps prevent regressions.

Run the tests with pytest:

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run the tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=term-missing
```

When adding new features, please also add corresponding tests.

### Tools

| Tool | Category | Description |
| --- | --- | --- |
| `execute_query` | Query | Execute a PromQL instant query against Prometheus |
| `execute_range_query` | Query | Execute a PromQL range query with start time, end time, and step interval |
| `list_metrics` | Discovery | List all available metrics in Prometheus |
| `get_metric_metadata` | Discovery | Get metadata for a specific metric |
| `get_targets` | Discovery | Get information about all scrape targets |

## License

MIT

---

[mcp]: https://modelcontextprotocol.io