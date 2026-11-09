---
name: tabby
description: "Rules for every Python code change: errors, minimalism, stdlib first, typing, tests, dependencies, CI, packaging, performance, docs, reviews. Use whenever you write, change, debug, test, review, package or document Python, or start or join a project; load before editing any .py or pyproject.toml."
license: MIT
---

# Tabby: project memory and router

Project memory is the `## Tabby` section of AGENTS.md. Claude Code reads CLAUDE.md, not AGENTS.md: if the repo has no CLAUDE.md, suggest one line, `@AGENTS.md`.

## Modules

Each is a folder in this skill's folder; open its `index.md` with Read first. File paths in a module's `index.md` start with the module name, for example `engineering/references/...`, relative to this skill's folder.

| Module | Read when |
| --- | --- |
| `engineering/` | writing, changing, debugging, testing, speeding up, packaging or releasing code; services, workers, libraries, Rust or C behind Python |
| `review/` | reviewing a diff, a security audit, or before reporting your own change as done |
| `documentation/` | a README, docstring, tutorial, how-to, reference, changelog, ADR, runbook, troubleshooting page, CONTRIBUTING |
| `design/` | a diagram, an architecture picture, an explainer animation |

## Section exists

1. Read it. Load the modules in `modules:` that the task needs, and follow `kind:`.
2. Respect `out-of-scope:`. If the task contradicts `goals:` or `out-of-scope:`, or `reviewed:` is over six months old, ask whether the section still fits, then update it.
3. A task that makes a `growth:` item real (a first Rust module, a first public API, a first endpoint): read `references/growth.md` before designing it.

## Section missing

Read `references/start.md` and run it. For a small fix, do the work with `engineering/index.md` and offer the interview afterwards. Starting fresh and joining a project use the same interview; joining starts with what the repo already shows.

## Never

- Ask what the repo or the request already answers. Label inferred facts `(inferred)`.
- Ask more than three questions in a round.
- Build for growth the user did not state, or skip building for growth they did.
- Write the section before the user says yes to the restated summary.
