#!/usr/bin/env bash
# encode.sh — turn a folder of 2× PNG frames into MP4 + WebM (1920×1080) and a GIF (960×540).
# Usage: ./encode.sh <frames_dir> <out_root> <name>
#   → <out_root>/mp4/<name>.mp4   <out_root>/webm/<name>.webm   <out_root>/gif/<name>.gif
set -euo pipefail
F=$1; OUT=$2; NAME=$3; FPS=25
mkdir -p "$OUT/gif" "$OUT/mp4" "$OUT/webm"
PAL="$OUT/.palette-$NAME.png"

# MP4 (H.264): widest support (PowerPoint, Keynote, browsers). yuv420p + faststart so it plays inline.
ffmpeg -loglevel error -y -framerate $FPS -i "$F/f_%04d.png" \
  -c:v libx264 -pix_fmt yuv420p -crf 20 -preset slow -movflags +faststart "$OUT/mp4/$NAME.mp4"

# WebM (VP9): smallest file for modern browsers.
ffmpeg -loglevel error -y -framerate $FPS -i "$F/f_%04d.png" \
  -c:v libvpx-vp9 -b:v 0 -crf 36 -row-mt 1 -pix_fmt yuv420p "$OUT/webm/$NAME.webm"

# GIF at 1×: one palette built from all frames, then mapped without dithering (flat fills stay clean).
# 96 colours: the charts add anti-aliased lines in two hues, which 64 colours would band.
ffmpeg -loglevel error -y -framerate $FPS -i "$F/f_%04d.png" \
  -vf "scale=iw/2:ih/2:flags=lanczos,palettegen=max_colors=96:stats_mode=full" "$PAL"
ffmpeg -loglevel error -y -framerate $FPS -i "$F/f_%04d.png" -i "$PAL" \
  -lavfi "scale=iw/2:ih/2:flags=lanczos[x];[x][1:v]paletteuse=dither=none:diff_mode=rectangle" \
  -loop 0 "$OUT/gif/$NAME.gif"
rm -f "$PAL"
echo "$NAME: gif $(du -h "$OUT/gif/$NAME.gif" | cut -f1), mp4 $(du -h "$OUT/mp4/$NAME.mp4" | cut -f1), webm $(du -h "$OUT/webm/$NAME.webm" | cut -f1)"
