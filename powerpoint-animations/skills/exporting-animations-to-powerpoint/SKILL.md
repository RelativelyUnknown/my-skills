---
name: exporting-animations-to-powerpoint
description: "Encodes rendered animation frames to MP4, WebM and GIF, and puts them on PowerPoint slides. Use when a finished animation needs to go into a .pptx, when picking MP4 vs GIF, or when an animation looks soft, bands, or will not play in PowerPoint."
---

# Exporting animations to PowerPoint

Input: a folder of 2× PNG frames from `building-animation-scenes` (`f_0000.png`, …).

## Pick the format

| Format | Use | Notes |
| --- | --- | --- |
| **MP4 (H.264)** | PowerPoint, Keynote, Google Slides upload | Best quality, 1920×1080. Default for decks. |
| **GIF** | email, wiki, anywhere video is blocked | 960×540, 96 colours, no dither. About 2× the size of MP4. |
| **WebM (VP9)** | web pages | Smallest. Not for PowerPoint. |

## Encode

`bash <skill>/scripts/encode.sh <frames_dir> <out_root> <name>` writes `mp4/`, `webm/`, `gif/` (25 fps). `building-animation-scenes/scripts/build.sh` calls it for you.

Why these settings: MP4 uses `yuv420p` and `+faststart` so PowerPoint plays it inline; the GIF palette is built from all frames and applied without dithering so flat fills stay clean (96 colours because anti-aliased lines in two hues band at 64).

## Put it in a deck

`python3 <skill>/scripts/embed_in_pptx.py deck.pptx out/mp4/<name>.mp4 [more.mp4 …] --poster-dir out/.frames`

- Needs `pip install python-pptx`. Creates the deck (16:9) if it does not exist, otherwise appends one full-bleed slide per video.
- The poster frame is a late, fully drawn frame, so the slide looks finished in thumbnails and before playing.
- Autoplay and looping cannot be set by python-pptx. In PowerPoint: select the video, Playback tab, Start = Automatically, tick Loop until Stopped.
- To place a clip inside an existing slide instead, insert it in PowerPoint (Insert, Video, This Device) and size it to 16:9; keep the aspect ratio.
- A GIF can also be inserted as a picture (Insert, Pictures); it loops by itself, but file size and colour are worse.

## Check before shipping

1. `python3 <skill>/scripts/contact_sheet.py sheet.png out/gif/<name>.gif --frames 20,60,110,160` and look at the result: no clipped text, no empty first frame.
2. `ffprobe out/mp4/<name>.mp4`: 1920×1080, 25 fps, `yuv420p`.
3. Open the deck and play the slide in slideshow mode once; embedded video does not show motion in the editing view of every PowerPoint version.
4. Keep the video file next to the deck if you link instead of embed.
