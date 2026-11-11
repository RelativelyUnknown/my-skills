---
name: tabby-frontend
description: "Use when building or changing what a user sees in a browser: a server-rendered page or template (Jinja, Django), a dashboard or admin screen, a Streamlit, Dash or Gradio app, a docs site, or a README visual. Not for diagrams or animations."
license: MIT
---

# Interfaces

Read `interfaces/index.md` and follow it. It covers the method (context, a five-line brief, the mode, build with the project's own tools, tokens, refuse list, check and look) and links one page per surface: `interfaces/server-rendered.md`, `interfaces/data-apps.md`, `interfaces/docs-and-readme.md`, plus `interfaces/layout-and-states.md`, `interfaces/tokens-and-type.md` and `interfaces/refuse.md` for the details.

Never miss:

- Read `design.md` (or `DESIGN.md`) and the project's existing pages, CSS framework and theme config first, and match them. A redesign only when it is asked.
- Build with the tools the project already has (Tailwind, Bootstrap, Pico, Streamlit theme, MkDocs Material). Do not add a second styling system.
- Content that exists: no invented figures, names or logos.
- Check by measuring: `node assets/interfaces/ui-check.mjs <url or file>` (Playwright Chromium; ask before installing), then look at the page at 390 px and 1280 px, in light and dark, with the keyboard. A finding is fixed or waived with a reason in `.tabby-ui-waivers.json`. Say what was measured, what you looked at and what you did not check.

A diagram or an explainer animation is the `tabby-diagrams` skill, not this one. Defaults come from `## Tabby` or `## Python defaults` in AGENTS.md.
