#!/usr/bin/env bash
# build.sh — frames → MP4 / WebM / GIF for one or more scenes.
# Usage: build.sh <assets_dir> <out_dir> <scene> [scene …]
#   <assets_dir>  your working copy of assets/ (stage.html, specs.js, scenes/, node_modules/)
#   <out_dir>     receives gif/, mp4/, webm/ (frames go to <out_dir>/.frames/<scene>)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ASSETS=$1; OUT=$2; shift 2
[ $# -gt 0 ] || { echo "usage: build.sh <assets_dir> <out_dir> <scene> [scene …]"; exit 2; }
[ -d "$ASSETS/node_modules/@fontsource/inter" ] || (cd "$ASSETS" && npm install --silent)
for k in "$@"; do rm -rf "$OUT/.frames/$k"; node "$HERE/render.js" "$ASSETS" "$k" "$OUT/.frames/$k" & done; wait
for k in "$@"; do "$HERE/../../exporting-animations-to-powerpoint/scripts/encode.sh" "$OUT/.frames/$k" "$OUT" "$k" & done; wait
echo "Done → $OUT/gif, $OUT/mp4, $OUT/webm"
