# Handover

State of the repository for whoever continues it. Branch `claude/design-patterns-and-code-snags` (PR #4).

## What this is

Tabby: one registered Claude skill (`tabby/SKILL.md`) that routes to four modules, for AI coding agents working on Python projects, with Rust, C, C++ and Zig as native-extension citizens. Install: `/plugin marketplace add RelativelyUnknown/my-skills`, `/plugin install tabby@tabby`. Manifests are in `.claude-plugin/`; check with `claude plugin validate .`.

## Layout

| Path | Role |
| --- | --- |
| `tabby/SKILL.md` | Router and project memory rules. `description:` must stay at or under 300 characters. |
| `tabby/references/` | `start.md` (multi-round interview), `research.md` (read-only research feeding it), `growth.md` (build the seam, not the feature). |
| `tabby/development/` | Writing, testing, packaging, running code. Front door `index.md`; areas `code/`, `testing/`, `architecture/`, `workflow/`, `dependencies/`, `performance/`, `library/`, `application/`. |
| `tabby/review/` | Diff review, security audit, native boundary review. |
| `tabby/documentation/` | Diátaxis page types plus ADR, runbook, troubleshooting, changelog, style. |
| `tabby/design/` | Diagrams and explainer animations. |
| `tabby/evals/` | 53 eval cases plus `tabby.triggers.json`. |

Project memory is the `## Tabby` section of the user's AGENTS.md (`reviewed:`, `purpose:`, `users:`, `goals:`, `growth:`, `ask-first:`, `never:`, `kind:`, `modules:`, `commands:`). The router reads it before any task.

## Decisions that hold

- **Additive changes need approval.** `ask-first: public API change` covers new public names, not only breaking ones. `api-design.md` says so; "safe in a minor release" means compatible, not permitted. A task may grant one-off permission in its prompt.
- **Smells are split by area** (`code`, `library`, `testing`, `native`, `application`), each its own `smells.md`. No `io-smells.md`.
- **Content leads with the principle.** A file opens with the question to ask or the decision rule; examples are secondary and live in a sibling `*-examples.md` when long (`fit.md`/`fit-examples.md`, `senior-engineering.md`/`senior-engineering-examples.md`).
- **Every technical claim is grounded in real source** (cloned and read), not recalled. TigerBeetle, polars, Spark, DeepSeek (DualPipe, DeepEP, DeepGEMM, FlashMLA) and ziggy-pydust were read directly.
- **Prefer Rust for new native code.** `library/native/zig.md` covers Zig only for projects already using it.
- **Nothing is written to memory before an explicit yes** to the restated interview summary. At most three questions per round.
- **Do not detect overly verbose wording with grep.** It is flaky; do not suggest it.

## Audit of the "state it plainly, give examples, miss the essence" pattern

Every content file was checked. Result:

- **Rewritten earlier:** `architecture/senior-engineering.md` (was a list of named examples; now questions, with the stories in the sibling file).
- **Given an opening question this round** (they were bare rule lists): `code/minimalism.md`, `errors.md`, `comments.md`, `typing.md`, `logging.md`, `security-basics.md`; `testing/testing.md`, `fixtures.md`; `workflow/debugging.md`, `planning.md`; `library/shared/tooling.md`, `layout.md`; `documentation/voice.md`. The rules stay as the detail beneath.
- **Already principle-led, left alone:** `architecture/fit.md`, `design-patterns.md`; `code/stdlib-first.md`, `resources.md`, `validation.md`, `scripts.md`; `library/native/architecture.md`; `dependencies/dependencies.md`; `workflow/refactoring.md`, `shipping.md`, `checking-apis.md`; `library/shared/api-design.md`; `references/*`; `documentation/placing.md`, `style.md`, `concision.md`, `ai-patterns.md`; the `review/` files.
- **Reference by nature, left alone:** `application/**` (versioned facts run on a stated Python and library version), `dependencies/uv*.md`, `library/native/{c,rust,zig,ci-wheels}.md`, `library/shared/{release,versioning,entry-points,package-setup}.md`, `design/**` (a fixed visual vocabulary), page-type templates (`tutorial`, `how-to`, `reference`, `explanation`, `adr`, `runbook`, `symptom-fix-matrix`, `changelog`, `readme`, `docstrings`).
- **Lists by design, left alone:** every `smells.md` (smell → fix). Their intro says when to report one.
- **Not checked for rigor:** whether each added lead is the best wording. They are short and easy to tune.

## Evals

`claude plugin eval tabby --case <name> --runs 3 --ablation with-without --scaffold --allow-tools Write Edit --model claude-haiku-5-5 --judge-model haiku -j 3 --max-cost-usd 0.3 --trust-plugin --no-publish --json <path> --output-dir <path>`

A case is `case.yaml`, `prompt.md`, `fixture.sh`, `graders/*.md`. Pitfalls found:

1. A prompt's quoted code must match the fixture exactly, or the agent correctly stops to ask in both arms.
2. An `ask-first:` line in the fixture can block the task in both arms. Fix by granting permission in the prompt, not by weakening the fixture.
3. Write prompts as a task and a symptom, like the other cases; do not prescribe the solution.

`confine-unsafe-accessor` (confined `unsafe`): 0.87 with the skill, 0.93 without. No lift; the bare model already does this well. Its grader 03 (`// SAFETY:` comment at the call site) fails in some runs of both arms, which is the one place the skill could help.

## Open

- The README's numbers are stamped with commit hashes from earlier measurements and were not re-run after this round of edits. Re-measure before publishing them.
- Eval coverage for the new leads is indirect; no case targets them. Add cases only where a bare-model failure is observed.
- `development/SOURCE.md` credits upstream sources; keep it current when adding material.

## Working rules for this repo

- Check before committing: link checker (0 broken), `claude plugin validate .`, router `description:` length.
- Commit and push each phase to the designated branch only. Commits end with the attribution lines the session specifies.
- Flag any new tool or dependency before installing it.
