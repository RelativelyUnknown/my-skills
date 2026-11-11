# Interfaces

A Python project's screens: a server-rendered web app, a data app, a docs site, a README. The method is the same for each: know the visitor's job, build with the project's own tools, check by measuring and by looking.

1. **Context before looks.** Read `design.md` (or `DESIGN.md`) and `## Tabby` in AGENTS.md; look at what the project already has (its CSS framework, templates, theme config, existing pages). Match it. A redesign is only for when it is asked.
2. **Brief in five lines, then build.** Who comes; the one job they came to do; the one thing the screen must make easy; the content that really exists (never invented figures, names or logos); the limits (accessibility, devices, existing components). Write it in the reply, not in a file.
3. **Pick the mode from the visitor's job** and read [layout-and-states.md](layout-and-states.md): *persuade* (a landing page, a project site), *operate* (a dashboard, an admin screen, an internal tool), *read* (documentation, a reference).
4. **Build with the project's tools.** A project on Tailwind, Bootstrap, Pico, Streamlit's theme or MkDocs Material stays on it: set tokens through that tool's own settings, do not add a second system. Read the page for the surface: [server-rendered.md](server-rendered.md), [data-apps.md](data-apps.md), [docs-and-readme.md](docs-and-readme.md).
5. **Tokens and type** from [tokens-and-type.md](tokens-and-type.md): the same one-accent palette as the diagrams, so a project's pictures and screens match.
6. **Refuse the known defaults** in [refuse.md](refuse.md) unless the brief earns one.
7. **Check, then look.** `node assets/interfaces/ui-check.mjs <url or file>` measures what a machine can (it needs Playwright Chromium; ask before installing). A finding is fixed, or waived with a reason of at least 12 characters in `.tabby-ui-waivers.json`. Then look at the page at 390 px and at 1280 px, in light and dark, with the keyboard: the checker does not see hierarchy, fit or voice.

Say in the report what the checker measured, what you looked at, and anything not checked.
