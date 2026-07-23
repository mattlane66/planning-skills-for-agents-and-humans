#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

SKILLS=()
while IFS= read -r skill || [[ -n "$skill" ]]; do
  [[ -n "$skill" ]] && SKILLS+=("$skill")
done < skill-inventory.txt

mode="${1:-sync}"

if [[ "$mode" != "sync" && "$mode" != "--check" ]]; then
  echo "Usage: $0 [sync|--check]" >&2
  exit 2
fi

for skill in "${SKILLS[@]}"; do
  source_dir="$skill"
  packaged_dir="skills/$skill"

  if [[ ! -f "$source_dir/SKILL.md" ]]; then
    echo "Missing canonical skill: $source_dir/SKILL.md" >&2
    exit 1
  fi

  if [[ "$mode" == "--check" ]]; then
    if [[ ! -d "$packaged_dir" ]] || ! diff -qr "$source_dir" "$packaged_dir" >/dev/null; then
      echo "Packaged skill directory is out of sync: $packaged_dir" >&2
      diff -qr "$source_dir" "$packaged_dir" || true
      exit 1
    fi
    echo "✓ $packaged_dir matches $source_dir"
  else
    rm -rf "$packaged_dir"
    mkdir -p "$(dirname "$packaged_dir")"
    cp -R "$source_dir" "$packaged_dir"
    echo "Synced $packaged_dir"
  fi
done
