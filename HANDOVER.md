# Handover

As of 12 November 2026. Branch `ccr-fafc7af6-jyh8oc`, pull request already open (do not open another). `AUDIT.md` has every measurement; this file is how to carry on.

## What this is

Tabby: a Claude Code plugin of six skills for Python projects (Rust, C, C++, Zig as native-extension languages), plus opt-in `hooks`. Claude Code only. Manifests in `.claude-plugin/`.

| Path | Role |
| --- | --- |
| `tabby/` | Core skill: "Never miss" rules, leaves under `development/`, project-memory rules |
| `tabby-review/` | Diff review, repo audit, bug hunt (`bug-hunt.md`, `two-places-agree.md`, `python-traps.md`, `state-machines.md`), security audit (`security-audit/`: `process.md` is the front door with a "Read next" table), native boundary, design review |
| `tabby-docs/`, `tabby-diagrams/`, `tabby-frontend/` | Docs types and style; diagrams and animation (builder, checkers, self-tests); web UI method and checker |
| `interview/` | `/tabby:interview` |
| `hooks/` | Opt-in reminder hook skill, off by default |
| `evals/` | ~92 cases, trigger sets, seeded-defect fixtures (`seeded-audit*`), hidden tests for code quality (`evals/quality/hidden/`) |
| `tools/` | `eval/run.py`, `summarise.py`, `traces.py`, `triggers.py`, `quality.py`; `linkcheck.py` |
| `AUDIT.md`, `THIRD_PARTY_NOTICES.md` | Results; credits for ideas taken from other repositories |

Project memory is the `## Tabby` section of the user's AGENTS.md (template in `interview/references/start.md`).

## Decisions that hold

- Six self-contained skills, one level deep; no router.
- Do the task; interview only on request. Guesses are labelled `(assumed)`.
- The project's own tools win; reuse ladder is project tool, stdlib, community standard, niche library, own code.
- "Get rid of" a public name is a deprecation.
- Content leads with the principle, is grounded in sources read or run, and is never copied (nothing vendored; credit in `THIRD_PARTY_NOTICES.md`; no licence files inside `tabby/`).
- Prevent slop while coding; review is for other people's diffs.
- Hooks stay opt-in.
- Graders that use Tabby's vocabulary are `arm: with-only` (reported, not scored).

## Measured effect (AUDIT.md top and sections 11 to 14)

- 91 cases, Haiku, 3 runs: six skills 0.82 to 0.84 vs bare 0.76; +27% to +35% cost, +50% turns. Sonnet, one run: 0.84 vs 0.78.
- Hard seeded audit: about 28 to 29 of 30 defects vs 22 bare, at about +45% cost. The agent never opened the class pages; the lift comes from loading the skill and reading `process.md`.
- Code quality (6 tasks): hidden tests at ceiling in both arms; fewer lint errors added with the skill; +38% cost.
- 13 Nov rerun (94 cases, Haiku, 3 runs, no errored runs): 0.809 with vs 0.772 without; cost +17%, turns +30%. About 15% of with-skill traces wander into the plugin copy's `evals/` (the runner needs it under the plugin), which inflates the skill arm.
- A 50-word cap per finding and other report-length rules did not shorten reports (about 1,000 words either way); the cap was reverted.

## Open, in order of value

1. **Cost and turns.** Scope rules to tasks that need them; the skill adds reading on cases the bare agent already passes.
2. **Audit pages get read: resolved by the Read-next table.** In the 13 Nov rerun the agent opened class pages in about 6 of 7 old-core audit traces (mean 4.7 pages). A `pages.py` detect script (tried, reverted) did not change that (8 of 9, mean 3.7) or the seeded-audit scores (0.91 to 0.94 either way). The earlier "never opened" predates the front-door rewrite.
3. **Prune leaves that do not earn their words.** `tools/eval/leafusage.py` counts which files traces Read: of 143 content files, 98 (about 60% of words) were never opened in 651 traces, including `native-boundary.md` (~1,520 words) and `debugging.md` (~1,240). Ablating an unread leaf shows nothing, so first add cases that need those leaves, then ablate.
4. **Report length.** Untried: terse as the default for audits, or a fixed per-finding template.
5. **Cases that get worse** (design, gates, vague asks; `three-pages`, `ci-job-for-a-uv-project`, `import-rows-some-fail`, `agents-md-for-a-repo`; `timeout-is-not-the-fix` near 0.2 everywhere).
6. **Measurement validity.** Cases and fixtures are written by the same author as the content; one judge model; effort level requested but unverified in traces; no outside benchmark, messy repository or multi-turn case.
7. **Unverified claims:** GitHub Actions behaviour, Semgrep's 1 MB skip, Python 3.14 `pdb -p`, nanobind templates, long video encodes. The new core has not been rerun on all 91 cases.
8. **Skill loading** is about 96% on unseen phrasings with the hook but 35% without it on Haiku; loading is no longer the bottleneck.
9. **Confidential content in git history:** an example scene from another project is in 6 older commits. The owner handles it; do not rewrite history or force-push.

## Evals

A case is `case.yaml`, `prompt.md`, `fixture.sh`, `graders/*.md`. From the repository root:

`python3 tools/eval/run.py --out <dir> --all --plugin . --plugin-dir . --model claude-haiku-5-5 --runs 3 --batch 2 --jobs 2`

Useful flags: `--ablation none|with-without`, `--errored` (re-run errored), `--keep-temp` (traces for `traces.py`, and kept working directories for `tools/eval/quality.py`). Summaries: `python3 tools/eval/summarise.py <dir> --csv out.csv [--compare other_dir]`.

- Do not edit the plugin while an eval runs; copy it and pass the copy to `--plugin`/`--plugin-dir`.
- A full run costs about $4 to $9. The runner stops at the first usage-limit error (exit 3); re-run only the cut-off cases.
- Noise: with three runs, a per-case difference under about 0.3 is not readable; the 91-case mean moves about 0.01 between identical runs.
- `Bash` grants need `bubblewrap` and `socat` (present here). Skills that build files print to stdout and save with Write.
- Writing cases: quoted code must match the fixture; give a task and a symptom, never the solution; keep scored graders free of Tabby vocabulary.

## Before committing

1. `claude plugin validate .` (an `ICON_MISSING` warning is expected); then `python3 tabby-diagrams/assets/diagram/selftest.py`, `node tabby-diagrams/assets/animation/selftest-motion.mjs`, `node tabby-frontend/assets/interfaces/selftest-ui.mjs` after changing a checker or builder.
2. Skill descriptions at most 1,024 characters.
3. `python3 tools/linkcheck.py` reports 0 broken.
4. Keep `THIRD_PARTY_NOTICES.md` and the `SOURCE.md` files current.

## Working rules

- Commit and push each step to the designated branch only.
- Flag any new tool before installing it.
- `rm -rf` with a glob after `cd` is blocked; use `mktemp -d`.
- Before reporting a number, say which run it came from and whether any run errored.
