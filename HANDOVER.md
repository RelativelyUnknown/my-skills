# Handover

State of the repository for whoever continues it, as of 12 November 2026. Work is on branch `ccr-fafc7af6-jyh8oc` with a pull request already open; do not open another. `AUDIT.md` holds the audits and every measurement (sections 4 to 7 are the recent ones); this file is how to carry on.

## What this is

Tabby: a plugin of six Claude Code skills for Python projects, with Rust, C, C++ and Zig as native-extension languages. **Built for Claude Code only.** Install: `/plugin marketplace add RelativelyUnknown/my-skills`, `/plugin install tabby@tabby`. Manifests are in `.claude-plugin/` (`plugin.json` lists the skills).

## Layout

| Path | Role |
| --- | --- |
| `tabby/` | Core skill. `SKILL.md` has the "Never miss" rules, on-demand leaf pointers, the native pointer and the project-memory rules. `development/` holds the leaves (code, testing, architecture, workflow, dependencies, performance, library incl. `native/`, application, `ecosystem.md`, `which-type.md`, `assets/` templates). `references/growth.md`: options and seams. |
| `tabby-review/` | Diff review, repo audit, security audit, native boundary review, design review (`design.md`). Calls the checkers in the diagrams and frontend skills. |
| `tabby-docs/` | Diátaxis page types, ADR, runbook, changelog, commit messages, docs drift, style. |
| `tabby-diagrams/` | Diagrams and explainer animations. `diagrams/` and `animation/` hold pages (`quickstart.md` first). `assets/diagram/` is the builder `make.mjs`, `check.py`, `render.mjs`, `selftest.py`; `assets/animation/` is `animate.mjs`, `check-motion.mjs`, `selftest-motion.mjs`; `assets/icons/` is the vendored Tabler set. `SOURCE.md` says what came from where. |
| `tabby-frontend/` | Web UI: method, tokens, `refuse.md`, server-rendered, data apps, docs and README visuals. `assets/interfaces/` is `ui-check.mjs`, `selftest-ui.mjs`, `fixtures/`. |
| `interview/` | `/tabby:interview`. A plain skill (not `disable-model-invocation`: that returned no body when run as a command). `references/start.md`, `references/research.md`. |
| `evals/` | 91 cases plus `tabby.triggers.json`, `triggers.skills.json` (88 queries with the expected skill) and `triggers.heldout.json` (25 queries written after tuning). |
| `tools/` | `eval/run.py` (batch runner, stops on the first usage-limit error, exit 3, resumable), `summarise.py` (paired tables, `--csv`, `--compare`), `traces.py`, `triggers.py` (skill-level trigger test with a confusion matrix), `variants/`, `results/*.csv`; `linkcheck.py`. |
| `AUDIT.md`, `THIRD_PARTY_NOTICES.md` | Audits and results; what was taken from other repositories. |

Project memory is the `## Tabby` section of the user's AGENTS.md (template in `interview/references/start.md`); tool and style defaults are the separate `## Python defaults` section. The core skill reads the section before a task when it exists. Claude Code reads CLAUDE.md, not AGENTS.md; the core suggests a one-line `@AGENTS.md` CLAUDE.md.

## Decisions that hold

- **Six skills, one level deep.** Research (SkillsBench, the AGENTS.md study, the progressive-disclosure papers) and our own flattening test (`AUDIT.md` section 6) say a router does not help. Each skill is self-contained: no links across skills except the review skill calling the checkers by path. Descriptions are imperative and list their trigger phrases; they do not share trigger nouns (`dashboard` is frontend, `architecture diagram` is diagrams).
- **Do the task; interview only on request.** Guesses are labelled `(assumed)`; the core offers `/tabby:interview` once. Nothing is saved to memory before an explicit yes to the restated summary.
- **The project's tools win.** Never swap a tool or add a second for a job one does. uv templates are for projects that have not chosen.
- **The reuse ladder is not "stdlib first":** the project's own tool, the standard library, the community's standard library, then niche libraries or your own code.
- **"Get rid of" a public name is a deprecation** unless nothing outside the repository can use it.
- **One look for pictures and screens.** `tabby-diagrams/diagrams/style.md` is the only place colours and fonts are defined (white ground, one accent, light and dark). A `design.md` maps onto the spec's `theme`.
- **Build from a spec, then check, then look.** Every checker has a self-test with seeded defects; run all three after changing a checker, builder or token. A finding is fixed in the spec or waived with a reason.
- **Animation is a self-contained HTML file by default**; video is rendered from it on request.
- **Completion gates are automatic for multi-part requests**, never for one-line fixes.
- **Content leads with the principle**, claims are grounded in source that was read or run, and nothing is copied from another project (examples are original).
- **Opt-in hooks stay off by default** and are shown exactly before they are enabled (planned, not built).
- A grader that matches Tabby's own vocabulary is `arm: with-only`: reported, not scored. Cases tagged `protocol` test behaviour Tabby defines; report them apart.

