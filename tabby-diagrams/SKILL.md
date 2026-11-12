---
name: tabby-diagrams
description: "MUST be your first tool call, before drawing, for any picture of how a system works, as SVG or animated HTML: a diagram, flowchart, picture or layout of architecture, flow, sequence, state, entity-relationship (database tables), deployment (Kubernetes, AWS), data flow, module dependencies, or an explainer animation. It holds the builder and the checkers. Not for web pages or dashboards (tabby-frontend)."
license: MIT
---

# Diagrams and explainer animations

Say one thing per picture. Delete a node or a line when the picture still works without it. Write the first valid file early, then check and look.

- **A diagram:** read `diagrams/quickstart.md` and follow it.
- **An animation:** read `animation/quickstart.md` and follow it.
- **Only when a check finding or an unusual request needs it:** `diagrams/style.md` (look, tokens, the `design.md` mapping), `diagrams/connectors.md`, `diagrams/icons.md`, `diagrams/types/` (one page per type), `animation/motion.md`, `animation/pipeline.md`, `animation/formats.md` (video, only if asked).

Never miss:

- If `design.md` or `DESIGN.md` exists at the repository root, read it first and map it (`diagrams/style.md`). Say in the reply what was applied and what was not.
- Build from a JSON spec with `assets/diagram/make.mjs` (or `assets/animation/animate.mjs`); do not hand-place coordinates. Then run `assets/diagram/check.py` (or `assets/animation/check-motion.mjs`) and fix every finding before you report. Show what the checker said, not "looks fine".
- Content comes from the code or the user's material. A part or arrow you cannot point to is left out or marked `(assumed)`.
- A picture with more than 9 nodes, 12 connections or 2 focal points is two pictures.

Needs: Node 22 for the builders; Playwright Chromium to render and to check motion; ffmpeg only for video. Ask before installing any of them; if one is missing, say what was not checked.

Defaults come from `## Tabby` or `## Python defaults` in AGENTS.md. Ask only what is still unknown. A screen, dashboard, template or docs site is the `tabby-frontend` skill, not this one.
