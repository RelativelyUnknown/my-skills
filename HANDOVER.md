# Handover

State of the repository for whoever continues it, as of 11 November 2026. The work is on PR #4 (branch `claude/design-patterns-and-code-snags`, open, not merged). This handover is PR #5, stacked on PR #4: it changes only this file. If #4 merges first, retarget #5 to `main`. `AUDIT.md` holds the audit, the final measurement and the per-case table; this file is how to carry on.

## What this is

Tabby: one registered Claude skill (`tabby/SKILL.md`) that routes to four modules, for AI coding agents working on Python projects, with Rust, C, C++ and Zig as native-extension languages. The agent works as a senior engineer would: it knows the platform and the project, works out what the user is after, thinks past the ask while keeping options open, reuses before it writes, and uses the project's own toolstack. Install: `/plugin marketplace add RelativelyUnknown/my-skills`, `/plugin install tabby@tabby`. Manifests are in `.claude-plugin/`; the interview command is `commands/interview.md` (`/tabby:interview`).

## Layout

| Path | Role |
| --- | --- |
| `tabby/SKILL.md` | The router (about 4 KB). Infers kind and stack, says them in one line, loads the modules a task needs, offers the interview once. `description:` must stay at or under 300 characters (now 293) and its opening words decide whether the router loads at all. |
| `tabby/references/` | `start.md` (the interview, run only on request), `research.md` (read-only research feeding it), `growth.md` (options and seams: read the evidence, name options per fork, build the seam not the feature, say it once). |
| `tabby/development/` | The front door `index.md` (the senior method, never-miss rules, a universal reading list); areas `code/`, `testing/`, `architecture/`, `workflow/`, `dependencies/`, `performance/` are universal; `library/` (shared, native), `application/` (apis, shared, workers) are read through the project's kind index only. `ecosystem.md` lists what exists by job; `code/reuse.md` is the ladder; `which-type.md` names the kind and the tool stack; `assets/` holds the templates (`native/` for Cargo lints and nanobind). |
| `tabby/review/` | Diff review, whole-repo audit, security audit (code, and dependencies, CI and release), native boundary review. |
| `tabby/documentation/` | Diátaxis page types, ADR, runbook, troubleshooting, changelog, commit messages, docs drift, style. |
| `tabby/design/` | Choosing and checking a diagram; `diagrams/style.md` is the one token set (light and dark) for static diagrams and the animation engine, and the design.md mapping; `assets/animation/` is the render engine. |
| `tabby/evals/` | 84 cases plus `tabby.triggers.json` (30 should-trigger, 30 should-not). |
| `AUDIT.md`, `THIRD_PARTY_NOTICES.md`, `tabby/development/SOURCE.md` | The audit and results; what was read from other repositories and what was taken; what was adapted from wshobson/agents. |

Sizes (11 November): 83 Markdown files under `development/`, 8 under `review/`, 26 under `documentation/`, 9 under `design/` (plus the engine); front door 5.8 KB.

Project memory is the `## Tabby` section of the user's AGENTS.md: `reviewed:`, `purpose:`, `users:`, `goals:`, `growth:`, `workload:`, `out-of-scope:`, `constraints:`, `always:`, `ask-first:`, `never:`, `kind:`, `modules:`, `docs:`, `commands:`, `map:`, `conventions:`, `gotchas:`, `open:` (the template is in `tabby/references/start.md`). Tool and style defaults are the separate `## Python defaults` section (`python`, `runner`, `build`, `test`, `lint`, `ci`, `types`, `rigor`, `report`, `docstrings`); `kind:` is only in `## Tabby`. The router reads the section before a task when it exists.

## Decisions that hold

