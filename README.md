<p align="center">
  <img src="assets/tabby-logo.png" width="360" alt="Tabby: an orange tabby cat batting at a laptop keyboard, drawn in crayon">
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/tabby-title-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/tabby-title-light.png">
    <img src="assets/tabby-title-light.png" width="300" alt="Tabby">
  </picture>
</p>

<p align="center">
  <strong>Skills that make an AI agent build, review and explain a project properly.<br>Opinionated. Token-lean. Python first, with Rust and C as first-class partners.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/modules-4-cd5c1c?style=flat-square" alt="4 modules">
  <img src="https://img.shields.io/badge/eval%20cases-49-cd5c1c?style=flat-square" alt="49 eval cases">
  <img src="https://img.shields.io/badge/format-Agent%20Skills-cd5c1c?style=flat-square" alt="Agent Skills format">
  <img src="https://img.shields.io/badge/license-MIT-cd5c1c?style=flat-square" alt="MIT licence">
</p>

<p align="center"><img src="assets/crayon-divider.png" width="640" alt=""></p>

## What Tabby is

An agent that writes code with no guidance writes plausible code. Tabby gives it the habits of a careful senior engineer for the whole life of a project, not just the typing part:

- **Build:** small honest diffs, standard library first, real errors, typed APIs, tests that can fail.
- **Review:** a self-review before "done", and a security audit that separates confirmed bugs from look-alikes.
- **Explain:** documentation by what the reader needs (tutorial, how-to, reference, explanation), plus ADRs, runbooks, troubleshooting tables, diagrams and short explainer animations.

Everything is markdown. There is no runtime, no daemon and no generated code. The agent reads a short front door, then only the few files its task needs.

## The router

A project is not a prompt, so Tabby does not load everything. The front door sends the agent to the files that match the task. Each file is one idea, written once.

The `tabby` skill runs when a project starts, when the agent joins an existing one, or when `AGENTS.md` has no `## Tabby` section.

1. It reads the repo first (pyproject, CI, native build files, docs) and does not ask what it can see.
2. It asks three questions in one round: what the project is and who uses it, what is likely to change, and what is off limits. More questions only if an answer changes what it would build.
3. It restates the answers in six lines and waits for a clear yes.
4. It saves a short `## Tabby` section to `AGENTS.md`: purpose, goals, growth, out of scope, constraints, the canonical check command, and the skills and reference folder that apply.
5. Later work loads only those. A growth item you named, such as a Rust hot path, gets a cheap seam now (a typed Python function with a reference implementation) and no Cargo workspace until you ask. If a task conflicts with the saved answers, the agent asks whether they still fit.

First check (Haiku 5.5, two cases in `tabby/evals/`): the router fired in 9 of 10 runs; joining a Rust-backed library it wrote a correct `## Tabby` section in 6 of 6 runs, marking unknowns as assumed; in an empty repo it asked three or fewer questions with recommended answers in 5 of 5 runs, but 4 of those 5 also asked about things the request already said. No run without the skill yet, so this shows the router works, not that it beats the bare model. The growth table is untested.

Without a `## Tabby` section the router still loads `engineering/index.md`, which lists which file to read for each kind of task (a new function, a dependency, an error path, a CI job, a release).

<p align="center"><img src="assets/crayon-divider.png" width="640" alt=""></p>

## Does it help? Measured, with the caveats

Every skill ships eval cases and is run with `claude plugin eval` (3 runs per case, regex and LLM-judge graders, one model). A skill was only built where the bare model failed first.

| Task | Without | With |
| --- | --- | --- |
| Security audit with 3 real bugs and 3 look-alikes | 0.84 | **1.00** |
| Three documentation pages (tutorial, how-to, reference) | 0.76 | **0.91** |
| ADR, runbook and troubleshooting page | 0.94 | **0.98** |

Where the bare model already did well (PyO3 API calls, a leakage-free ML split, a re-runnable data load) nothing was added. Those cases stay as baselines.

Routing against 20 flat skills installed together: score 0.788 against 0.773, and the skill fired in all 26 cases against 15 of 26. It cost about 13% more per run, so the "fewer tokens" goal is not yet met. That is the next thing to fix.

