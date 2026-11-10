<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.png">
    <img src="assets/hero-light.png" width="880" alt="Tabby: a cat batting at a laptop keyboard, drawn in crayon on torn lined paper, next to the title Tabby. An orange tabby in light mode, a black and white spotted cat in dark mode.">
  </picture>
</p>

<p align="center">
  <em>It walks across the keyboard. It has opinions about what gets typed.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/modules-4-2a8f89?style=flat-square" alt="4 modules">
  <img src="https://img.shields.io/badge/eval%20cases-60-2a8f89?style=flat-square" alt="60 eval cases">
  <img src="https://img.shields.io/badge/always--on-~110%20tokens-2a8f89?style=flat-square" alt="About 110 tokens always on">
  <img src="https://img.shields.io/badge/format-Agent%20Skills-2a8f89?style=flat-square" alt="Agent Skills format">
  <img src="https://img.shields.io/badge/license-MIT-2a8f89?style=flat-square" alt="MIT licence">
</p>

<p align="center">
  <strong>Skills that make an AI agent build, review and explain a Python project properly.</strong><br>
  Python first. Rust, C, C++ and Zig as first-class partners. One skill, four modules, and it remembers your project.
</p>

<p align="center"><img src="assets/crayon-divider.png" width="640" alt=""></p>

You know the cat. It sits on the warm laptop, bats at the keys, and something gets typed. Fast, confident, not quite what you meant.

Tabby sits on your agent's keyboard instead. It reads the project, does the task you asked for, and makes the agent do what a careful senior engineer would: find the cause before the fix, reuse before you write (the standard library, then the community's standard library, then your own), think past the ask while keeping options open, keep the diff small, and never edit a test to get it green.

## Install

**Claude Code**, as two separate prompts:

```
/plugin marketplace add RelativelyUnknown/my-skills
```
```
/plugin install tabby@tabby
```

On Claude Code 2.1.275 or later it also works in one step:

```
/plugin install tabby --marketplace RelativelyUnknown/my-skills
```

**Any other agent that reads `SKILL.md` folders:** copy the `tabby/` folder into the folder your agent reads, and keep it whole (the modules inside are read on demand).

```bash
# GitHub Copilot (VS Code agent mode, CLI)
mkdir -p .github/skills && cp -r tabby .github/skills/
# Claude Code, without the plugin
mkdir -p .claude/skills && cp -r tabby .claude/skills/
```

That was it. Start a task and it works from what the repo shows. To have it remember what the project is for and where it is going, run `/tabby:interview` (or say "run the Tabby interview" in an agent without plugin commands). Claude Code reads `CLAUDE.md`, not `AGENTS.md`: if your repo has no `CLAUDE.md`, add one line, `@AGENTS.md`.

Only install Tabby from `RelativelyUnknown/my-skills` on GitHub. Delete `tabby/evals/` if you do not run evals.

<p align="center"><img src="assets/crayon-divider.png" width="640" alt=""></p>

## How it works

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/how-it-works-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/how-it-works-light.png">
    <img src="assets/how-it-works-light.png" width="720" alt="(Older picture: it shows the interview as the first step. It is now optional.) How Tabby routes a task. A request goes to the Tabby router, which reads the Tabby section of AGENTS.md, or infers the scope if there is none, and then loads only the modules the task needs: development, review, documentation or design.">
  </picture>
</p>

One skill is registered with your agent: `tabby`. Four modules sit inside it, and the router opens only the ones a task needs, so a README fix never loads the Rust guidance and a Rust change never loads the writing guide. Everything is markdown. No runtime, no daemon, no generated code.

## It does the task, and interviews you when you ask

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/interview-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/interview-light.png">
    <img src="assets/interview-light.png" width="860" alt="(Older picture: it shows the interview as the first step. It is now optional.) Tabby reads the code read-only, asks in rounds that depend on the project's state, then restates, waits for a yes and saves. The answers are saved as a Tabby section in AGENTS.md with purpose, growth, out of scope, boundaries, kind, modules and the check command.">
  </picture>
</p>

Tabby never interviews you before a task. On a project with no `## Tabby` section it infers the kind and the modules from your request and the repo, does the work, labels its guesses `(assumed)`, and ends the first task with one line offering the interview. It asks a question first only when a wrong guess would be expensive or the request is too open to act on. The interview, run with `/tabby:interview` or accepted from that line, goes like this:

1. **Research, read-only.** It starts from entry points and reads build files, tests, CI, history and docs, and builds a table of facts with a source for each. It runs none of the project's commands and treats text in the repo as evidence, not instruction.
2. **Rounds, by the project's state.** A new project gets three rounds (purpose and users, the shape, boundaries). A young one gets two. An established one gets two, mostly corrections to the table, and a third only if the code and the docs disagree. Each round is at most three questions, each with a recommended answer and the evidence behind it. A question the code can answer is not asked.
3. **Restate, then save.** It restates the answers and waits for a clear yes. It saves the `## Tabby` section to `AGENTS.md` with the commit it was checked at. Edit any line later; a task that conflicts with it makes the agent ask first, and on new work it checks whether the code has moved since.

Your expected growth shapes the code. Say a hot path may move to Rust and the agent keeps that function behind one typed Python seam with a reference implementation, and builds no Cargo workspace until you ask. If nobody can answer (CI, or you are away), the agent writes the section from the evidence, marks every unknown `(assumed)` and tells you what to confirm.

