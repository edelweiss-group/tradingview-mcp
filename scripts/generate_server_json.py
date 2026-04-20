#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate MCP Registry server.json for a released MCPB artifact.")
    parser.add_argument("--version", required=True, help="Released server version, for example 0.3.0")
    parser.add_argument("--artifact-url", required=True, help="Public download URL for the .mcpb artifact")
    parser.add_argument("--sha256", required=True, help="SHA-256 checksum for the .mcpb artifact")
    parser.add_argument("--output", required=True, help="Path to write server.json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    server_metadata = {
        "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
        "name": "io.github.atilaahmettaner/tradingview-mcp",
        "title": "TradingView MCP",
        "description": "Advanced multi-agent AI trading framework and real-time market analysis MCP server",
        "repository": {
            "url": "https://github.com/atilaahmettaner/tradingview-mcp",
            "source": "github",
        },
        "version": args.version,
        "packages": [
            {
                "registryType": "mcpb",
                "identifier": args.artifact_url,
                "fileSha256": args.sha256,
                "transport": {
                    "type": "stdio",
                },
            }
        ],
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(server_metadata, indent=2) + "\n")


if __name__ == "__main__":
    main()
