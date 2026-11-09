# Encoding formats

`render.js` writes 2× PNG frames (`f_0001.png`, …; 1920×1080 for the 960×540 stage) to `out/.frames/<scene>`. Encode from there at 25 fps. With `F=out/.frames/<scene>` and `N=<scene>`:

```bash
mkdir -p out/mp4 out/webm out/gif
# MP4 (H.264): widest support. yuv420p and faststart so it plays inline.
ffmpeg -loglevel error -y -framerate 25 -i "$F/f_%04d.png" -c:v libx264 -pix_fmt yuv420p -crf 20 -preset slow -movflags +faststart out/mp4/$N.mp4
# WebM (VP9): smallest file for modern browsers.
ffmpeg -loglevel error -y -framerate 25 -i "$F/f_%04d.png" -c:v libvpx-vp9 -b:v 0 -crf 36 -row-mt 1 -pix_fmt yuv420p out/webm/$N.webm
# GIF at 960×540: one palette from all frames, mapped without dithering so flat fills stay clean.
ffmpeg -loglevel error -y -framerate 25 -i "$F/f_%04d.png" -vf "scale=iw/2:ih/2:flags=lanczos,palettegen=max_colors=96:stats_mode=full" out/.palette-$N.png
ffmpeg -loglevel error -y -framerate 25 -i "$F/f_%04d.png" -i out/.palette-$N.png -lavfi "scale=iw/2:ih/2:flags=lanczos[x];[x][1:v]paletteuse=dither=none:diff_mode=rectangle" -loop 0 out/gif/$N.gif
```

- 96 colours: charts add anti-aliased lines in two hues, which 64 colours would band.
- Pick the format by destination: MP4 for documents and most players, WebM for web pages, GIF where video does not autoplay (README files).
- Scenes are independent: render several in parallel with `&` and `wait`.
