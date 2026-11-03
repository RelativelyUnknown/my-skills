---
name: building-animation-scenes
description: "Builds a time-driven SVG animation scene (pop, draw, fly, grow) and renders it to PNG frames and MP4/WebM/GIF with headless Chromium and ffmpeg. Use when asked to create or edit an animated explainer, chart or process animation for a PowerPoint deck."
---

# Building animation scenes

A scene is a pure function of time: `renderAt(t)` sets every attribute for second `t`. Frames can be rendered in any order and are identical on every run. Follow `powerpoint-animation-style` for how it should look.

## Setup (once)

1. Copy `<this skill's folder>/assets/` to a working folder (not into the skill). It holds `helpers.js`, `common.js`, `stage.html`, `style.css`, `specs.js`, `package.json` and `scenes/example.js`.
2. Needs `node` 20+, `ffmpeg`, and Playwright with Chromium (`npm i playwright` somewhere resolvable, or a global install with `NODE_PATH` set). `build.sh` runs `npm install` for the two font packages the first time.

## Make a scene

1. Add data to `specs.js`: `window.SPECS.<scene> = { title, … }`. Plain numbers and strings. Compute real values in your own code and paste or generate the file; scenes only draw, never compute.
2. Copy `scenes/example.js` to `scenes/<scene>.js`. Keep this shape:
   - `makeStage(title)` returns `{ dyn }`; add everything to `dyn`.
   - `splitHeader(dyn, [left, right])`, `makeChart(dyn, PANELS.left, spec, { ticks })`, `valuePill`, `emptySlot`, `ring` are in `common.js`; `S`, `seg`, `win`, `lerp`, `ease`, `draw`, `pop` in `helpers.js`.
   - Create all elements up front with `opacity: 0`; the loop only updates attributes.
   - Finish with `finish(dyn, END, t => { … })`, where `END` is the time of the last event.
3. Per element, derive progress with `seg(t, start, end)` (0..1), shape it with `ease.out | inOut | back`, then apply: `pop` for scale-in, `draw` for stroke-in, `lerp` for moves, `place` for a (0,0)-centred group. Name start times as constants at the top (`BIN0`, `PILLS0`) so the choreography reads as a script.
4. Preview stills while designing:
   `node <skill>/scripts/render.js <work>/assets <scene> <work>/prev --times 1,2.5,4,6.5`
   and look at them. Check overlaps, text clipping and that mid-motion frames are legible, not only the last one.
5. Build everything:
   `bash <skill>/scripts/build.sh <work>/assets <work>/out <scene> [more scenes]`
   Output: `out/mp4`, `out/webm`, `out/gif`. Scenes render in parallel.

## Rules

- No wall-clock time, no `Math.random()`, no CSS animations or transitions: they break determinism.
- Gate "appears at time a" with `opacity = t >= a ? 1 : 0` or `seg`, never by creating elements late.
- Stroke-dash paths (`draw`) need `fill: none`; call `draw` every frame, including with progress 0.
- Keep text inside its pill or tile: mono 13 px fits about 6 characters in a 60 px pill.
- Chart-specific layout (`makeChart`) is optional; for other layouts build with `S('rect' | 'path' | …)` and `T()` directly.
- References: see `references/motion-recipes.md` for ready-made timing patterns.
