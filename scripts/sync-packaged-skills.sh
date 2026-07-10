#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

SKILLS=(
  framing-doc
  shaping
  breadboarding
  interface-contracts
  executable-breadboards
  dumplink
  kickoff-doc
  feed-planning-context
  breadboard-reflection
)

mode="${1:-sync}"

if [[ "$mode" != "sync" && "$mode" != "--check" ]]; then
  echo "Usage: $0 [sync|--check]" >&2
  exit 2
fi

for skill in "${SKILLS[@]}"; do
  source_file="$skill/SKILL.md"
  packaged_file="skills/$skill/SKILL.md"

  if [[ ! -f "$source_file" ]]; then
    echo "Missing canonical skill: $source_file" >&2
    exit 1
  fi

  if [[ "$mode" == "--check" ]]; then
    if [[ ! -f "$packaged_file" ]] || ! cmp -s "$source_file" "$packaged_file"; then
      echo "Packaged skill is out of sync: $packaged_file" >&2
      exit 1
    fi
    echo "✓ $packaged_file matches $source_file"
  else
    mkdir -p "$(dirname "$packaged_file")"
    cp "$source_file" "$packaged_file"
    echo "Synced $packaged_file"
  fi
done
