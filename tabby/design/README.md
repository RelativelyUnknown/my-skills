# design

A module of [Tabby](../SKILL.md) for diagrams and explainer animations: one idea per picture, one quiet visual language (white ground, soft zones, one accent, light and dark), a builder that turns a small JSON spec into an SVG, mechanical checks, and a `design.md` at the repository root honoured when there is one. Output is SVG for a diagram and one self-contained animated HTML for an explainer; MP4, WebM and GIF are rendered from that HTML on request.

**Entry point:** [`index.md`](index.md), about 190 tokens.

## Layout

```
index.md
diagrams/         index.md  choosing.md  style.md  connectors.md  icons.md  types/   when and what to draw; look; connectors; icons; one page per type
animation/        index.md  pipeline.md  motion.md  formats.md
assets/diagram/   make.mjs  check.py  selftest.py  render.mjs  examples/              build from a spec, check, prove the checker can fail, render
assets/icons/     tabler-outline.json  build-icons.mjs  LICENSE.tabler               5,233 outline icons (MIT)
assets/animation/ animate.mjs  check-motion.mjs  selftest-motion.mjs  render-video.mjs  templates/   build, check, prove the checker, encode video
SOURCE.md                                             what was taken from which source
```

An animation is the same spec as a diagram plus a `story`; `animate.mjs` writes one HTML file whose picture is a pure function of time. Video is rendered by seeking it. Node 22 and Playwright Chromium check it, and ffmpeg is needed only for video; the agent asks before installing any of them. The steps are in [`animation/pipeline.md`](animation/pipeline.md).

## Evals

`assets/diagram/selftest.py` and `assets/animation/selftest-motion.mjs` are the checkers' own tests: every example passes and each seeded defect (nine for diagrams, eight for animation) is caught. Run them after any change to a checker, the builder, the player or the tokens.

## Licence

MIT. The vendored icons are Tabler Icons (MIT, `assets/icons/LICENSE.tabler`). No fonts are bundled: Inter and JetBrains Mono are used when installed, with a system fallback.
