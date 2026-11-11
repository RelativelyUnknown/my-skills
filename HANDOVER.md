# Handover

State of the repository for whoever continues it, as of 11 November 2026 (evening). PRs #4 and #5 are merged. The design redesign, the interfaces area, the design review and the completion gates are on branch `ccr-fafc7af6-jyh8oc`, pushed, with no PR opened. `AUDIT.md` holds the audits, the measurements (section 4 is the 11 November run, which was cut off by the usage limit) and the per-case table; this file is how to carry on.

## What this is

Tabby: one registered Claude skill (`tabby/SKILL.md`) that routes to four modules, for AI coding agents working on Python projects, with Rust, C, C++ and Zig as native-extension languages. The agent works as a senior engineer would: it knows the platform and the project, works out what the user is after, thinks past the ask while keeping options open, reuses before it writes, and uses the project's own toolstack. Install: `/plugin marketplace add RelativelyUnknown/my-skills`, `/plugin install tabby@tabby`. Manifests are in `.claude-plugin/`; the interview command is `commands/interview.md` (`/tabby:interview`).

## Layout

| Path | Role |
| --- | --- |
| `tabby/SKILL.md` | The router (about 4 KB). Infers kind and stack, says them in one line, loads the modules a task needs, offers the interview once. `description:` must stay at or under 300 characters (now 293) and its opening words decide whether the router loads at all. |
| `tabby/references/` | `start.md` (the interview, run only on request), `research.md` (read-only research feeding it), `growth.md` (options and seams: read the evidence, name options per fork, build the seam not the feature, say it once). |
| `tabby/development/` | The front door `index.md` (the senior method, never-miss rules, a universal reading list); areas `code/`, `testing/`, `architecture/`, `workflow/` (now with `gates.md`: checks written before a multi-part change), `dependencies/`, `performance/` are universal; `library/` (shared, native), `application/` (apis, shared, workers) are read through the project's kind index only. `ecosystem.md` lists what exists by job; `code/reuse.md` is the ladder; `which-type.md` names the kind and the tool stack; `assets/` holds the templates (`native/` for Cargo lints and nanobind). |
| `tabby/review/` | Diff review, whole-repo audit, security audit (code, and dependencies, CI and release), native boundary review, and `design.md`: a judgment pass and a measured pass over a diagram, animation or interface, kept apart. |
| `tabby/documentation/` | Diátaxis page types, ADR, runbook, troubleshooting, changelog, commit messages, docs drift, style. |
| `tabby/design/` | One quiet look for pictures and screens. `diagrams/` (`quickstart.md` first, then `choosing.md`, `style.md` tokens and the `design.md` mapping, `connectors.md`, `icons.md`, `types/` one page per type); `animation/` (`quickstart.md`, `motion.md` thesis and step vocabulary, `pipeline.md`, `formats.md` for video on request); `interfaces/` (method, tokens, layout and states, `refuse.md`, server-rendered, data apps, docs and README). `assets/diagram/` is the builder `make.mjs` (spec to SVG: grid, icons, routes `h v hv vh z below above`, theme from a design.md), `check.py`, `render.mjs`, `selftest.py`, `examples/`; `assets/animation/` is `animate.mjs` (spec plus a story to one HTML file), `check-motion.mjs`, `render-video.mjs`, `selftest-motion.mjs`, `templates/`; `assets/interfaces/` is `ui-check.mjs`, `selftest-ui.mjs`, `fixtures/`; `assets/icons/` is the vendored Tabler set (`tabler-outline.json`, MIT, `build-icons.mjs` regenerates it). `SOURCE.md` says what came from where. |
| `tabby/evals/` | 91 cases (seven added on 11 November: state-machine diagram, animated HTML, UI accessibility fix, docs-site theme, page review, multi-part gates, trivial gates) plus `tabby.triggers.json` (38 should-trigger, 33 should-not). |
| `AUDIT.md`, `THIRD_PARTY_NOTICES.md`, `tabby/development/SOURCE.md` | The audit and results; what was read from other repositories and what was taken; what was adapted from wshobson/agents. |

Sizes (11 November): the plugin folder is about 6.2 MB (1.2 MB of it the icon JSON); front door 5.9 KB; router 4.1 KB.

Project memory is the `## Tabby` section of the user's AGENTS.md: `reviewed:`, `purpose:`, `users:`, `goals:`, `growth:`, `workload:`, `out-of-scope:`, `constraints:`, `always:`, `ask-first:`, `never:`, `kind:`, `modules:`, `docs:`, `commands:`, `map:`, `conventions:`, `gotchas:`, `open:` (the template is in `tabby/references/start.md`). Tool and style defaults are the separate `## Python defaults` section (`python`, `runner`, `build`, `test`, `lint`, `ci`, `types`, `rigor`, `report`, `docstrings`); `kind:` is only in `## Tabby`. The router reads the section before a task when it exists.

## Decisions that hold

