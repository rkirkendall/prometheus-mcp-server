"""Tests for timestamp conversion functionality."""

import pytest
from prometheus_mcp_server.server import convert_timestamp_to_iso, convert_prometheus_response_timestamps


class TestTimestampConversion:
    """Test timestamp conversion utilities."""

    def test_convert_timestamp_to_iso_basic(self):
        """Test basic Unix timestamp to ISO 8601 conversion."""
        # 2021-04-08T16:14:08Z (UTC)
        result = convert_timestamp_to_iso(1617898448)
        
        assert isinstance(result, str)
        assert "T" in result
        assert result.endswith("Z")
        assert "2021-04-08" in result
        # Check for time components (HH:MM:SS format)
        assert result.count(":") == 2

    def test_convert_timestamp_to_iso_with_decimal(self):
        """Test Unix timestamp with decimal precision."""
        # Should strip microseconds
        result = convert_timestamp_to_iso(1617898448.214)
        
        assert isinstance(result, str)
        assert "T" in result
        assert result.endswith("Z")
        # Should not have microseconds
        assert "." not in result or result.split(".")[-1] == "Z"

    def test_convert_prometheus_response_instant_query(self):
        """Test conversion of instant query response."""
        data = {
            "resultType": "vector",
            "result": [
                {"metric": {"__name__": "up"}, "value": [1617898448, "1"]},
                {"metric": {"__name__": "down"}, "value": [1617898448, "0"]}
            ]
        }
        
        result = convert_prometheus_response_timestamps(data)
        
        assert result["resultType"] == "vector"
        assert len(result["result"]) == 2
        
        # Check first result
        assert isinstance(result["result"][0]["value"][0], str)
        assert "2021-04-08" in result["result"][0]["value"][0]
        assert result["result"][0]["value"][1] == "1"
        
        # Check second result
        assert isinstance(result["result"][1]["value"][0], str)
        assert result["result"][1]["value"][1] == "0"

    def test_convert_prometheus_response_range_query(self):
        """Test conversion of range query response."""
        data = {
            "resultType": "matrix",
            "result": [
                {
                    "metric": {"__name__": "up"},
                    "values": [
                        [1617898400, "1"],
                        [1617898415, "1"],
                        [1617898430, "0"]
                    ]
                }
            ]
        }
        
        result = convert_prometheus_response_timestamps(data)
        
        assert result["resultType"] == "matrix"
        assert len(result["result"]) == 1
        assert len(result["result"][0]["values"]) == 3
        
        # Check all timestamps were converted
        for value_pair in result["result"][0]["values"]:
            assert isinstance(value_pair[0], str)
            assert "T" in value_pair[0]
            assert "Z" in value_pair[0]
            assert "2021-04-08" in value_pair[0]

    def test_convert_prometheus_response_empty_result(self):
        """Test conversion with empty result."""
        data = {
            "resultType": "vector",
            "result": []
        }
        
        result = convert_prometheus_response_timestamps(data)
        
        assert result["resultType"] == "vector"
        assert result["result"] == []

    def test_convert_prometheus_response_no_timestamps(self):
        """Test conversion with scalar result (no timestamps)."""
        data = {
            "resultType": "scalar",
            "result": [1617898448, "42"]
        }
        
        result = convert_prometheus_response_timestamps(data)
        
        # Should handle gracefully even if structure is different
        assert "resultType" in result

    def test_convert_prometheus_response_preserves_metrics(self):
        """Test that metric labels are preserved during conversion."""
        data = {
            "resultType": "vector",
            "result": [
                {
                    "metric": {
                        "__name__": "http_requests_total",
                        "job": "api-server",
                        "instance": "localhost:9090",
                        "status": "200"
                    },
                    "value": [1617898448, "12345"]
                }
            ]
        }
        
        result = convert_prometheus_response_timestamps(data)
        
        # Verify all metric labels are preserved
        metric = result["result"][0]["metric"]
        assert metric["__name__"] == "http_requests_total"
        assert metric["job"] == "api-server"
        assert metric["instance"] == "localhost:9090"
        assert metric["status"] == "200"
        
        # Verify timestamp was converted
        assert isinstance(result["result"][0]["value"][0], str)
        assert "2021-04-08" in result["result"][0]["value"][0]

    def test_convert_prometheus_response_invalid_input(self):
        """Test conversion with invalid input."""
        # Non-dict input
        result = convert_prometheus_response_timestamps("invalid")
        assert result == "invalid"
        
        # Dict without expected keys
        result = convert_prometheus_response_timestamps({"foo": "bar"})
        assert result["resultType"] is None
        assert result["result"] == []

    def test_timestamp_conversion_multiple_timezones(self):
        """Test that timestamps are consistently UTC."""
        timestamps = [1617898448, 1609459200, 1640995200]
        
        for ts in timestamps:
            result = convert_timestamp_to_iso(ts)
            assert result.endswith("Z"), "All timestamps should be UTC"
            assert "T" in result, "Should use ISO 8601 format with T separator"

