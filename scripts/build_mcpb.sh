#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${1:-$ROOT_DIR/dist}"

cd "$ROOT_DIR"

VERSION="${VERSION:-$(python3 - <<'PY'
import re
from pathlib import Path

match = re.search(r'^version\s*=\s*"([^"]+)"', Path("pyproject.toml").read_text(), re.M)
if not match:
    raise SystemExit("Could not determine version from pyproject.toml")
print(match.group(1))
PY
)}"

ARTIFACT="$OUTPUT_DIR/tradingview-mcp-$VERSION.mcpb"

mkdir -p "$OUTPUT_DIR"

npx -y @anthropic-ai/mcpb validate .
npx -y @anthropic-ai/mcpb pack . "$ARTIFACT"

shasum -a 256 "$ARTIFACT" | awk '{print $1}' > "$ARTIFACT.sha256"

printf 'Created %s\n' "$ARTIFACT"
printf 'SHA256 %s\n' "$(cat "$ARTIFACT.sha256")"
