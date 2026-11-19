#!/usr/bin/env bash
# Build the deck and publish it as a new GitHub Release, so every version stays on the releases page.
# The version is the newest "## x.y.z" heading in CHANGELOG.md, the tag vx.y.z, the title the deck's
# name (README.md's first line) and the notes that version's changelog section. Add the version to
# CHANGELOG.md and point the download links at it (scripts/check-release-links.sh checks them) in
# the PR, then publish from main after merging:
#   scripts/publish.sh
set -euo pipefail
cd "$(dirname "$0")/.."
[ -z "$(git status --porcelain)" ] || { echo "commit your changes first" >&2; exit 1; }
version=$(scripts/version.sh)
tag="v$version"
if gh release view "$tag" >/dev/null 2>&1; then
  echo "$tag is already published: add a new version to CHANGELOG.md" >&2; exit 1
fi
[ -f .gitmodules ] && git submodule update --init -q
uv run --no-project -q -p 3.13 --with genanki==0.13.1 python build.py
apkg=$(ls ./*.apkg)
# The section under the newest version heading, up to the next one.
changes=$(awk '/^## /{n++; next} n==1' CHANGELOG.md)
notes="$changes

Built from $(git rev-parse --short HEAD). Open the .apkg with Anki to import or update the deck."
git tag "$tag" HEAD
git push origin "refs/tags/$tag"
gh release create "$tag" "$apkg" --title "$(head -1 README.md | sed 's/^# //') $version" --notes "$notes"
