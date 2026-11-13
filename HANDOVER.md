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
- Leaf triggers (13 Nov): a leaf in the "Read on demand" menu is rarely opened (`debugging.md` 0 of 3, `security-basics.md` 0 of 3 even when the skill fired). A rule in "Never miss" worded as a condition plus "before the first edit" fixed it (2 of 3 and 3 of 3, always before the first edit). Scores did not change on those cases (both arms tie), so reading the leaf is not yet shown to help. New cases: `fix-ssrf-in-link-preview`, `first-endpoint-from-a-library` (reads `growth.md` in 2 of 3 runs because `AGENTS.md` names the growth item).
- Menu to conditions (13 Nov): the core's "Read on demand" menu became "Read before the first edit" with conditions, plus a "read when you reach it" group. On 12 cases (Haiku, 3 runs, with-skill only): leaf reads per run 0.08 to 0.50, mean score 0.884 to 0.896, turns +3%, cost +3% (noise level). One case, `stream-command-output-with-limit`, reads about 4 leaves per run; `tiny-fix-stays-tiny` went from 3 to 8 turns with no leaf reads (score unchanged), so watch the guard cases. Core is 1,371 words. Ideas credited in `THIRD_PARTY_NOTICES.md`.
- Restructure experiments (13 Nov, 12 cases, Haiku, 3 runs, with-skill only, against the conditions-menu core above), both not adopted. (A) Merging `smells.md`, `minimalism.md` and `reuse.md` into one `code/writing.md` (2,100 words, 31 inbound links): leaf reads/run 0.50 to 0.72, turns 16.3 to 17.2, cost +3%, score 0.896 to 0.889 (one errored run in `stream-command-output-with-limit`). (B) Moving the "read when you reach it" group out of the core into `development/index.md`: core 1,371 to 1,329 words; reads/run 0.50 to 0.33, turns and cost equal, score 0.896 to 0.886. Neither moved reads, turns or score beyond noise; wording of the conditions mattered more than file layout. Both were built in scratch copies, not the repo.
- Smell metric (13 Nov): `tools/eval/quality.py` now also counts added violations of established ruff smell rules (B, SIM, TRY, BLE, ERA, PERF, RET, C4, PLR; PLR2004 ignored) and added comment lines, with no LLM judge. On the 13 Nov baseline (6 tasks, 3 runs per arm, old core): smells 0.44 per run with the skill vs 0.72 without, comment lines 0.00 vs 1.28, lines added 64 vs 89, hidden tests 0.986 vs 1.000, turns +36%. So the skill does reduce the narrating-comment and small-smell habits that `smells.md` and `minimalism.md` target, at least on these tasks (18 runs per arm; counts are small; comment lines also include legitimate comments). Not yet run on the newer core or on tasks written to tempt smells. Rule choices follow ruff's published catalogs (flake8-bugbear, simplify, tryceratops, blind-except, eradicate, perflint, pylint refactor); `senior-engineering.md` is design questions and is not countable on a small diff.
- LLM quality judge (13 Nov): `tools/eval/judge.py` judges with-skill against without-skill final diffs blind, in both orders, with a plain-language rubric (six criteria from common code-quality catalogs and `senior-engineering.md`, no Tabby vocabulary), Sonnet judging Haiku. On the 13 Nov baseline (6 tasks, 17 valid pairs, one unparseable): with-skill won 12, lost 0, tied 3 (all `tiny-fix-stays-tiny`), and 2 pairs flipped with the order. Per-criterion means: minimal and fits the codebase 4.68 vs 3.41, reuses what exists 4.62 vs 3.91, readable comments 4.29 vs 3.82, real-problem 4.68 vs 4.68, errors and invariants 3.85 vs 4.00, tests 3.62 vs 3.44. Read with care: the rubric itself says a smaller correct change beats a larger one, which favours the skill's own philosophy; the judge also noted fair trade-offs (limit validation missing in one skill-arm solution; `itertools.batched` needs Python 3.12). Same author as the content, one judge model, 6 small tasks. Use it next to the hidden tests and the smell counts, never alone; it has not been run on the newer core.
- Video ideas (13 Nov): transcripts could not be fetched (one mirror returned HTTP 530); third-party summaries of three CodeAesthetic videos were read instead. Added to `code/smells.md`: nesting over three levels (guard clauses, extraction), sentinel values and magic numbers, a comment explaining a compound condition, a variant added as a flag, and a base class added only to share a line. Added to `tools/eval/judge.py`: criteria `flat_control_flow` and `abstraction_earns_its_coupling`. Added to `tools/eval/quality.py`: `nest`, the nesting depth added. On the baseline `nest` is 1.0 in both arms because the six tasks never tempt deep nesting, so it cannot show an effect yet: write tasks that do (a deeply conditional importer; a second export format) before claiming the new smells rows work. The new rows are unmeasured and `smells.md` grew by 5 lines.
- Video summaries (13 Nov): `youtube-transcript-api` was installed in a scratchpad venv but YouTube returns `IpBlocked` for this network, so no transcript came through it; one agent per video then searched other pages. 11 videos (4 CodeAesthetic, 7 ArjanCodes) chosen from the channels' RSS feeds (aarthificial and Tsoding Daily are Rust/Bevy and C/Lua streams, skipped; the handle `@codeaesthetic` is the beginner-C "Malloc" channel and `@codeaestheticmalloc` is the real CodeAesthetic). Five gave usable content, six gave none. Added to `code/smells.md`: unbounded `functools.cache` on changing data, public mutable dataclasses, `match` on a boolean, subclass misuse, classes that build their own collaborators (constructor injection, fakes over `mock.patch`), naming (abbreviations, `Base`/`Abstract`). `smells.md` is now about 1,110 words (was 751) and is the file read first, so trim it if reads cost more than they help. The new rows are unmeasured; `judge.py`'s two new criteria cover them. Confidence in the sources is stated in `THIRD_PARTY_NOTICES.md`.
- A 50-word cap per finding and other report-length rules did not shorten reports (about 1,000 words either way); the cap was reverted.

## Open, in order of value

1. **Cost and turns.** Scope rules to tasks that need them; the skill adds reading on cases the bare agent already passes.
2. **Audit pages get read: resolved by the Read-next table.** In the 13 Nov rerun the agent opened class pages in about 6 of 7 old-core audit traces (mean 4.7 pages). A `pages.py` detect script (tried, reverted) did not change that (8 of 9, mean 3.7) or the seeded-audit scores (0.91 to 0.94 either way). The earlier "never opened" predates the front-door rewrite.
3. **Prune leaves that do not earn their words.** `tools/eval/leafusage.py` counts which files traces Read: of 143 content files, 98 (about 60% of words) were never opened in 651 traces, including `native-boundary.md` (~1,520 words) and `debugging.md` (~1,240). Ablating an unread leaf shows nothing, so first add cases that need those leaves, then ablate. Added 13 Nov: `review-pyo3-diff` (opens `native-boundary.md` in 2 of 3 runs; 1.00 with vs 0.89 without) and `debug-order-dependent-test` (skill did not fire in any with-skill run on "tests fail in the suite, sort it out", so `debugging.md` was never offered; 0.92 both arms; a loading gap, see item 8).
4. **Report length: tried, no gain.** A fixed per-finding block (title, path, fix, test) in `security-audit/reporting.md` made seeded-audit reports longer (mean 970 to 1,143 words, 12 runs each; scores 0.92 to 0.98 either way), so it was reverted. A report covers about 13 findings at roughly 75 words each; length follows the finding count. Untried: terse as the default for audits.
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