- **Do the task; interview only on request.** With no saved section the router infers scope and stack from the request and the repo, labels guesses `(assumed)`, and offers `/tabby:interview` once at the end. It asks a question first only when a wrong guess is expensive or the request cannot be stated as one change (then one to three questions with suggested answers). Once the interview is invoked: nothing is written to memory before an explicit yes to the restated summary, at most three questions per round.
- **The project's tools win.** Detect the runner, build backend, test framework, formatter, type checker and check command from the repo (`development/which-type.md`); poetry stays poetry, black stays black, unittest stays unittest. The uv-based templates in `development/assets/` are for projects that have not chosen. Never swap a tool, never add a second for a job one does.
- **The reuse ladder is not "stdlib first".** The project's own tool, then the standard library, then the community's standard library (httpx or requests, pydantic, pytest, SQLAlchemy; serde and tokio in Rust), then niche libraries or your own code. The burden of proof is on the last rung. A new dependency is named in the reply with its rung and reason, and needs a yes first only when `ask-first:` says so.
- **Think past the ask, keep options open.** For a request that adds a layer (an API, a queue, a cache, auth, an ORM, async), `references/growth.md`: read the evidence, name options per real fork, choose what fits today, build the seam, say it once; stop and ask first only when the choice binds data or a public contract.
- **"Get rid of" a public name is a deprecation** unless nothing outside the repository can use it. Additive changes to public names also need approval (`ask-first: public API change`).
- **Kind-specific content is reached through the kind index only.** The front door lists universal leaves; library, service, worker and native pages are read by the project's kind. Nothing was deleted when this was done; deletions need evidence of no lift.
- **One token set for pictures.** `design/diagrams/style.md` is the only place colours and fonts are defined; the engine's defaults match it exactly in light, and derive the dark set and the accent tints from `SURFACE`, `INK`, `ACCENT` and `BASE`. design.md is applied for colours and fonts; stage size and motion are listed as not applied, and the agent says so.
- **Smells are split by area** (`code`, `library`, `testing`, `native`, `application`), each its own `smells.md`.
- **Content leads with the principle.** A file opens with the question to ask or the decision rule; long examples live in a sibling `*-examples.md`.
- **Every technical claim is grounded in real source** (cloned and read, or run), not recalled. Rows that were run say so with the version; anything not run is labelled.
- **Prefer Rust for new native code.** `library/native/zig.md` covers Zig only for projects already using it; `cpp.md` covers C++ (nanobind for new bindings, pybind11 where it exists); `porting.md` covers moving a Python function native.
- **A grader that matches Tabby's own vocabulary is `arm: with-only`**: reported, not scored, so a lift is never credited for wording the bare agent cannot know. Cases tagged `protocol` test behaviour Tabby defines; report them apart from outcome cases.
- **Do not detect overly verbose wording with grep.** It is flaky; do not suggest it.
- **Never copy an example from another project into the skill.** Check where an example came from before keeping it (see Open).

## Evals

A case is `case.yaml`, `prompt.md`, `fixture.sh`, `graders/*.md`; `fixture.sh` builds the repository the agent works in. Run from the repository root:

`claude plugin eval tabby --case <name> --runs 3 --ablation with-without --scaffold --allow-tools Write Edit Bash WebFetch --model claude-haiku-5-5 --judge-model haiku -j 8 --max-cost-usd 10 --trust-plugin --no-publish --json <path> --output-dir <path>`

- Granting `Bash` needs `bubblewrap` and `socat` (`apt-get update && apt-get install -y bubblewrap socat`); without them graders that need a `Bash` call fail in both arms. `--case` takes a glob, not braces; run several cases in parallel with `xargs -P`.
- **Do not edit anything under `tabby/` while an eval runs:** the plugin directory is read live, so the run would measure a mixture.
- **Usage limit.** A full run (84 cases, 3 runs, both arms) costs about $8 and ran into the account's 5-hour limit once. Runs that hit it end with `exit 1: You've hit your 5-hour limit` and score 0 without grading. After a run, count `error` fields in the JSON, and re-run only the cut-off cases (the cost cap is per invocation).
- **Traces** (`tracePath` in the JSON) are deleted after the run unless you pass `--keep-temp`. Use it to find out why a run scored low; the final message and the tool sequence are in `trace.jsonl`.
- **Score** is the weighted pass rate of the scored graders; `withOnly` graders are not scored. A grader that points at a file the agent did not create counts as failed ("grader threw"), so a run that never wrote the file scores 0. With three runs, a difference under about 0.15 on one case is noise.
- Inside the eval sandbox the working directory can be read-only for `Bash` while the `Write` tool still works; some runs of file-creating cases fail because the agent gave up after `mkdir` failed.
- Pitfalls writing cases: a prompt's quoted code must match the fixture exactly; an `ask-first:` line in a fixture can block the task in both arms (grant permission in the prompt, do not weaken the fixture); write prompts as a task and a symptom, never prescribe the solution; keep scored graders free of Tabby vocabulary.
- Tags: `development`, `review`, `documentation`, `design` (module); `protocol`, `guard` (the right result is to do little), `baseline` (the bare agent passes), `senior`, `options`, `ladder`, `toolstack`.

### Checks before committing

Run from the repository root; all three must be clean.

1. `claude plugin validate .` (an `ICON_MISSING` warning is expected).
2. The router description length: `python3 -c "import re;print(len(re.search(r'description: \"(.*)\"',open('tabby/SKILL.md').read()).group(1)))"` (at most 300).
3. Relative links resolve and every content file is named by an index:

```python
import pathlib, re
FENCE = chr(96) * 3          # a code fence, built so this block can contain it
root = pathlib.Path('.'); bad = 0
mds = [p for p in root.rglob('*.md') if '.git/' not in str(p) and 'node_modules' not in str(p)]
for p in mds:
    t = re.sub(FENCE + '.*?' + FENCE, '', p.read_text(), flags=re.S)
    for m in re.finditer(r'\]\(([^)#\s]+)(#[^)]*)?\)', t):
        u = m.group(1)
        if not re.match(r'[a-z]+:', u) and not (p.parent / u).exists(): print('BROKEN', p, u); bad += 1
