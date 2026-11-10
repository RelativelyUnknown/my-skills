# design

A module of [Tabby](../SKILL.md) for minimalist diagrams and explainer animations: one idea per picture, a restrained visual language, and a `design.md` at the repository root honoured when there is one. Output is SVG, MP4, WebM or GIF.

**Entry point:** [`index.md`](index.md), about 190 tokens.

## Layout

```
index.md
diagrams/         index.md  choosing.md  style.md     when and what to draw; visual language, mapped from design.md onto the theme
animation/        index.md  pipeline.md  motion.md  formats.md
assets/animation/                                     the render engine: common.js, helpers.js, render.js, specs.js, stage.html, style.css, scenes/
```

The pipeline draws SVG scenes as a function of time, renders frames in headless Chromium, and encodes them with ffmpeg. It needs Node 22, Playwright Chromium and ffmpeg; the agent asks before installing any of them. The commands are in [`animation/formats.md`](animation/formats.md).

## Evals

None yet.

## Licence

MIT. The engine's two font packages (`@fontsource/inter`, `@fontsource/jetbrains-mono`) are declared in `assets/animation/package.json` and installed with `npm install`; they are not part of this repository.
