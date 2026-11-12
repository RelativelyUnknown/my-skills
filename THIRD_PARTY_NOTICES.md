# Third-party notices

Skills in this repository were adapted from the work of other authors. The adapted wshobson material is credited below with its copyright line, and `provenance/development-SOURCE.md` records (upstream URL, pinned commit, what changed); other adapted material keeps its licence and `SOURCE.md` next to it. Everything below is MIT-licensed; the MIT licence requires its copyright and permission notice to travel with every copy or substantial portion, which is why the licence text sits next to each adapted skill.

The rest of this repository is MIT (see `LICENSE`).

## wshobson/agents (python-development plugin)

- Upstream: https://github.com/wshobson/agents
- Author and licence: Copyright (c) 2024 Seth Hobson, MIT License
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d (5 November 2026)

| Upstream skill | Adapted into |
| --- | --- |
| `python-resource-management` | `tabby/development/code/resources.md` |
| `python-type-safety` | `tabby/development/code/typing.md` |
| `uv-package-manager` | `tabby/development/dependencies/uv.md`, `uv-ci.md`, `uv-docker.md` |
| `async-python-patterns` | `tabby/development/application/shared/async.md`, `async-patterns.md` |
| `python-background-jobs` | `tabby/development/application/workers/background-jobs.md`, `background-jobs-patterns.md` |
| `python-observability` | `tabby/development/application/shared/observability.md` |
| `python-configuration` | `tabby/development/application/shared/configuration.md` |
| `python-resilience` | `tabby/development/application/shared/resilience.md` |
| `python-error-handling` | `tabby/development/code/errors.md`, `validation.md` |
| `python-design-patterns` | `tabby/development/architecture/design-patterns.md` (three principles) |
| `python-testing-patterns` | one section of `tabby/development/testing/mocking.md`; the rest was already covered (see `provenance/development-SOURCE.md`) |
| `python-performance-optimization` | `tabby/development/performance/index.md`; the profiler tutorial was not copied (see `provenance/development-SOURCE.md`) |
| `python-packaging`, `python-project-structure` | `tabby/development/library/shared/versioning.md`, `entry-points.md`, `tooling.md`; the rest was already covered (see `provenance/development-SOURCE.md`) |
| `python-code-style` | pointer only; nothing copied (see `provenance/development-SOURCE.md`) |

## cloudflare/security-audit-skill

- Upstream: https://github.com/cloudflare/security-audit-skill
- Author and licence: Cloudflare, Inc., MIT
- Used as an approach only; no text copied. `tabby/review/security-audit/` restates, in new words and for Python, the boundary-and-result requirement, the source-to-sink trace, the attempt to disprove each candidate, the confirmed / needs-validation / rejected buckets with severity only for confirmed findings, and the fix with a regression test.

## Ideas only (no text copied)

- DietrichGebert/ponytail (MIT) and JuliusBrussee/caveman (Apache-2.0): the rules in the `tabby/development` front door and `code/comments.md` that comments say only what is not obvious, replies stay short, and negations ("not", "never", "only", "except") are never dropped. Names, installers, proxies and telemetry are not used.

## Read, nothing taken

blader/humanizer (MIT), softaworks/agent-toolkit `writing-clearly-and-concisely` (MIT), addyosmani/agent-skills (MIT), morganlinton/BeautifulRust (MIT), heydamir/unslop (CC BY 4.0), vercel-labs/agent-skills (no LICENSE file), mukul975/Anthropic-Cybersecurity-Skills (Apache-2.0), ComposioHQ/awesome-claude-skills, github/awesome-copilot (MIT). (cathrynlavery/diagram-design, caru-ini/stack-diagram and pbakaus/impeccable were listed here by mistake; they were reread on 2026-11-11 and are credited in the design section below.) They were read for ideas; where a baseline case showed the model already does the thing, nothing was added. Earlier unmodified copies of humanizer, writing-clearly-and-concisely and the wshobson Python skills were removed from the repository; the adapted wshobson material is in `tabby/development` with its pinned commit.

## Read for ideas, rewritten (added 2026-11-09)

No text copied; ideas restated in new words for the native-extension and router work. Licences noted for credit.

