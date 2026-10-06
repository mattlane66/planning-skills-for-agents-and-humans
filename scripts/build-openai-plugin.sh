#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

VERSION="$(python3 - <<'PY'
import json
from pathlib import Path

plugin = json.loads(Path("plugin.json").read_text(encoding="utf-8"))
version = plugin.get("version")
if not isinstance(version, str) or not version.strip():
    raise SystemExit("plugin.json is missing a non-empty version")
print(version)
PY
)"

OUT_DIR="$ROOT_DIR/dist/openai-plugin"
STAGE_DIR="$OUT_DIR/package"
ZIP_PATH="$OUT_DIR/planning-skills-for-agents-and-humans-${VERSION}.zip"
SHA_PATH="$ZIP_PATH.sha256"

rm -rf "$STAGE_DIR"
mkdir -p "$STAGE_DIR/.codex-plugin" "$OUT_DIR"

copy_file() {
  local src="$1"
  local dest="$2"
  if [[ ! -f "$src" ]]; then
    echo "Missing required file: $src" >&2
    exit 1
  fi
  mkdir -p "$(dirname "$dest")"
  cp "$src" "$dest"
}

copy_dir() {
  local src="$1"
  local dest="$2"
  if [[ ! -d "$src" ]]; then
    echo "Missing required directory: $src" >&2
    exit 1
  fi
  cp -R "$src" "$dest"
}

copy_file "plugin.json" "$STAGE_DIR/plugin.json"
copy_file "mcp.json" "$STAGE_DIR/mcp.json"
copy_file ".codex-plugin/plugin.json" "$STAGE_DIR/.codex-plugin/plugin.json"
copy_file "AGENTS.md" "$STAGE_DIR/AGENTS.md"
copy_file ".agent-orchestration.yaml" "$STAGE_DIR/.agent-orchestration.yaml"
copy_file "LICENSE" "$STAGE_DIR/LICENSE"

copy_dir "skills" "$STAGE_DIR/skills"
copy_dir "templates" "$STAGE_DIR/templates"
copy_dir "docs" "$STAGE_DIR/docs"

python3 - "$STAGE_DIR" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])

plugin = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
mcp = json.loads((root / "mcp.json").read_text(encoding="utf-8"))
codex = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))

if plugin.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
    raise SystemExit("plugin.json does not use the portable Agent Plugins schema")
if plugin.get("name") != "planning-skills-for-agents-and-humans":
    raise SystemExit("Unexpected plugin name")
if codex.get("name") != plugin.get("name"):
    raise SystemExit("Portable and Codex plugin names differ")
if codex.get("version") != plugin.get("version"):
    raise SystemExit("Portable and Codex plugin versions differ")

servers = mcp.get("mcpServers")
if not isinstance(servers, dict) or len(servers) != 1:
    raise SystemExit("mcp.json must contain exactly one MCP server")
server = servers.get("planning-skills")
if not isinstance(server, dict):
    raise SystemExit("mcp.json is missing the planning-skills server")
if server.get("type") != "streamable-http":
    raise SystemExit("planning-skills MCP must use streamable-http")
expected_url = "https://planning-skills-mcp-production.up.railway.app/mcp"
if server.get("url") != expected_url:
    raise SystemExit(f"Unexpected MCP URL: {server.get('url')!r}")

skills_dir = root / "skills"
skills = sorted(path.parent.name for path in skills_dir.glob("*/SKILL.md"))
if not skills:
    raise SystemExit("No packaged skills found")

for skill in skills:
    skill_file = skills_dir / skill / "SKILL.md"
    if skill_file.stat().st_size == 0:
        raise SystemExit(f"Empty SKILL.md: {skill}")

for forbidden in ("mcp-server", ".github", "tests", "site", "visualizer", "hooks", ".git"):
    if (root / forbidden).exists():
        raise SystemExit(f"Development-only path leaked into package: {forbidden}")

required_support = [
    root / "AGENTS.md",
    root / ".agent-orchestration.yaml",
    root / "templates",
    root / "docs",
]
for path in required_support:
    if not path.exists():
        raise SystemExit(f"Missing packaged support path: {path.relative_to(root)}")

print(f"Validated {len(skills)} packaged skills")
PY

rm -f "$ZIP_PATH" "$SHA_PATH"
(
  cd "$STAGE_DIR"
  zip -qrX "$ZIP_PATH" . -x "*/.DS_Store"
)

python3 - "$ZIP_PATH" <<'PY'
import sys
import zipfile
from pathlib import Path

archive = Path(sys.argv[1])
with zipfile.ZipFile(archive) as zf:
    names = set(zf.namelist())
    required = {
        "plugin.json",
        "mcp.json",
        ".codex-plugin/plugin.json",
    }
    missing = required - names
    if missing:
        raise SystemExit(f"ZIP missing required root entries: {sorted(missing)}")
    if not any(name.startswith("skills/") and name.endswith("/SKILL.md") for name in names):
        raise SystemExit("ZIP contains no skills/*/SKILL.md files")
    if any(name.startswith("planning-skills-for-agents-and-humans/") for name in names):
        raise SystemExit("ZIP is incorrectly wrapped in an extra top-level folder")
PY

if command -v shasum >/dev/null 2>&1; then
  shasum -a 256 "$ZIP_PATH" > "$SHA_PATH"
else
  sha256sum "$ZIP_PATH" > "$SHA_PATH"
fi

echo "Built: $ZIP_PATH"
echo "Checksum: $SHA_PATH"
