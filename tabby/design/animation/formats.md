# Formats

**The animated HTML is the default.** It is a few tens of kilobytes, stays sharp at any size, honours `prefers-reduced-motion` and the viewer's light or dark scheme, and needs nothing to open. Use video only where a page cannot run it: a README that must autoplay, a slide, a chat message.

```bash
node assets/animation/render-video.mjs anim.html out.mp4            # H.264, plays everywhere
node assets/animation/render-video.mjs anim.html out.webm           # VP9, smallest for web pages
node assets/animation/render-video.mjs anim.html out.gif --fps 12   # where video does not autoplay (README files)
```

Options: `--fps` (default 30), `--scale` (default 2; the frame is the diagram's own size times this), `--dark` for the dark scheme, `--loops N`. Frames come from seeking the page, so every run is identical.

- Needs Playwright with Chromium and ffmpeg: ask before installing either. For video that matches the diagram exactly, Inter should be resolvable (`@fontsource/inter` in the working folder); without it a fallback font shows and the report says so.
- MP4 and WebM are encoded yuv420p with even dimensions so they play inline; MP4 has faststart.
- GIF uses one 96-colour palette built from all frames and no dithering, so flat fills stay clean. 12 fps is enough for this kind of motion; the file is the largest per second of the three.
- Pick by destination: MP4 for documents and most players, WebM for web pages, GIF where video will not autoplay.
- Look at a frame from the output before reporting: extract one with `ffmpeg -i out.mp4 -vf "select=eq(n\,60)" -frames:v 1 check.png`.
