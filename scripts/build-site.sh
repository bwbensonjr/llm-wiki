#!/usr/bin/env bash
#
# Build the published static site from the curated wiki/ layer using Quartz.
#
# Strategy: Quartz v4 is consumed as a project scaffold, not an npm library, so
# we clone a pinned Quartz into .quartz/ (gitignored), overlay our own
# quartz.config.ts, and build wiki/ -> public/. Content is read in place via
# `--directory wiki`; it is never copied, which is what structurally excludes the
# immutable raw/ twins from the published output.
#
# Usage: bash scripts/build-site.sh
set -euo pipefail

QUARTZ_VERSION="v4.5.2"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORK="$ROOT/.quartz"
CONTENT="$ROOT/wiki"
OUTPUT="$ROOT/public"

if [ ! -d "$CONTENT" ]; then
  echo "error: wiki/ content directory not found at $CONTENT" >&2
  exit 1
fi

if [ ! -f "$ROOT/quartz.config.ts" ]; then
  echo "error: quartz.config.ts not found at repo root" >&2
  exit 1
fi

# Clone the pinned Quartz once; reuse the checkout on subsequent builds.
if [ ! -d "$WORK/.git" ]; then
  rm -rf "$WORK"
  echo "Cloning Quartz $QUARTZ_VERSION into .quartz/ ..."
  git clone --quiet --depth 1 --branch "$QUARTZ_VERSION" \
    https://github.com/jackyzha0/quartz.git "$WORK"
fi

# Overlay our configuration onto the pinned checkout.
cp "$ROOT/quartz.config.ts" "$WORK/quartz.config.ts"

cd "$WORK"
npm ci
npx quartz build --directory "$CONTENT" --output "$OUTPUT"

echo "Built site -> $OUTPUT"
