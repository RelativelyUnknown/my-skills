# Handover

State of the repository for whoever continues it. Branch `claude/design-patterns-and-code-snags` (PR #4).

## What this is

Tabby: one registered Claude skill (`tabby/SKILL.md`) that routes to four modules, for AI coding agents working on Python projects, with Rust, C, C++ and Zig as native-extension citizens. The audit behind the current state is in `AUDIT.md`. Install: `/plugin marketplace add RelativelyUnknown/my-skills`, `/plugin install tabby@tabby`. Manifests are in `.claude-plugin/`; check with `claude plugin validate .`.

## Layout

| Path | Role |
| --- | --- |
| `tabby/SKILL.md` | Router and project memory rules. `description:` must stay at or under 300 characters. |
| `tabby/references/` | `start.md` (multi-round interview), `research.md` (read-only research feeding it), `growth.md` (build the seam, not the feature). |
| `tabby/development/` | Writing, testing, packaging, running code. Front door `index.md`; areas `code/`, `testing/`, `architecture/`, `workflow/`, `dependencies/`, `performance/`, `library/`, `application/`. |
| `tabby/review/` | Diff review, security audit (code, and dependencies, CI and release), native boundary review. |
| `tabby/documentation/` | Diátaxis page types plus ADR, runbook, troubleshooting, changelog, commit messages, docs drift, style. |
| `tabby/design/` | Choosing and checking a diagram, visual style, explainer animations. |
| `tabby/evals/` | 84 eval cases plus `tabby.triggers.json` (30 should-trigger, 30 should-not). |

Project memory is the `## Tabby` section of the user's AGENTS.md (`reviewed:`, `purpose:`, `users:`, `goals:`, `growth:`, `out-of-scope:`, `constraints:`, `always:`, `ask-first:`, `never:`, `kind:`, `modules:`, `docs:`, `commands:`, `open:`; the template is in `tabby/references/start.md`). Tool and style defaults are the separate `## Python defaults` section; `kind:` is only in `## Tabby`. The router reads it before any task.

## Decisions that hold

- **Additive changes need approval.** `ask-first: public API change` covers new public names, not only breaking ones. `api-design.md` says so; "safe in a minor release" means compatible, not permitted. A task may grant one-off permission in its prompt.
- **Smells are split by area** (`code`, `library`, `testing`, `native`, `application`), each its own `smells.md`. No `io-smells.md`.
- **Content leads with the principle.** A file opens with the question to ask or the decision rule; examples are secondary and live in a sibling `*-examples.md` when long (`fit.md`/`fit-examples.md`, `senior-engineering.md`/`senior-engineering-examples.md`).
- **Every technical claim is grounded in real source** (cloned and read), not recalled. TigerBeetle, polars, Spark, DeepSeek (DualPipe, DeepEP, DeepGEMM, FlashMLA) and ziggy-pydust were read directly.
- **Prefer Rust for new native code.** `library/native/zig.md` covers Zig only for projects already using it; `library/native/cpp.md` covers C++ (nanobind for new bindings, pybind11 where it exists).
- **A grader that matches Tabby's own vocabulary is `arm: with-only`.** It is reported and not scored, so a lift is never credited for wording the bare agent cannot know.
- **Cases tagged `protocol`** test behaviour Tabby defines (the interview, the memory section). Report them apart from outcome cases.
- **The interview is opt-in.** `/tabby:interview` (`commands/interview.md`) or the phrase "run the Tabby interview"; the router suggests it in one line after the first task on a project with no section and never blocks on it. Once invoked: nothing is written to memory before an explicit yes to the restated summary, at most three questions per round.
- **Do not detect overly verbose wording with grep.** It is flaky; do not suggest it.

## Audit of the "state it plainly, give examples, miss the essence" pattern

Every content file was checked. Result:

- **Rewritten earlier:** `architecture/senior-engineering.md` (was a list of named examples; now questions, with the stories in the sibling file).
- **Given an opening question this round** (they were bare rule lists): `code/minimalism.md`, `errors.md`, `comments.md`, `typing.md`, `logging.md`, `security-basics.md`; `testing/testing.md`, `fixtures.md`; `workflow/debugging.md`, `planning.md`; `library/shared/tooling.md`, `layout.md`; `documentation/voice.md`. The rules stay as the detail beneath.
- **Already principle-led, left alone:** `architecture/fit.md`, `design-patterns.md`; `resources.md`, `validation.md`, `scripts.md`; `library/native/architecture.md`; `dependencies/dependencies.md`; `workflow/refactoring.md`, `shipping.md`, `checking-apis.md`; `library/shared/api-design.md`; `references/*`; `documentation/placing.md`, `style.md`, `concision.md`, `ai-patterns.md`; the `review/` files.
- **Reference by nature, left alone:** `application/**` (versioned facts run on a stated Python and library version), `dependencies/uv*.md`, `library/native/{c,rust,zig,ci-wheels}.md`, `library/shared/{release,versioning,entry-points,package-setup}.md`, `design/**` (a fixed visual vocabulary), page-type templates (`tutorial`, `how-to`, `reference`, `explanation`, `adr`, `runbook`, `symptom-fix-matrix`, `changelog`, `readme`, `docstrings`).
- **Lists by design, left alone:** every `smells.md` (smell → fix). Their intro says when to report one.
- **Not checked for rigor:** whether each added lead is the best wording. They are short and easy to tune.

## Evals

`claude plugin eval tabby --case <name> --runs 3 --ablation with-without --scaffold --allow-tools Write Edit --model claude-haiku-5-5 --judge-model haiku -j 3 --max-cost-usd 0.3 --trust-plugin --no-publish --json <path> --output-dir <path>`

A case is `case.yaml`, `prompt.md`, `fixture.sh`, `graders/*.md`. Pitfalls found:

1. A prompt's quoted code must match the fixture exactly, or the agent correctly stops to ask in both arms.
2. An `ask-first:` line in the fixture can block the task in both arms. Fix by granting permission in the prompt, not by weakening the fixture.
3. Write prompts as a task and a symptom, like the other cases; do not prescribe the solution.
4. Without `bubblewrap` and `socat` the eval cannot grant `Bash`; graders that need a `Bash` or `WebFetch` call then fail in both arms. `AUDIT.md` reports scores with those graders excluded.

`confine-unsafe-accessor` (confined `unsafe`): 0.87 with the skill, 0.93 without. No lift; the bare model already does this well. Its grader 03 (`// SAFETY:` comment at the call site) fails in some runs of both arms, which is the one place the skill could help.

## Open

- **Results (10 November 2026, 84 cases, 3 runs, both arms): 0.85 with, 0.76 without; +19% cost and +50% turns.** Efficiency targets (cost at most +15%, turns at most +35%) were missed. Full account and per-case table in `AUDIT.md`. A full run costs about $8 (more if the 5-hour usage limit interrupts it: use `--max-cost-usd` and check for `exit 1: You've hit your ... limit` errors, which score 0 without grading).
- **The senior-engineer methods have no measured benefit yet** (footprint, scout, learned note, options and seams on the API example). Either the model already does them or the instructions are not followed; reading the traces of `scout-reports-what-it-noticed` and `api-on-plain-sql-*` is the next step. The reuse ladder and deprecation rules do show lift.
- **Cost:** 51 of 84 cases tie; Tabby adds 22% there. Ideas not tried: shorten `development/index.md` (5.9 KB), drop `workflow/shipping.md` reading, make the `Noticed:` line optional for tiny changes.
- **The router description decides everything.** A rewrite that dropped "Rules for every code change ... Use whenever ..." cut loading from 114 to 49 of 180 runs. Test any wording on a dozen cases with `--ablation none --runs 1` before a full run. The router does not load on review, audit and documentation requests with any wording tried.
- **Confidential content in git history.** An example scene from another project was in the animation engine; it is removed from the current tree, but 6 commits on the PR branches still contain it. The owner said they will handle the history. Do not rewrite or force-push without their say-so.
- The C++, supply-chain, commit-message, docs-drift, porting, specs and slices, deprecation and repo-audit leaves are unproven except deprecation. nanobind templates were not built.
- `development/SOURCE.md` and `THIRD_PARTY_NOTICES.md` credit upstream sources; keep them current when adding material.

## Working rules for this repo

- Check before committing: link checker (0 broken), `claude plugin validate .`, router `description:` length.
- Commit and push each phase to the designated branch only. Commits end with the attribution lines the session specifies.
- Flag any new tool or dependency before installing it.
