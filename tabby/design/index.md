# Design: diagrams and explainer animations

Say one thing per picture. Delete a node or a line when the picture still works without it.

1. A diagram: read `design/diagrams/choosing.md` first (whether to draw, which type, the budget).
2. Read `design/diagrams/style.md`: the colour and font tokens (light and dark) shared by diagrams and animations, and how a `design.md` at the repository root maps onto them.
3. Animation or video: also read `design/animation/index.md`, then `pipeline.md`, `motion.md`, `formats.md` as needed. The engine is in `design/assets/animation/` (needs Node 22, Playwright Chromium and ffmpeg: ask before installing any of them).
4. Render the picture and look at it. Check it at its smallest display size before reporting it done. If text cannot be read there, cut text.

Defaults: `## Tabby` or `## Python defaults` in AGENTS.md. Ask only what is still unknown.
