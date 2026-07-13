#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VIEWER_DIR="$ROOT_DIR/visualizer"

if ! command -v node >/dev/null 2>&1 || ! command -v npm >/dev/null 2>&1; then
  echo "Node.js 20+ and npm are required for the planning diagram viewer." >&2
  exit 1
fi

if [[ ! -f "$VIEWER_DIR/node_modules/mermaid/dist/mermaid.esm.min.mjs" ]]; then
  echo "Installing the local Mermaid viewer dependency..."
  npm --prefix "$VIEWER_DIR" ci --ignore-scripts
fi

exec node "$VIEWER_DIR/src/cli.mjs" "$@"