- OoriData/Amara `python-c` (Apache-2.0): when to go native, interface choice, a visible pure-Python fallback, modern C-API hygiene.
- pganssle/dotfiles `consensus-cpp-and-native` and `pablogsal-cpp-and-ml` (Apache-2.0): CPython C review rules (fallible calls, borrowed references, GC lifecycle slots). The persona framing is not used.
- VincentChuWaiChow/vanguard-frontier-agentic `python-native-extension-interop` (Apache-2.0): severity-ordered review of reference ownership, buffers and exception translation.
- affaan-m/ECC `cpp-coding-standards` (MIT) and ericrisco/rsc-harness `cpp` (MIT): C++ Core Guidelines digests, read, nothing taken yet.
- addyosmani/agent-skills `interview-me`, `spec-driven-development` (MIT) and pbakaus/impeccable `init` and `shape` (Apache-2.0): interview cadence, explore-first, confirm-then-stop; used for the `tabby` router.
- cloudflare/security-audit-skill `MEMORY-SAFETY-AND-BINARY.md` (MIT): the boundary table and FFI bug classes behind `tabby/review/native-boundary.md`.
- Layouts and CI practice studied (file trees and build files only; nothing copied): astral-sh/uv, astral-sh/ruff, pola-rs/polars, pydantic/pydantic-core, ijl/orjson, pyca/cryptography, pandas-dev/pandas, numpy/numpy, jcrist/msgspec.

## Fonts

