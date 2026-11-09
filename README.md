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
  <img src="https://img.shields.io/badge/skills-3-cd5c1c?style=flat-square" alt="3 skills">
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

**Today:** the front door lists exactly which file to read for each kind of task (a new function, a dependency, an error path, a CI job, a release). Project defaults live in your `AGENTS.md`.

**Planned:** an interview when a project starts or when the agent joins an existing one.

1. It reads the repo first and does not ask what it can see.
2. It asks three questions: what the project is for, where it is going, and what is out of scope.
3. It saves the answers as editable memory in `AGENTS.md`, with the list of skills that apply.
4. Later work loads only those skills, and builds in the seams your stated growth needs, such as a typed Python seam where a Rust hot path may arrive.

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

**Limits:** one model, three runs, one judge, no shell in the eval sandbox, and the skills have not been run in GitHub Copilot.

## What is in the box

Each skill is a folder you copy. A short `SKILL.md` plus `references/` that load on demand.

| Folder | What it does |
| --- | --- |
| [`python-engineering/`](python-engineering/) | Writing, testing, packaging and running Python: errors, minimalism, typing, dependencies and uv, CI, performance, libraries, services, workers, design patterns |
| [`reviewing-python-code/`](reviewing-python-code/) | Self-review of a change, and a security audit with a confirmed / needs-validation split |
| [`documentation/`](documentation/) | Documentation by reader need, ADRs, runbooks, troubleshooting, docstrings, and minimalist diagrams and explainer animations |

## Install

Copy the folders into the folder your agent reads:

```bash
# Claude Code
mkdir -p .claude/skills && cp -r python-engineering reviewing-python-code documentation .claude/skills/
# GitHub Copilot (VS Code agent mode, CLI)
mkdir -p .github/skills && cp -r python-engineering reviewing-python-code documentation .github/skills/
```

Delete each skill's `evals/` folder if you do not run evals. Any agent that reads `SKILL.md` folders and `AGENTS.md` can use them.

## Project defaults live in AGENTS.md

Skills take no arguments. They read a `## Python defaults` section of `AGENTS.md`, infer what is missing from the repo, ask only what is still unknown (once, with the agent's question tool if it has one), and save the answers there. Edit or delete a line to be asked again.

```markdown
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
- [ ] The router interview for new and existing projects
- [ ] Rust and C extensions as first-class: layouts, boundary review, build and CI
- [ ] Folding documentation into `python-engineering` and splitting design into its own skill
- [ ] Trim the front door and the largest files
- [ ] TypeScript and JavaScript, later

## Where the ideas came from

Tabby takes ideas, rewritten in its own words, from [ponytail](https://github.com/DietrichGebert/ponytail), [caveman](https://github.com/JuliusBrussee/caveman), [BeautifulRust](https://github.com/morganlinton/BeautifulRust), [Cloudflare's security-audit skill](https://github.com/cloudflare/security-audit-skill), [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), [impeccable](https://github.com/pbakaus/impeccable), [diagram-design](https://github.com/cathrynlavery/diagram-design), [stack-diagram](https://github.com/caru-ini/stack-diagram) and others. Adapted material keeps its licence; see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). The research behind the "small and focused" design is in [`HANDOVER.md`](HANDOVER.md).

## Credits and licence

MIT. The Tabby title is set in "Pizza is my FAVORITE Font" by Kimberly Geswein (freeware; commercial use requires a donation, see [fontspace](https://www.fontspace.com/pizza-is-my-favorite-font-f11293)). Only the rendered image is in this repository, not the font file.
