#!/usr/bin/env bash
# Fail when README.md's download links don't point at the current version: every
# releases/download/v<version>/ and releases/tag/v<version> link must use the newest version in
# CHANGELOG.md, and there must be a download link. Run by .local-ci.
set -euo pipefail
cd "$(dirname "$0")/.."
version=$(scripts/version.sh)
links=$(grep -oE "releases/(download|tag)/v[^/) ]*" README.md || true)
status=0
if ! grep -qx "releases/download/v$version" <<<"$links"; then
  echo "README.md: no download link for $version" >&2; status=1
fi
stale=$(grep -vxE "releases/(download|tag)/v$version" <<<"$links" || true)
if [ -n "$stale" ]; then
  echo "README.md: links not at $version:" $stale >&2; status=1
fi
[ $status -eq 0 ] && echo "download links match CHANGELOG.md ($version)"
exit $status