## Evals

A case is `case.yaml`, `prompt.md`, `fixture.sh`, `graders/*.md`. Run from the repository root with the batch runner:

`python3 tools/eval/run.py --out <dir> --all --plugin . --plugin-dir . --model claude-haiku-5-5 --runs 3 --batch 2 --jobs 2` (`--ablation with-without` is the default, `none` runs the plugin arm only; `--errored` re-runs cases with errored runs; `--keep-temp` keeps traces for `traces.py`). Summaries: `python3 tools/eval/summarise.py <dir> --csv out.csv [--compare other_dir]`. Trigger test: `python3 tools/eval/triggers.py --out <file> --queries evals/triggers.skills.json --runs 1 --model claude-haiku-5-5`.

- Granting `Bash` needs `bubblewrap` and `socat` (installed in this container).
- **Do not edit the plugin while an eval runs**: it is read live. Copy it to a scratch folder and pass `--plugin <copy> --plugin-dir <copy>`.
- **Usage limit.** A full run (91 cases, 3 runs, both arms) costs roughly $4 to $9. On 11 November the weekly limit cut a run off and the rest scored 0 without grading. The runner stops at the first limit error; re-run only the cut-off cases afterwards. A missing result file now counts as an error (earlier it printed `ok`).
- **Noise:** with three runs a per-case difference under about 0.3 should not be read; the mean over 91 cases moves about 0.01 between identical runs.
- A grader pointing at a file the agent never wrote counts as failed. Inside the sandbox the working directory can be read-only for `Bash` while `Write` works: skills that build files say to print to stdout and save with Write.
- Pitfalls writing cases: a prompt's quoted code must match the fixture exactly; write a task and a symptom, never the solution; keep scored graders free of Tabby vocabulary.

### Checks before committing

1. `claude plugin validate .` (an `ICON_MISSING` warning is expected), then `python3 tabby-diagrams/assets/diagram/selftest.py`, `node tabby-diagrams/assets/animation/selftest-motion.mjs`, `node tabby-frontend/assets/interfaces/selftest-ui.mjs` (the last two need Playwright Chromium).
2. Every skill description at most 1,024 characters (the combined listing is cut at 1,536).
3. `python3 tools/linkcheck.py`: relative links resolve and every leaf is named by another file.

## Open

- **Latest numbers (Haiku, 91 cases, 3 runs):** bare 0.754, one skill 0.812, six skills 0.840 (turns 17.1, cost +27% over bare). Sonnet check of the six skills: see `AUDIT.md` section 7. No held-out set yet; the cases were written next to the content.
- **Loading is the weak point.** On queries not used for tuning the skills load about 35% of the time on Haiku (68% on the tuned ones), and `tabby-frontend` is sometimes pre-empted by `tabby`. Next: tune the descriptions with a 60/40 split and a confusion matrix.
- **Cost.** Still +27% over bare, above the +10% target. The rules fire on the 36 cases the bare agent already passes. Scoping rules to the tasks that need them is untried.
- **Not built:** the opt-in hooks (`/tabby:hooks on`), a `detect` script, a hold-out set of about 15 new cases, five-run decisions, a leaf-ablation helper.
- **Worst current cases:** `three-pages`, `ci-job-for-a-uv-project`, `import-rows-some-fail`, `agents-md-for-a-repo` (all -0.2 to -0.36 against the one-skill plugin); `timeout-is-not-the-fix` stays near 0.2 in every arm.
- **Confidential content in git history.** An example animation scene from another project was in an earlier commit; it is gone from the tree but 6 commits still contain it. The owner will handle the history; do not rewrite history or force-push.
- **Not run:** the nanobind templates, long full-size video encodes. One model family, small single-turn fixtures.
- Keep `THIRD_PARTY_NOTICES.md` and the `SOURCE.md` files current when adding material.

## Working rules for this repo

- Commit and push each step to the designated branch only; no new PR.
- Flag any new tool or dependency before installing it.
- A `rm -rf` with a glob after a `cd` is blocked by the harness; use a fresh `mktemp -d`.
- Before reporting a number, say which run it came from and whether any run errored.
