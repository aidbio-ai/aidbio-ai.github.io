#!/usr/bin/env bash
# Vendors the design-system CSS tokens from the sibling aidbio-design repo
# into assets/ds/. Run this whenever aidbio-design/tokens or styles.css change.
set -euo pipefail

SITE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DS_ROOT="$SITE_ROOT/../aidbio-design"
DEST="$SITE_ROOT/assets/ds"

if [ ! -d "$DS_ROOT" ]; then
  echo "error: expected aidbio-design repo at $DS_ROOT (sibling of this repo)" >&2
  exit 1
fi

mkdir -p "$DEST/tokens"

rsync -a --delete "$DS_ROOT/tokens/" "$DEST/tokens/"
cp "$DS_ROOT/styles.css" "$DEST/styles.css"

echo "Synced design-system tokens into $DEST"
