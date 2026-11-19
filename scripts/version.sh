#!/usr/bin/env bash
# Print the deck's current version: the first "## x.y.z" heading in CHANGELOG.md.
set -euo pipefail
cd "$(dirname "$0")/.."
version=$(grep -m1 -oE '^## [0-9]+\.[0-9]+\.[0-9]+' CHANGELOG.md | cut -c4-) || true
[ -n "$version" ] || { echo "CHANGELOG.md has no '## x.y.z' heading" >&2; exit 1; }
echo "$version"