tab = [p for p in mds if str(p).startswith('tabby/') and '/evals/' not in str(p)]
texts = {p: p.read_text() for p in tab}
for p in tab:
    if p.name not in ('README.md', 'SKILL.md', 'index.md', 'SOURCE.md') and not any(p.name in t for q, t in texts.items() if q != p): print('UNREFERENCED', p)
print('broken', bad)
```

## Open

- **Results (10 November, 84 cases, 3 runs per arm): 0.85 with Tabby, 0.76 without; +19% cost and +50% turns per run.** The efficiency targets (cost at most +15%, turns at most +35%) were missed. 26 cases improve by 0.10 or more, 51 tie, 7 get worse. `AUDIT.md` has the table.
- **The senior-engineer methods have no measured benefit yet** (footprint of a similar change, scouting, the learned-note, options and seams on the API example); the reuse ladder, deprecation and the toolstack rules do show lift. Next step: run `scout-reports-what-it-noticed` and `api-on-plain-sql-growth-known` with `--keep-temp` and read the traces to see whether the instructions are ignored or the model already does it.
- **Cost.** Tabby adds 22% on the 51 cases where it changes nothing. Not tried: shortening `development/index.md`, dropping the `workflow/shipping.md` read, making `Noticed:` optional for tiny changes, a lighter router for one-line fixes.
- **The router decides everything.** Rewording the description once cut loading from 114 to 49 of 180 runs; it loads in 76% of runs now, and never on review, audit and documentation requests, so Tabby's effect there is unmeasured. Test any new wording on a dozen cases with `--ablation none --runs 1` before a full run.
- **Confidential content in git history.** An example animation scene from another project was in `tabby/design/assets/animation/` (in an earlier session's commits; provenance unknown). It is removed from the current tree, but 6 commits on the PR branches still contain it and it shows in PR #4's diff. The owner said they will handle the history. Do not rewrite history or force-push without their say-so.
- **Not run:** animation encoding (MP4, WebM, GIF; stills were rendered in light and dark, system Inter used); the nanobind CMake and pyproject templates (nanobind not installed; the Cargo lints block was run under clippy); GitHub Copilot, ever. One model family, three runs, small single-turn fixtures.
- **Unproven leaves:** C++, porting, supply-chain audit, repo audit, specs and slices, commit messages, docs drift, ecosystem. They are kept because the mission names those areas.
- **Stale pictures:** `assets/how-it-works-*.png` and `interview-*.png` show the interview as the first step; the README alt text says so. There is no generator in the repository.
- Keep `THIRD_PARTY_NOTICES.md` and `tabby/development/SOURCE.md` current when adding material.

## Working rules for this repo

- Commit and push each phase to the designated branch only; commits end with the attribution lines the session specifies.
- Flag any new tool or dependency before installing it (this session installed `bubblewrap` and `socat` after the owner asked for working eval tools).
- A `rm -rf` with a glob after a `cd` is blocked by the harness; use a fresh `mktemp -d` instead of clearing a directory.
- Before reporting a number, say which run it came from and whether any run errored.