**Limits:** the numbers above predate the rework (they were measured on separate skills, before the router). One model, three runs, one judge, no shell in the eval sandbox, and Tabby has not been run in GitHub Copilot.

## What is in the box

One folder, [`tabby/`](tabby/), is the only skill your agent registers, so only its short description sits in context. Four modules live inside it, and the router loads the ones a task needs.

| Module | What it does |
| --- | --- |
| [`tabby/engineering/`](tabby/engineering/) | Writing, testing, packaging and running Python: errors, minimalism, typing, dependencies and uv, CI, performance, libraries, services, workers, design patterns, and Rust or C behind a Python API (layouts, PyO3, the C API, wheels and CI) |
| [`tabby/review/`](tabby/review/) | Self-review of a change, a security audit with a confirmed / needs-validation split, and a checklist for the Python and native boundary |
| [`tabby/documentation/`](tabby/documentation/) | Documentation by reader need: tutorial, how-to, reference, explanation, docstrings, README, changelog, ADRs, runbooks, troubleshooting |
| [`tabby/design/`](tabby/design/) | Minimalist diagrams and explainer animations (SVG, MP4, WebM, GIF) |

## Install

Copy the one folder into the folder your agent reads:

```bash
# Claude Code
mkdir -p .claude/skills && cp -r tabby .claude/skills/
# GitHub Copilot (VS Code agent mode, CLI)
mkdir -p .github/skills && cp -r tabby .github/skills/
```

Delete `tabby/evals/` if you do not run evals. Any agent that reads `SKILL.md` folders and `AGENTS.md` can use them.

## Project defaults live in AGENTS.md

Skills take no arguments. They read two sections of `AGENTS.md`: `## Tabby` (what the project is for and where it is going) and `## Python defaults` (tools and style). They infer what is missing from the repo, ask only what is still unknown (once, with the agent's question tool if it has one), and save the answers there. Edit or delete a line to be asked again.

```markdown
## Tabby
reviewed: 2026-11-09
purpose: a retry library for HTTP clients
users: backend developers
goals: stable API, no runtime dependencies
growth: a Rust hot path for backoff maths
out-of-scope: async support
kind: software-engineering/library/native
modules: engineering, review, documentation
docs: README, reference, how-to, changelog
commands: nox -e local

## Python defaults
python: 3.12
runner: uv
types: mypy
layout: src
rigor: full
report: normal
```

Claude Code reads `CLAUDE.md`, not `AGENTS.md`; if your repo has no `CLAUDE.md`, add one line, `@AGENTS.md`.

<p align="center"><img src="assets/crayon-divider.png" width="640" alt=""></p>

## Roadmap

- [x] Three routed skills with evals
- [x] Security audit and self-review
- [x] Documentation by reader need, with the history, operations, troubleshooting and governance add-ons
- [x] The router interview for new and existing projects (written, not yet measured)
- [x] Rust and C extensions: layouts, PyO3, the C API, boundary review, wheels and CI (written from sources, not yet measured)
- [x] One skill with four modules (engineering, review, documentation, design) behind the router
- [ ] Measure the router and the native leaves against baselines; keep what helps
- [ ] Trim the front door (about 1,070 tokens, aim 600) without dropping a routing pointer
- [ ] TypeScript and JavaScript, later

## Where the ideas came from

Tabby takes ideas, rewritten in its own words, from [ponytail](https://github.com/DietrichGebert/ponytail), [caveman](https://github.com/JuliusBrussee/caveman), [BeautifulRust](https://github.com/morganlinton/BeautifulRust), [Cloudflare's security-audit skill](https://github.com/cloudflare/security-audit-skill), [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), [impeccable](https://github.com/pbakaus/impeccable), [diagram-design](https://github.com/cathrynlavery/diagram-design), [stack-diagram](https://github.com/caru-ini/stack-diagram) and others. Adapted material keeps its licence; see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). The research behind the "small and focused" design is in [`HANDOVER.md`](HANDOVER.md).

## Credits and licence

MIT. The Tabby title is set in "Pizza is my FAVORITE Font" by Kimberly Geswein (freeware; commercial use requires a donation, see [fontspace](https://www.fontspace.com/pizza-is-my-favorite-font-f11293)). Only the rendered image is in this repository, not the font file.
