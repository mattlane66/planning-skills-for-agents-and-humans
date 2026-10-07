#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

VERSION="$(python3 - <<'PY'
import json
from pathlib import Path
p=json.loads(Path("plugin.json").read_text())
assert p["version"]=="1.5.3", p["version"]
assert p["extensions"]["com.openai"]["review"]["demo_recording_url"]=="https://mattlane66.github.io/planning-skills-for-agents-and-humans/review/"
print(p["version"])
PY
)"

OUT_DIR="$ROOT_DIR/dist/openai-plugin"
STAGE_DIR="$OUT_DIR/package"
ZIP_PATH="$OUT_DIR/planning-skills-for-agents-and-humans-${VERSION}.zip"

rm -rf "$STAGE_DIR"
mkdir -p "$STAGE_DIR/.codex-plugin" "$OUT_DIR"

cp plugin.json mcp.json AGENTS.md .agent-orchestration.yaml LICENSE "$STAGE_DIR/"
cp .codex-plugin/plugin.json "$STAGE_DIR/.codex-plugin/plugin.json"
cp -R skills templates docs assets "$STAGE_DIR/"

python3 - "$STAGE_DIR" <<'PY'
import json, sys
from pathlib import Path

root=Path(sys.argv[1])
plugin=json.loads((root/"plugin.json").read_text())
codex=json.loads((root/".codex-plugin/plugin.json").read_text())
mcp=json.loads((root/"mcp.json").read_text())

assert plugin["version"]=="1.5.3"
assert codex["version"]=="1.5.3"
assert plugin["extensions"]["com.openai"]["review"]["demo_recording_url"]=="https://mattlane66.github.io/planning-skills-for-agents-and-humans/review/"
assert mcp["mcpServers"]["planning-skills"]["url"]=="https://planning-skills-mcp-production.up.railway.app/mcp"
assert len(list((root/"skills").glob("*/SKILL.md")))==14
for p in ("assets/icon.svg","AGENTS.md",".agent-orchestration.yaml"):
    assert (root/p).exists(), p
print("Validated OpenAI plugin package v1.5.3")
PY

rm -f "$ZIP_PATH" "$ZIP_PATH.sha256"
(
  cd "$STAGE_DIR"
  zip -qrX "$ZIP_PATH" . -x "*/.DS_Store"
)

python3 - "$ZIP_PATH" <<'PY'
import json, sys, zipfile
z=zipfile.ZipFile(sys.argv[1])
names=set(z.namelist())
for p in ("plugin.json","mcp.json",".codex-plugin/plugin.json","assets/icon.svg"):
    assert p in names, p
plugin=json.loads(z.read("plugin.json"))
assert plugin["version"]=="1.5.3"
assert plugin["extensions"]["com.openai"]["review"]["demo_recording_url"]=="https://mattlane66.github.io/planning-skills-for-agents-and-humans/review/"
assert not any(n.startswith("mcp-server/") or n.startswith(".github/") or n.startswith("site/") for n in names)
print("ZIP contents validated")
PY

sha256sum "$ZIP_PATH" > "$ZIP_PATH.sha256"
