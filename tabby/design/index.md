# Design: diagrams and explainer animations

Say one thing per picture. Delete a node or a line when the picture still works without it.

1. A diagram: read `design/diagrams/choosing.md` first (whether to draw, which type, the budget, how to build and check it), then the type's page under `design/diagrams/types/`.
2. Read `design/diagrams/style.md`: the tokens (light and dark), the builder (`assets/diagram/make.mjs`) and how a `design.md` at the repository root maps onto them.
3. Animation: also read `design/animation/index.md`, then `pipeline.md` and `motion.md`; `formats.md` only if video is asked for. The default is one self-contained animated HTML built by `design/assets/animation/animate.mjs` (Node 22; Playwright Chromium to check it; ffmpeg only for video: ask before installing any of them).
4. Run `check.py` (and `check-motion.mjs` for an animation), render the picture, and look at it in light and dark. Check it at its smallest display size before reporting it done. If text cannot be read there, cut text.

Defaults: `## Tabby` or `## Python defaults` in AGENTS.md. Ask only what is still unknown.