The Tabby title image is rendered from "Pizza is my FAVORITE Font" by Kimberly Geswein (freeware; commercial use requires a donation; https://www.fontspace.com/pizza-is-my-favorite-font-f11293). The font file is not in this repository.

## Second review (2026-11-10)

Every source was cloned again at the commit below and read for ideas Tabby did not yet use. No text was copied; each idea is restated for Python and its native languages. The per-source findings are in `AUDIT.md`.

| Source (commit) | Licence | Idea taken | Where it went |
| --- | --- | --- | --- |
| DietrichGebert/ponytail (`96608e0`) | MIT | ask first whether the code needs to exist; a list of what minimalism never cuts; moved code keeps its checks; review against the expected load; a marked shortcut is a decision | `development/code/minimalism.md`, `workflow/refactoring.md`, `review/changes/self-review.md` |
| JuliusBrussee/caveman (`3dc497a`) | Apache-2.0 | when short replies must become full sentences; existing comments are not yours to shorten; why-first commit messages | `development/workflow/shipping.md`, `code/comments.md`, `documentation/commits.md` |
| morganlinton/BeautifulRust (`b971843`) | MIT | rules for the PyO3-free core crate (error enum, invariants in types, trait contracts, lossy casts, map order) | `development/library/native/rust.md` |
| cloudflare/security-audit-skill (`c1c8a8c`) | MIT | CI configuration as authorization code; integrity across build, test and publish | `review/security-audit/supply-chain.md` |
| addyosmani/agent-skills (`301b02b`) | MIT | observable behaviour becomes contract; state-dependent fields as a union; when to write an ADR and matching the project's ADR convention; details that must survive an edit; a timeout is an unknown outcome | `library/shared/api-design.md`, `code/typing.md`, `documentation/history/adr.md`, `documentation/concision.md`, `application/shared/resilience.md` |
| cathrynlavery/diagram-design (`f2496ac`), caru-ini/stack-diagram (`5af3b09`) | MIT | draw only when a table or sentence will not do; a node and line budget; three kinds of connection; accessible SVG; verify by rendering and looking | `design/diagrams/choosing.md` |
| github/awesome-copilot (`227949a`), `docs-sync-audit` | MIT | both sides of a docs mismatch; definite-answer checks first | `documentation/drift.md` |
| mukul975/Anthropic-Cybersecurity-Skills (`54a7988`) | Apache-2.0 | dependency-confusion and typosquat checks, as pointers | `review/security-audit/supply-chain.md` |

Read again, nothing taken: heydamir/unslop (`97daa3e`, interface restyling; its copy rules are already in `documentation/ai-patterns.md`), vercel-labs/agent-skills (`1a2c79d`, React and deployment rules; its one-rule-per-file layout was weighed against Tabby's smells lists and not adopted), ComposioHQ/awesome-claude-skills (`be2a406`, application connectors).

The C++ leaf (`development/library/native/cpp.md`) was written from the documentation in wjakob/nanobind (`af676a3`, BSD-3-Clause) and pybind/pybind11 (`3beb376`, BSD-3-Clause); no text copied.

## Gap fill (2026-11-10)

Ideas restated for Tabby; no text copied. `provenance/development-SOURCE.md` lists the leaves.

| Source (commit) | Licence | Idea taken | Where it went |
| --- | --- | --- | --- |
| morganlinton/BeautifulRust (`b971843`) `rust-port` | MIT | list the observable behaviour including the quiet parts, port the tests first, keep and flag the original's bugs, mapping tables | `development/library/native/porting.md` (the arithmetic and sorting rows were run with Python 3.13, rustc and g++) |
| addyosmani/agent-skills (`301b02b`) `spec-driven-development`, `incremental-implementation`, `planning-and-task-breakdown` | MIT | a short spec with boundaries and success criteria, thin vertical slices, checkpoints | `development/workflow/specs-and-slices.md` |
| github/awesome-copilot (`227949a`) `refactor-plan` | MIT | a plan with rollback and risks before a multi-file refactor | `development/workflow/refactoring.md` |
| DietrichGebert/ponytail (`96608e0`) `ponytail-audit`, `ponytail-debt` | MIT | audit order (bug, risk, load, test, speed, lean), a debt ledger of shortcut markers | `review/repo-audit.md` |
| cloudflare/security-audit-skill (`c1c8a8c`), addyosmani `doubt-driven-development` | MIT | a fresh verifier tries to refute each candidate | `review/security-audit/reporting.md` |
| addyosmani `deprecation-and-migration` | MIT | the questions before deprecating, advisory against compulsory, strangler, zombie code | `development/workflow/deprecation-and-migration.md` |
| morganlinton/BeautifulRust `lints/` | MIT | a lints block with the suppression and panic lints | `development/assets/native/Cargo.lints.toml` (run under clippy 0.1.97) |

## Design skills, read in full and adapted (2026-11-11)

The earlier entries for diagram-design, stack-diagram and impeccable said "nothing taken", and taste-skill and unlazy were not listed; that was wrong. Each was cloned and read in full at the commit below. No text, example, icon or diagram was copied; the ideas are restated in new words for Tabby's diagrams, animations, interfaces and completion gates. `tabby/design/SOURCE.md` lists them per leaf.

| Source (commit) | Licence | Idea taken | Where it went |
| --- | --- | --- | --- |
| cathrynlavery/diagram-design (`f2496ac`) | MIT | node treatment by role; six connector rules (orthogonal elbows, label gap, no overlaps, one attach point per connector, no transit behind a box, label mask before node); per-type budgets; a 4 px grid; choosing a semantic pattern before the visual type; mechanical geometry and accessibility checks as scripts; animation modes with budgets, a complete static frame and reduced motion | `design/diagrams/`, `design/animation/`, `design/assets/diagram/check.py` |
| caru-ini/stack-diagram (`5af3b09`) | MIT | labelled group containers; a node is its tile plus its text, so connectors anchor to the box boundary; edge labels with a halo; a pictogram for an abstract node, never text or emoji; render to PNG in both themes and look before delivering | `design/diagrams/connectors.md`, `design/assets/diagram/render.mjs` |
| Leonxlnx/taste-skill (`f6b7657`) | MIT | diagrams as small specs with a few layouts (hub, lanes, fan-in, sync, timeline); every motion gets a written purpose or is cut; a finish gate that runs the checker in a real browser with documented waivers; a copy-slop vocabulary | `design/diagrams/types/`, `design/animation/motion.md`, `design/interfaces/` |
| pbakaus/impeccable (`c1e0e54`, and the docs at impeccable.style) | Apache-2.0 | context before visuals; visitor modes (persuade, operate, read); a list of known defaults to refuse; a detector that runs in code with exit codes 0, 2 and 1; a critique split into two isolated assessments (judgment and detector) with a banner when they cannot be isolated; a motion thesis and one authored moment | `design/interfaces/`, `review/design.md`, `design/animation/motion.md` |
| Leonxlnx/unlazy (`1667149`) | MIT | acceptance gates written before the work, each with a runnable check and an expected result; gates that cannot fail are linted and given a negative control; the request is re-read and every claim re-measured before reporting; an unmet or abandoned gate is reported as a handoff | `development/workflow/gates.md` |

## Icons

The diagram icon set is Tabler Icons (MIT, Copyright (c) 2020-2026 Pawel Kuna; https://github.com/tabler/tabler-icons), outline style, vendored as one JSON file at `tabby/design/assets/icons/tabler-outline.json` with its licence in `tabby/design/assets/icons/LICENSE.tabler`.
