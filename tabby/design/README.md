# design

A module of [Tabby](../SKILL.md) for diagrams and explainer animations: one idea per picture, one quiet visual language (white ground, soft zones, one accent, light and dark), a builder that turns a small JSON spec into an SVG, mechanical checks, and a `design.md` at the repository root honoured when there is one. Output is SVG; MP4, WebM and GIF come from the animation engine.

**Entry point:** [`index.md`](index.md), about 190 tokens.

## Layout

```
index.md
diagrams/         index.md  choosing.md  style.md  connectors.md  icons.md  types/   when and what to draw; look; connectors; icons; one page per type
animation/        index.md  pipeline.md  motion.md  formats.md
assets/diagram/   make.mjs  check.py  selftest.py  render.mjs  examples/              build from a spec, check, prove the checker can fail, render
assets/icons/     tabler-outline.json  build-icons.mjs  LICENSE.tabler               5,233 outline icons (MIT)
assets/animation/                                     the render engine: common.js, helpers.js, render.js, specs.js, stage.html, style.css, scenes/
SOURCE.md                                             what was taken from which source
```

The pipeline draws SVG scenes as a function of time, renders frames in headless Chromium, and encodes them with ffmpeg. It needs Node 22, Playwright Chromium and ffmpeg; the agent asks before installing any of them. The commands are in [`animation/formats.md`](animation/formats.md).

## Evals

`assets/diagram/selftest.py` is the checker's own test: every example passes and each of nine seeded defects is caught. Run it after any change to `check.py`, `make.mjs` or the tokens.

## Licence

MIT. The engine's two font packages (`@fontsource/inter`, `@fontsource/jetbrains-mono`) are declared in `assets/animation/package.json` and installed with `npm install`; they are not part of this repository.
