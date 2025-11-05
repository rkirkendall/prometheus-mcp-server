#!/bin/bash
# Quick test script for local Prometheus MCP server

echo "Testing local Prometheus MCP server..."
echo ""
echo "This will start the MCP server and you can test it interactively."
echo "Make sure you have a Prometheus instance running first!"
echo ""
echo "Press Ctrl+C to stop the server when done."
echo ""

# Set default Prometheus URL if not provided
export PROMETHEUS_URL="${PROMETHEUS_URL:-http://localhost:9090}"

echo "Using PROMETHEUS_URL: $PROMETHEUS_URL"
echo ""

cd /home/owner/prometheus-mcp-server

# Run the server
uv run python -m prometheus_mcp_server.main

