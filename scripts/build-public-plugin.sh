#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VERSION="$(python3 - <<'PY'
import json
from pathlib import Path
p=json.loads(Path("plugin.json").read_text())
print(p["version"])
PY
)"

OUT="$ROOT/dist/openai-public-plugin"
PKG="$OUT/package"
ZIP="$OUT/planning-skills-for-agents-and-humans-${VERSION}-public.zip"
rm -rf "$OUT"
mkdir -p "$PKG/.codex-plugin" "$PKG/assets"

cp plugin.json mcp.json AGENTS.md .agent-orchestration.yaml LICENSE "$PKG/"
cp .codex-plugin/plugin.json "$PKG/.codex-plugin/plugin.json"
cp -R skills templates docs "$PKG/"
cp assets/icon.svg "$PKG/assets/icon.svg"

python3 - "$PKG" <<'PY'
import json, re, sys
from pathlib import Path
root=Path(sys.argv[1])
plugin=json.loads((root/"plugin.json").read_text())
codex=json.loads((root/".codex-plugin/plugin.json").read_text())
mcp=json.loads((root/"mcp.json").read_text())

assert plugin["version"] == "1.5.1"
assert codex["version"] == plugin["version"]
ext=plugin["extensions"]["com.openai"]
ui=ext["interface"]
assert len(ui["displayName"]) <= 30
assert len(ui["shortDescription"]) <= 30
assert len(ui["longDescription"]) <= 4000
assert len(ui["defaultPrompt"]) <= 3
assert all(len(p) <= 128 for p in ui["defaultPrompt"])
for key in ("websiteURL","supportURL","privacyPolicyURL","termsOfServiceURL"):
    assert ui[key].startswith("https://"), key
for key in ("composerIcon","logo"):
    assert ui[key] == "./assets/icon.svg"
review=ext["review"]["test_cases"]
assert len(review["positive"]) == 5
assert len(review["negative"]) == 3
assert all(c.get("tools_triggered") and c.get("expected_behavior") for c in review["positive"])
assert ext["review"]["commerce"] is False
servers=mcp["mcpServers"]
assert list(servers) == ["planning-skills"]
assert servers["planning-skills"]["type"] == "streamable-http"
assert servers["planning-skills"]["url"] == "https://planning-skills-mcp-production.up.railway.app/mcp"

svg=(root/"assets/icon.svg").read_text()
assert re.search(r'<svg[^>]+width="512"[^>]+height="512"[^>]+viewBox="0 0 512 512"', svg)
skills=list((root/"skills").glob("*/SKILL.md"))
assert len(skills) == 14, len(skills)
print("validated public plugin package:", len(skills), "skills")
PY

(
 cd "$PKG"
 zip -qrX "$ZIP" . -x "*/.DS_Store"
)

python3 - "$ZIP" <<'PY'
import sys, zipfile
z=zipfile.ZipFile(sys.argv[1])
names=set(z.namelist())
for required in ("plugin.json","mcp.json",".codex-plugin/plugin.json","assets/icon.svg"):
    assert required in names, required
assert sum(1 for n in names if n.startswith("skills/") and n.endswith("/SKILL.md")) == 14
for forbidden in ("mcp-server/",".github/","tests/","site/","visualizer/","hooks/"):
    assert not any(n.startswith(forbidden) for n in names), forbidden
print("zip layout validated")
PY

shasum -a 256 "$ZIP" > "$ZIP.sha256"
echo "$ZIP"