- **Do the task; interview only on request.** With no saved section the router infers scope and stack from the request and the repo, labels guesses `(assumed)`, and offers `/tabby:interview` once at the end. It asks a question first only when a wrong guess is expensive or the request cannot be stated as one change (then one to three questions with suggested answers). Once the interview is invoked: nothing is written to memory before an explicit yes to the restated summary, at most three questions per round.
- **The project's tools win.** Detect the runner, build backend, test framework, formatter, type checker and check command from the repo (`development/which-type.md`); poetry stays poetry, black stays black, unittest stays unittest. The uv-based templates in `development/assets/` are for projects that have not chosen. Never swap a tool, never add a second for a job one does.
- **The reuse ladder is not "stdlib first".** The project's own tool, then the standard library, then the community's standard library (httpx or requests, pydantic, pytest, SQLAlchemy; serde and tokio in Rust), then niche libraries or your own code. The burden of proof is on the last rung. A new dependency is named in the reply with its rung and reason, and needs a yes first only when `ask-first:` says so.
- **Think past the ask, keep options open.** For a request that adds a layer (an API, a queue, a cache, auth, an ORM, async), `references/growth.md`: read the evidence, name options per real fork, choose what fits today, build the seam, say it once; stop and ask first only when the choice binds data or a public contract.
- **"Get rid of" a public name is a deprecation** unless nothing outside the repository can use it. Additive changes to public names also need approval (`ask-first: public API change`).
- **Kind-specific content is reached through the kind index only.** The front door lists universal leaves; library, service, worker and native pages are read by the project's kind. Nothing was deleted when this was done; deletions need evidence of no lift.
- **One look for pictures and screens.** `design/diagrams/style.md` is the only place colours and fonts are defined (art direction "quiet tonal": white ground, soft zones, tonal role fills, icon tiles, one accent, depth from tone; light and dark). A `design.md` maps onto the spec's `theme` (accent, surface, ink, font); the builder derives the rest and `check.py` reports any contrast pair that fails. Stage size and motion are not applied, and the agent says so.
- **Build from a spec, then check, then look.** A diagram or animation is a JSON spec run through `make.mjs` or `animate.mjs`, not hand-placed coordinates. Every checker has a self-test that mutates a clean example with seeded defects and requires each to be caught (`selftest.py`, `selftest-motion.mjs`, `selftest-ui.mjs`); run them after changing a checker, a builder or a token. A checker finding is fixed in the spec; a finding judged false is waived with a reason, never silently.
- **Animation is a self-contained HTML file by default**, a pure function of time with the complete picture as the base and the end state under `prefers-reduced-motion`; every step needs a `why`; at most 8 steps and 2 at once. Video (MP4, WebM, GIF) is rendered from it by seeking, on request. The old chart-comparison engine was removed on 11 November (it is in git history before `80dab2a`).
- **Completion gates are automatic for multi-part coding requests** (three or more independent outcomes, "all"/"every", a task that came back half done), never for one-line fixes. A short list of checks from the project's own commands, written first, run again before reporting; no script, no hook.
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
- **Usage limit: check it before a full run.** A full run (91 cases, 3 runs, both arms) costs roughly $4 to $9. On 11 November it hit the account's **weekly** limit (`exit 1: You've hit your weekly limit · resets Nov 15, 5pm (UTC)`) after about 45 cases; the remaining 252 runs scored 0 without grading. A cap with `--max-cost-usd` does not stop this. Run a few cases at a time, count `error` fields in each result as they land, and stop at the first limit error; re-run only the cut-off cases afterwards. Router tests and case development spend the same quota.
- **Running cases in parallel:** `xargs -P 4 -I{} claude plugin eval tabby --case {} --runs 3 --ablation with-without --scaffold --allow-tools Write Edit Bash WebFetch --model claude-haiku-5-5 --judge-model haiku -j 2 --trust-plugin --no-publish --json <dir>/{}.json --output-dir <dir>/{}` (redirect stderr to a per-case file inside the command, not `2>x/{}.err`, which the shell expands once). `bubblewrap` and `socat` are installed in this container for the Bash graders.
- **Router tests need four runs per case.** Identical wording loaded the skill in 16 and then 11 of 28 runs; compare wordings with `--ablation none --runs 4` over about 14 cases and read the `skill-was-invoked` grader. `AUDIT.md` section 4 has the numbers.
- **Traces** (`tracePath` in the JSON) are deleted after the run unless you pass `--keep-temp`. Use it to find out why a run scored low; the final message and the tool sequence are in `trace.jsonl`.
- **Score** is the weighted pass rate of the scored graders; `withOnly` graders are not scored. A grader that points at a file the agent did not create counts as failed ("grader threw"), so a run that never wrote the file scores 0. With three runs, a difference under about 0.15 on one case is noise.
- Inside the eval sandbox the working directory can be read-only for `Bash` while the `Write` tool still works; some runs of file-creating cases fail because the agent gave up after `mkdir` failed.
- Pitfalls writing cases: a prompt's quoted code must match the fixture exactly; an `ask-first:` line in a fixture can block the task in both arms (grant permission in the prompt, do not weaken the fixture); write prompts as a task and a symptom, never prescribe the solution; keep scored graders free of Tabby vocabulary.
- Tags: `development`, `review`, `documentation`, `design` (module); `protocol`, `guard` (the right result is to do little), `baseline` (the bare agent passes), `senior`, `options`, `ladder`, `toolstack`.

### Checks before committing

Run from the repository root; all three must be clean.

1. `claude plugin validate .` (an `ICON_MISSING` warning is expected). Also the three self-tests: `python3 tabby/design/assets/diagram/selftest.py`, and `node tabby/design/assets/animation/selftest-motion.mjs` and `node tabby/design/assets/interfaces/selftest-ui.mjs` (these two need Playwright Chromium).
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

- **Latest measurement is incomplete (11 November).** The 10 November result (84 cases, 3 runs per arm: 0.85 with Tabby, 0.76 without; +19% cost, +50% turns) is the last complete one. The 11 November run (91 cases) was cut off by the weekly usage limit: 46 cases are valid (0.80 with, 0.73 without; turns +49%, cost +27%; on the 41 with a 10 November score the lift fell from +0.12 to +0.09), 45 cases have errored runs and must be re-run after **Nov 15, 17:00 UTC** (the list is in `AUDIT.md` section 4). Do not quote a mean over all cases from that run.
- **Three cases score worse with Tabby because of turns**: `animation-self-contained-html` (0.22 vs 0.69), `diagram-of-a-small-service` (0.67 vs 0.96) and `gates-multipart-missed-requirement` (0.61 vs 0.94). The runs used 23 to 32 turns against 7 to 18 and some never wrote the file. The quickstarts (`design/diagrams/quickstart.md`, `design/animation/quickstart.md`) and the shorter gates leaf are the fix and are unmeasured. Next step: re-run those three with `--keep-temp` and read where the first file is written. Then find out whether the lift loss on the old cases comes from the router description, the larger front door or the new modules (one change at a time, 4 runs per case).
- **The efficiency targets (cost at most +15%, turns at most +35%) are still missed** (+27% and +49% on the valid cases). `AUDIT.md` has the per-case tables.
- **The senior-engineer methods have no measured benefit yet** (footprint of a similar change, scouting, the learned-note, options and seams on the API example); the reuse ladder, deprecation and the toolstack rules do show lift. Next step: run `scout-reports-what-it-noticed` and `api-on-plain-sql-growth-known` with `--keep-temp` and read the traces to see whether the instructions are ignored or the model already does it.
- **Cost.** Tabby adds 22% on the 51 cases where it changes nothing. Not tried: shortening `development/index.md`, dropping the `workflow/shipping.md` read, making `Noticed:` optional for tiny changes, a lighter router for one-line fixes.
- **The router decides everything.** Rewording the description once cut loading from 114 to 49 of 180 runs. On 14 cases with no baseline arm the current wording loaded the skill in 59 of 112 runs against 27 of 56 for the previous one (within noise overall) and now loads for page-review, docs-site and UI requests that the old wording never matched. Code-review and audit prompts are the ones that vary most between wordings. Test any new wording at four runs per case.
- **Confidential content in git history.** An example animation scene from another project was in `tabby/design/assets/animation/` (in an earlier session's commits; provenance unknown). It is removed from the current tree, but 6 commits on the PR branches still contain it and it shows in PR #4's diff. The owner said they will handle the history. Do not rewrite history or force-push without their say-so.
- **Not run:** the nanobind CMake and pyproject templates (nanobind not installed; the Cargo lints block was run under clippy); GitHub Copilot, ever. One model family, three runs, small single-turn fixtures. Animation encoding was run on 11 November (MP4, WebM and GIF from `render-video.mjs`, system Inter) but not at full size and frame rate on a long animation.
- **Unproven leaves:** C++, porting, supply-chain audit, repo audit, specs and slices, commit messages, docs drift, ecosystem. They are kept because the mission names those areas.
- **README pictures** (`assets/how-it-works-*.png`, `assets/interview-*.png`) were regenerated on 11 November from `assets/src/*.json` with the repo's builder (`node tabby/design/assets/diagram/make.mjs assets/src/<name>.json out.svg`, then `render.mjs`, light and dark); the rebuilds are byte-identical. The crayon hero, scoreboard and cat images are unchanged and have no generator.
- Keep `THIRD_PARTY_NOTICES.md`, `tabby/development/SOURCE.md` and `tabby/design/SOURCE.md` current when adding material. Never copy an example from the shared skills; every example diagram, scene and fixture here is original.

## Working rules for this repo

- Commit and push each phase to the designated branch only; commits end with the attribution lines the session specifies.
- Flag any new tool or dependency before installing it. Installed with the owner's yes on 11 November: `bubblewrap` and `socat` (apt, container only) for the eval sandbox; Tabler icons were installed with npm in a scratch folder only to generate the vendored JSON. Playwright Chromium and ffmpeg are present in this container; the skill's own scripts must ask before installing them for a user.
- A `rm -rf` with a glob after a `cd` is blocked by the harness; use a fresh `mktemp -d` instead of clearing a directory.
- Before reporting a number, say which run it came from and whether any run errored.