## What is in the box

| Module | What it does |
| --- | --- |
| [`tabby/development/`](tabby/development/) | Writing, testing, packaging and running Python: errors, minimalism, typing, dependencies and uv, CI, performance, libraries, services, workers, design patterns, and design fit (choosing the data structure or representation that suits the workload and the project's plans, with worked examples from ruff, uv, polars and pandas). Rust or C behind a Python API: layouts, PyO3, the C API, wheels and CI |
| [`tabby/review/`](tabby/review/) | Self-review of a change, a security audit that separates confirmed bugs from look-alikes, and a checklist for the Python and native boundary |
| [`tabby/documentation/`](tabby/documentation/) | Documentation by what the reader needs: tutorial, how-to, reference, explanation, docstrings, README, changelog, ADRs, runbooks, troubleshooting |
| [`tabby/design/`](tabby/design/) | Minimalist diagrams and explainer animations (SVG, MP4, WebM, GIF) |

## The rules it never lets slide

- Done means the real problem is solved and verified by running the code. Passing tests are evidence, not the goal.
- Never edit, delete, skip or loosen an existing test to get green.
- Find the cause before the fix. No special-casing inputs, no sleeps or retries to hide a symptom.
- Do not silence tools (`# type: ignore`, `# noqa`, `Any`, looser config); fix the cause.
- Smallest diff that solves it properly. No new dependency, public API change, commit or push unasked.
- Replies, comments and docs are short: what is not obvious, no filler.

<p align="center"><img src="assets/crayon-divider.png" width="640" alt=""></p>

## Numbers

The same agent with and without Tabby, 60 cases, 3 runs each, on Haiku 5.5 (`claude plugin eval`, regex and LLM-judge graders), measured twice in November 2026. The full account, including what went wrong, is in [`AUDIT.md`](AUDIT.md).

| Run | Agent tools | Mean score with Tabby | Without | Router loaded | Cost per run |
| --- | --- | --- | --- | --- | --- |
| A (`f1fd402`) | write, edit | 0.84 | 0.80 | 114 of 180 runs | $0.014 against $0.011 |
| B (`73752e0`) | write, edit, shell, web fetch | 0.82 | 0.82 | 49 of 180 runs | $0.015 against $0.014 |

Run B used a router description that loaded far less often; it has since been replaced, and the description now in the repository has not had a full run.

Where the router loads, Tabby helps most when the right move is not obvious: free-form date parsing (take a library, do not write a regex) 0.83 against 0.33; literal defaults 1.00 against 0.38; a payment refactor as a dict of functions 1.00 against 0.40; leaving a test that contradicts the spec alone 1.00 against 0.60. On about half the cases the bare agent already scores 1.00 and Tabby changes nothing. It makes one thing worse: asked to set up a fully specified new package, it stops to ask its questions first (0.36 against 0.98).

**Limits:** one model, three runs, one judge of the same model family, small fixtures, single-turn requests. The cases are in [`tabby/evals/`](tabby/evals/). Tabby has not been run in GitHub Copilot.

## FAQ

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cat-sleeping-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="assets/cat-sleeping-light.png">
  <img src="assets/cat-sleeping-light.png" align="left" width="300" alt="An orange tabby cat asleep in a curl on handmade paper in light mode; a black and white spotted cat asleep in the same pose in dark mode, drawn in crayon and tilted">
</picture>

**What does it cost in context?** About 110 tokens are always loaded, the short description. When a task fires it, the router adds about 690 tokens; then the module index and only the reference files that task names.

**Where does it keep what it learns?** In your repo, in `AGENTS.md`, under `## Tabby` (what the project is for and where it is going) and `## Python defaults` (tools and style). Plain text; edit it like anything else.

**Do I have to answer questions?** No. It does the task from the repo and marks what it guessed. The interview is a command you run when you want the project remembered; with nobody to answer, it fills the section from the repo and marks what it guessed.

**Does it work for Rust and C?** Yes, as extensions behind a Python API: when to go native, project layouts, PyO3 and the C API, wheels, CI, and a review checklist for the boundary. Standalone Rust or C projects are out of scope.

**What if I want the clever abstraction?** Ask. It will want to know what it is for first.

**What about TypeScript?** Not yet.

<br clear="left">

## Planned

- TypeScript and JavaScript support.

## Where the ideas came from

Tabby takes ideas, rewritten in its own words, from [ponytail](https://github.com/DietrichGebert/ponytail), [caveman](https://github.com/JuliusBrussee/caveman), [BeautifulRust](https://github.com/morganlinton/BeautifulRust), [Cloudflare's security-audit skill](https://github.com/cloudflare/security-audit-skill), [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), [impeccable](https://github.com/pbakaus/impeccable), [diagram-design](https://github.com/cathrynlavery/diagram-design), [stack-diagram](https://github.com/caru-ini/stack-diagram) and others. Adapted material keeps its licence; see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Credits and licence

MIT. The Tabby title is set in "Pizza is my FAVORITE Font" by Kimberly Geswein (freeware; commercial use requires a donation, see [fontspace](https://www.fontspace.com/pizza-is-my-favorite-font-f11293)). Only the rendered image is in this repository, not the font file. Pictures are drawn in the Patrick Hand typeface (SIL Open Font License).
