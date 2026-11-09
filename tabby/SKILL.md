---
name: tabby
description: "Use first when a user starts a new Python project, joins an existing one, says \"get set up\" or \"new project\", or when AGENTS.md has no `## Tabby` section. Runs a three-question interview, saves goals, growth and skills to AGENTS.md, and routes later work."
license: MIT
---

# Tabby: project memory and router

Project memory is the `## Tabby` section of AGENTS.md. Claude Code reads CLAUDE.md, not AGENTS.md: if the repo has no CLAUDE.md, suggest one line, `@AGENTS.md`.

## Section exists

1. Read it. Load the skills in `skills:` that the task needs (`python-engineering`, `python-review`, `python-design`) and follow `kind:`.
2. Respect `out-of-scope:`. If the task contradicts `goals:` or `out-of-scope:`, or `reviewed:` is over six months old, ask whether the section still fits, then update it.
3. A task that makes a `growth:` item real (a first Rust module, a first public API, a first service endpoint): read `references/growth.md` before designing it.

## Section missing

Read `references/start.md` and run it. Starting fresh and joining a project use the same interview; joining starts with what the repo already shows.

## Never

- Ask what the repo already answers. Label inferred facts `(inferred)` and let the user correct them.
- Ask more than three questions in a round. Extra rounds only for a real gap.
- Build for growth the user did not state, or skip building for growth they did.
- Write the section before the user says yes to the restated summary.
