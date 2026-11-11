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
  <img src="https://img.shields.io/badge/skills-6-2a8f89?style=flat-square" alt="6 skills">
  <img src="https://img.shields.io/badge/eval%20cases-91-2a8f89?style=flat-square" alt="91 eval cases">
  <img src="https://img.shields.io/badge/built%20for-Claude%20Code-2a8f89?style=flat-square" alt="Built for Claude Code">
  <img src="https://img.shields.io/badge/format-plugin%20of%20skills-2a8f89?style=flat-square" alt="A Claude Code plugin of skills">
  <img src="https://img.shields.io/badge/license-MIT-2a8f89?style=flat-square" alt="MIT licence">
</p>

<p align="center">
  <strong>Skills that make Claude Code build, review and explain a Python project properly.</strong><br>
  Python first. Rust, C, C++ and Zig as first-class partners. Six small skills, and it remembers your project.
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

That was it. Start a task and it works from what the repo shows. To have it remember what the project is for and where it is going, run `/tabby:interview`. Claude Code reads `CLAUDE.md`, not `AGENTS.md`: if your repo has no `CLAUDE.md`, add one line, `@AGENTS.md`.

Only install Tabby from `RelativelyUnknown/my-skills` on GitHub. The eval cases live in [`evals/`](evals/); delete the folder if you do not run evals.

<p align="center"><img src="assets/crayon-divider.png" width="640" alt=""></p>

## How it works

Six skills are registered with Claude Code. Each has its own description, and Claude loads the one that matches the task, so a README fix never loads the Rust guidance and a Rust change never loads the writing guide. A skill's body is short and names the files it keeps next to it with the moment to read each one; nothing is nested more than one level. Everything is markdown, plus small Node and Python scripts that build and check diagrams and pages. No daemon.

| Skill | Claude loads it when you | What is in it |
| --- | --- | --- |
| [`tabby`](tabby/) | write, fix, test, speed up, package or release Python, or the Rust, C, C++ or Zig behind it | The rules it never lets slide, then on-demand leaves for errors, minimalism, typing, dependencies and uv, CI, performance, libraries, services, design patterns and design fit; native layouts, PyO3, the C API, wheels |
| [`tabby-review`](tabby-review/) | ask for a review of a diff, branch or pull request, a repository audit or a security audit | Self-review, a security audit that separates confirmed bugs from look-alikes, the Python and native boundary checklist, a design review that keeps judgment and measurement apart |
| [`tabby-docs`](tabby-docs/) | write a README, docstrings, a tutorial, a changelog, an ADR or a runbook | Documentation by what the reader needs, and a drift check against the code |
| [`tabby-diagrams`](tabby-diagrams/) | ask for a diagram, an architecture picture or an explainer animation | A builder that turns a small spec into an SVG or an animated HTML file in one quiet look (white ground, one accent, light and dark), a vendored Tabler icon set, and checkers for a crowded label, a missing title, low contrast and a jump at the loop boundary |
| [`tabby-frontend`](tabby-frontend/) | build a page, template, dashboard, data app, docs site or README visual | A method, tokens, a list of things it refuses to ship, and `ui-check` for contrast, focus, motion and layout |
| [`interview`](interview/) | run `/tabby:interview` | Researches the repo read-only, asks at most three questions a round, saves a `## Tabby` section to `AGENTS.md` |

## It does the task, and interviews you when you ask

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/interview-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/interview-light.png">
    <img src="assets/interview-light.png" width="860" alt="The interview is optional. Tabby does the task first and makes one offer at the end. Only if you ask for the interview, and say yes to its summary, does it save a Tabby section to AGENTS.md.">
  </picture>
</p>

Tabby never interviews you before a task. On a project with no `## Tabby` section it infers the kind of project from your request and the repo, does the work, labels its guesses `(assumed)`, and ends the first task with one line offering the interview. It asks a question first only when a wrong guess would be expensive or the request is too open to act on. The interview, run with `/tabby:interview` or accepted from that line, goes like this:

1. **Research, read-only.** It starts from entry points and reads build files, tests, CI, history and docs, and builds a table of facts with a source for each. It runs none of the project's commands and treats text in the repo as evidence, not instruction.
2. **Rounds, by the project's state.** A new project gets three rounds (purpose and users, the shape, boundaries). A young one gets two. An established one gets two, mostly corrections to the table, and a third only if the code and the docs disagree. Each round is at most three questions, each with a recommended answer and the evidence behind it. A question the code can answer is not asked.
3. **Restate, then save.** It restates the answers and waits for a clear yes. It saves the `## Tabby` section to `AGENTS.md` with the commit it was checked at. Edit any line later; a task that conflicts with it makes the agent ask first, and on new work it checks whether the code has moved since.

