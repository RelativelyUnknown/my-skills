#!/usr/bin/env python3
"""Put rendered animations on PowerPoint slides (python-pptx).

Usage:
  python3 embed_in_pptx.py deck.pptx out/mp4/a.mp4 [out/mp4/b.mp4 …] [--poster-dir out/.frames]

One 16:9 slide per video. Each MP4 is embedded as a movie that fills the slide, with a poster
frame (a late, fully drawn frame, if --poster-dir has <name>/f_*.png; otherwise PowerPoint's default) so the slide looks right before it plays. Autoplay and looping are set in PowerPoint
(Playback tab: Start = Automatically, Loop until Stopped); python-pptx cannot set them safely.
Needs: pip install python-pptx
"""
import argparse
import glob
import os
import sys

from pptx import Presentation
from pptx.util import Emu


def poster_for(video: str, poster_dir: str | None) -> str | None:
    if not poster_dir:
        return None
    frames = sorted(glob.glob(os.path.join(poster_dir, os.path.splitext(os.path.basename(video))[0], "f_*.png")))
    return frames[len(frames) * 3 // 4] if frames else None   # late frame: everything drawn, before the fade


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("videos", nargs="+")
    ap.add_argument("--poster-dir")
    a = ap.parse_args()

    prs = Presentation(a.deck) if os.path.exists(a.deck) else Presentation()
    if not os.path.exists(a.deck):
        prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)   # 16:9, 13.333 × 7.5 in
    blank = prs.slide_layouts[6]
    for video in a.videos:
        slide = prs.slides.add_slide(blank)
        poster = poster_for(video, a.poster_dir)
        slide.shapes.add_movie(video, 0, 0, prs.slide_width, prs.slide_height,
                               poster_frame_image=poster, mime_type="video/mp4")
        print(f"slide {len(prs.slides)}: {os.path.basename(video)}" + (f" (poster {os.path.basename(poster)})" if poster else ""))
    prs.save(a.deck)
    return 0


if __name__ == "__main__":
    sys.exit(main())
