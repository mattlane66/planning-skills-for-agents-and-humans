#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

VERSION="$(python3 - <<'PY'
import json
from pathlib import Path
print(json.loads(Path("plugin.json").read_text(encoding="utf-8"))["version"])
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

root = Path(sys.argv[1])
plugin = json.loads((root / "plugin.json").read_text())
mcp = json.loads((root / "mcp.json").read_text())

assert plugin["version"] == "1.5.2"
assert plugin["extensions"]["com.openai"]["interface"]["displayName"] == "Planning Skills"
assert len(plugin["extensions"]["com.openai"]["interface"]["displayName"]) <= 30
assert len(plugin["extensions"]["com.openai"]["interface"]["shortDescription"]) <= 30
assert len(plugin["extensions"]["com.openai"]["interface"]["defaultPrompt"]) <= 3
assert all(len(p) <= 128 for p in plugin["extensions"]["com.openai"]["interface"]["defaultPrompt"])

for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
    value = plugin["extensions"]["com.openai"]["interface"].get(field)
    assert isinstance(value, str) and value.startswith("https://"), field

for field in ("logo", "composerIcon"):
    p = plugin["extensions"]["com.openai"]["interface"][field]
    assert p.startswith("./")
    assert (root / p[2:]).is_file(), p

server = mcp["mcpServers"]["planning-skills"]
assert server["type"] == "streamable-http"
assert server["url"] == "https://planning-skills-mcp-production.up.railway.app/mcp"

skills = list((root / "skills").glob("*/SKILL.md"))
assert len(skills) == 14, len(skills)

review = plugin["extensions"]["com.openai"]["review"]["test_cases"]
assert len(review["positive"]) == 5
assert len(review["negative"]) == 3

print("Validated public OpenAI plugin package:", plugin["version"])
print("Skills:", len(skills))
PY

rm -f "$ZIP_PATH"
(
  cd "$STAGE_DIR"
  zip -qrX "$ZIP_PATH" . -x "*/.DS_Store"
)

python3 - "$ZIP_PATH" <<'PY'
import sys, zipfile
archive = sys.argv[1]
with zipfile.ZipFile(archive) as z:
    names=set(z.namelist())
    for p in ("plugin.json","mcp.json","assets/icon.svg",".codex-plugin/plugin.json"):
        assert p in names, p
    assert any(n.startswith("skills/") and n.endswith("/SKILL.md") for n in names)
    for bad in ("mcp-server/", ".github/", "tests/", "site/", "visualizer/"):
        assert not any(n.startswith(bad) for n in names), bad
print("ZIP structure validated")
PY

shasum -a 256 "$ZIP_PATH" > "$ZIP_PATH.sha256"
echo "$ZIP_PATH"
cat "$ZIP_PATH.sha256"
