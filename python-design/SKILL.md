---
name: python-design
description: "Use when making a diagram, an architecture or flow picture, or a short explainer animation for a project. Minimalist, readable, reads the project's design.md if it has one; outputs SVG, MP4, WebM or GIF.."
license: MIT
---

# Python design: diagrams and explainer animations

Say one thing per picture. Delete a node or a line when the picture still works without it.

1. Read `references/diagrams/style.md` (visual language; it maps a `design.md` at the repository root onto the theme when there is one).
2. Animation or video: also read `references/animation/index.md`, then `pipeline.md`, `motion.md`, `formats.md` as needed. The engine is in `assets/animation/` (needs Node 22, Playwright Chromium and ffmpeg: ask before installing any of them).
3. Check the picture at its smallest display size before reporting it done. If text cannot be read there, cut text.

Defaults: `## Tabby` or `## Python defaults` in AGENTS.md. Ask only what is still unknown.