Your expected growth shapes the code. Say a hot path may move to Rust and the agent keeps that function behind one typed Python seam with a reference implementation, and builds no Cargo workspace until you ask. If nobody can answer (CI, or you are away), the agent writes the section from the evidence, marks every unknown `(assumed)` and tells you what to confirm.

## The rules it never lets slide

- Done means the real problem is solved and verified by running the code. Passing tests are evidence, not the goal.
- Never edit, delete, skip or loosen an existing test to get green.
- Find the cause before the fix. No special-casing inputs, no sleeps or retries to hide a symptom.
- Do not silence tools (`# type: ignore`, `# noqa`, `Any`, looser config); fix the cause.
- Smallest diff that solves it properly. No new dependency, public API change, commit or push unasked.
- Replies, comments and docs are short: what is not obvious, no filler.

<p align="center"><img src="assets/crayon-divider.png" width="640" alt=""></p>

## Numbers

The same agent with and without Tabby on Haiku 5.5 (`claude plugin eval`, regex and LLM-judge graders), 91 cases, 3 runs each, measured on 11 and 12 November 2026. The full account, with the cases where Tabby does not help, is in [`AUDIT.md`](AUDIT.md).

| | Score | Turns per run | Cost per run |
| --- | --- | --- | --- |
| Without Tabby | 0.754 | 11.1 | $0.0120 |
| Tabby as one skill (before the split) | 0.812 | 16.2 | $0.0149 |
| Tabby as six skills | 0.840 | 17.1 | $0.0153 |

It helps most when the right move is not obvious and a habit decides it: deprecate a public name instead of deleting it, take the ecosystem's standard library instead of hand-rolling one, ask before overriding a saved project rule, find that a longer timeout is not the fix, take a library for a hard problem, ask briefly when a request is vague. On many cases the bare agent already does as well, and there Tabby only adds cost. It is not cheaper: about 27% more per run and half again as many turns. A skill only helps when Claude loads it; on phrasings it had not seen, the descriptions loaded their skill about a third of the time on Haiku, which is the next thing to improve.

**Limits:** one model family, three runs, one judge of the same family, small single-turn fixtures written next to the skills, no held-out set yet. The senior-engineer methods (footprint of a similar change, scouting, options and seams) did not show a measured benefit. The cases are in [`evals/`](evals/); the runner and the tables are in [`tools/eval/`](tools/eval/).

## FAQ

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/cat-sleeping-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="assets/cat-sleeping-light.png">
  <img src="assets/cat-sleeping-light.png" align="left" width="300" alt="An orange tabby cat asleep in a curl on handmade paper in light mode; a black and white spotted cat asleep in the same pose in dark mode, drawn in crayon and tilted">
</picture>

**What does it cost in context?** Claude Code keeps the six descriptions in context (about 400 tokens in all). When a task matches one, that skill's body is added, and only the leaf files it names for that task.

**Where does it keep what it learns?** In your repo, in `AGENTS.md`, under `## Tabby` (what the project is for and where it is going) and `## Python defaults` (tools and style). Plain text; edit it like anything else.

**Do I have to answer questions?** No. It does the task from the repo and marks what it guessed. The interview is a command you run when you want the project remembered; with nobody to answer, it fills the section from the repo and marks what it guessed.

**Does it work for Rust and C?** Yes, as extensions behind a Python API: when to go native, project layouts, PyO3 and the C API, wheels, CI, and a review checklist for the boundary (in `tabby-review`). Standalone Rust or C projects are out of scope.

**What if I want the clever abstraction?** Ask. It will want to know what it is for first.

**What about TypeScript?** Not yet.

<br clear="left">

## Planned

- TypeScript and JavaScript support.

## Where the ideas came from

Tabby takes ideas, rewritten in its own words, from [ponytail](https://github.com/DietrichGebert/ponytail), [caveman](https://github.com/JuliusBrussee/caveman), [BeautifulRust](https://github.com/morganlinton/BeautifulRust), [Cloudflare's security-audit skill](https://github.com/cloudflare/security-audit-skill), [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), [impeccable](https://github.com/pbakaus/impeccable), [taste-skill](https://github.com/Leonxlnx/taste-skill), [unlazy](https://github.com/Leonxlnx/unlazy), [diagram-design](https://github.com/cathrynlavery/diagram-design), [stack-diagram](https://github.com/caru-ini/stack-diagram) and others. The diagram icons are [Tabler Icons](https://github.com/tabler/tabler-icons) (MIT). Adapted material keeps its licence; see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

## Credits and licence

MIT. The Tabby title is set in "Pizza is my FAVORITE Font" by Kimberly Geswein (freeware; commercial use requires a donation, see [fontspace](https://www.fontspace.com/pizza-is-my-favorite-font-f11293)). Only the rendered image is in this repository, not the font file. Pictures are drawn in the Patrick Hand typeface (SIL Open Font License).
