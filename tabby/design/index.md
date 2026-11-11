# Design: diagrams, explainer animations and interfaces

Say one thing per picture. Delete a node or a line when the picture still works without it. Write the first valid file early, then check and look.

- **A diagram:** read `design/diagrams/quickstart.md` and follow it.
- **An animation:** read `design/animation/quickstart.md` and follow it.
- **A screen, template, dashboard, docs site or README visual:** read `design/interfaces/index.md`.
- **Deeper, only when a check finding or an unusual request needs it:** `design/diagrams/style.md` (look, tokens, `design.md` mapping), `connectors.md`, `icons.md`, `types/`, `design/animation/motion.md`, `pipeline.md`, `formats.md` (video, only if asked).

Needs: Node 22 for the builders; Playwright Chromium to render and to check motion or interfaces; ffmpeg only for video. Ask before installing any of them; if one is missing, say what was not checked.

Defaults: `## Tabby` or `## Python defaults` in AGENTS.md. Ask only what is still unknown.
