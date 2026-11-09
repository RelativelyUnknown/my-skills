# Plan: Claude-first Python skillset with native-extension support and project onboarding

Written 2026-11-09 from the directive and a read of the third-party sources. Nothing in this plan is built yet.

## Product: Tabby (2026-11-09 brief)

Tabby is an opinionated set of skills for an AI agent to use across the whole life of a project (library, application, API, web app, tool), including the context around the code: ADRs, documentation, tests, diagrams, explainers. Python first, with Rust and C as first-class citizens. TypeScript and JavaScript later, not now.

- **The router is the product.** An interview (three questions up front, more only when context is missing) or the project's own scope decides which subset of skills the agent loads. Two entry modes: start a new project, or join an existing one. Answers are saved as editable project memory in `AGENTS.md` (section 3).
- **Goal:** highest quality, clarity, maintainability and explainability, at the lowest token cost.
- **Third-party skills are sources.** Ideas are taken and rewritten (section 2); nothing is adopted wholesale.
- **Identity:** name Tabby; logo `assets/tabby-logo.png` (the cat at the laptop, cut out from the supplied JPEG, see-through screen kept on purpose); crayon, rough-edged style; title set in "Pizza is my FAVORITE Font" by Kimberly Geswein.
  - **Font licence:** the font page says "Freeware, commercial use requires donation". The font file is not committed. The title is rendered once to an image and only the image is committed. The owner decides whether to donate or ask the designer for a licence.
  - **Font download:** fontspace returned 403 to a scripted download; the owner supplies the file.
- **README:** its own crayon style, written for a reader who has never seen the repo. Every claim in it must be true of what exists; planned features are marked as planned.

## 0. Decisions needed first

| # | Question | Recommendation |
| --- | --- | --- |
| D1 | **Decided: AGENTS.md first.** Claude Code reads `CLAUDE.md`, not `AGENTS.md`. | All project memory (`## Python defaults`, `## Project`) lives in `AGENTS.md`. Skills read and write only `AGENTS.md`. If the repo has no `CLAUDE.md`, suggest one line, `@AGENTS.md`, so Claude Code loads it; never copy the content. Tell the agent to use its question tool (`AskUserQuestion` on Claude). |
| D2 | "Fold documentation into python-engineering" reverses the three-skill split. | Fold `documentation/references/written/` into `python-engineering/references/fields/documentation/`. Keep the animation and diagram material as its own skill (directive item 3). Measure: the 5 docs cases must score at least as well as now (0.91 on `three-pages`). |
| D3 | Branch. The session says `ccr-5a44ac80-g3qmqp`; the handover says PR #4 lives on `claude/design-patterns-and-code-snags`. | Work on `ccr-5a44ac80-g3qmqp` as instructed, unless you say to move. |
| D4 | Your original list has no C or C++ source. | Use the community skills found in section 4a plus the official docs. Fetch the official ones: PEP 7, CPython devguide, Python/C API refcount and stable-ABI pages, PyO3 guide, maturin, scikit-build-core, cibuildwheel, Rust API Guidelines. Needs network hosts allowed. Idea-only, rewritten. |
| D5 | Probing native work needs `cargo`, `maturin`, a C compiler and sanitizers. | Check what is installed first; ask before installing anything. |

## 1. Target layout

```
python-engineering/      front door + software-engineering, architecture, documentation, start/ (onboarding), native/
python-review/           renamed from reviewing-python-code; shared by every discipline
python-design/           animation + diagrams, split out of documentation
```

- Frontmatter stays `name` and `description` (plus `license`). Descriptions at most 300 characters.
- Project memory lives in two editable sections of one file (`AGENTS.md`): `## Python defaults` (exists) and `## Project` (new, section 3).
- No new scripts, no test infrastructure for markdown. Checks are `grep` one-liners in the README.
- Debloat before adding: the front door goes from about 980 to at most 600 tokens; the 8 oversize leaves are cut to 4,200 characters.

## 2. What the third-party sources give us

Read in full or in the relevant parts. Licences matter: MIT/Apache sources are rewritten in our words with a notice; vercel-labs has no licence file (ideas only); unslop is CC BY 4.0 (keep the credit if any wording is adapted).

| Source | Take | Goes to |
| --- | --- | --- |
| BeautifulRust (`rust-best-practices`, `rust-review`, `rust-port`) | Rust-shaped code, library vs application split, ownership/clone tactics, error contracts, `// SAFETY:` and `# Safety` rules, FFI rules (`repr(C)`, same-side alloc/free, RAII wrapper, stop panics at the boundary, `-sys` crate plus safe core crate), lint config in `Cargo.toml`, review report shape (rule, `file:line`, fix, what is good), port flow (tests first, behaviour list, porting notes) | `native/rust.md`, `native/architecture.md`, review checklist, `native/porting.md` |
| cloudflare/security-audit-skill, `MEMORY-SAFETY-AND-BINARY.md` | One table per FFI boundary: accepted length/type, checked representation, allocation owner, consumer, thread, teardown. Classes: pointer-length and ownership mismatch, layout/enum disagreement, unwind across ABI, thread affinity, unload safety. Confirmed vs needs-validation rules, sanitizer coverage caveat | `python-review/references/native-boundary.md` (extends the existing security-audit leaves) |
| ponytail | Choose the smallest change in an ordered list; `shortcut: <limit>, <upgrade trigger>` comments plus a grep-only debt ledger; four-part findings (what, problem, fix, if skipped); "no concrete case, no finding" | Front door "smallest diff" rule, review report format, `all/workflow/planning.md` |
| caveman | Answer first, payload verbatim, never drop negations, one idea per sentence, bounded status between tool calls. `native-core`, `surgical-patch`, `safe-refactor`, `verify-and-stop`, `investigate-first` as one-paragraph rule sets | Already in the front door; add `investigate-first` and `verify-and-stop` wording to `workflow/debugging.md` and `shipping.md` only if a case fails |
| addyosmani/agent-skills | `interview-me` (hypothesis plus confidence, one question with a guess, restate with Out of scope, explicit yes, stop), `spec-driven-development` (assumptions list, six spec areas, three-tier boundaries), `api-and-interface-design` (Hyrum's law, contract first, additive change), `deprecation-and-migration`, `documentation-and-adrs` (match existing convention first) | `start/`, `library/shared/api-design.md`, documentation `history/` |
| impeccable | `init.md`: scan the repo first, never re-ask known facts, at most three questions per round, label inferred facts, probe once whether anyone can answer. `shape.md`: brief of 3-5 bullets when settled. Motion rules (purposeful, timing table) | `start/`, `python-design/` animation leaf |
| awesome-copilot | `memory-bank` (resume across sessions from a small set of files), `spec-driven-workflow` (requirements, design, tasks), ADR and PRD skills | Mostly confirms the `start/` design; take only the resume-from-files idea |
| diagram-design, stack-diagram | Deletion-first diagram philosophy, density target, one or two focal nodes; stack-diagram needs fetch scripts and Playwright, so no | `python-design/` (already partly there) |
| unslop | Direction before edits, audit-then-fix order | Only if `python-design` handles UI; low priority |
| vercel-labs, ComposioHQ/awesome-claude-skills | Nothing Python-specific. vercel is React/Next; Composio is app integrations. Fetching rules at run time (vercel) is rejected: unpinned remote instructions | Nothing taken |
| Anthropic-Cybersecurity-Skills (818 skills) | No Python/C-extension skills. Useful ideas only: AFL++ fuzzing workflow, Semgrep custom rules, SBOM, dependency-confusion and CI supply-chain checks | `python-review/references/` fuzz and supply-chain notes, only if a case fails |

Not read in full: impeccable's 40+ reference files and generated copies, diagram-design's 45 diagram types, and most of the 818 cybersecurity skills. I read what bears on this plan.

## 3. Onboarding: start a project or join one

Files: `python-engineering/references/start/{new-project,existing-project,project-section}.md`. The front door gets two lines that point to them.

**Trigger.** No `## Project` section in memory and the task is more than a small fix, or the user says "new project" or "I'm new here".

**Existing project (join).**
1. Read, do not ask: `pyproject.toml`, lockfiles, CI, layout, README, last commits, native build files (`Cargo.toml`, `setup.py`, `CMakeLists.txt`, `meson.build`).
2. Write down what was inferred, labelled `(inferred)`.
3. Ask only what the repo cannot answer (section below), at most three questions per round.
4. Save to memory.

**New project (start).** Same interview, then choose `kind:` from `which-type.md`, copy templates from `assets/`, and record the architecture choices the answers imply.

**The interview** (use the question tool; give a recommended option with each question; one round, a second only for a real gap):
1. What is it for, and who uses it? (purpose, users)
2. What does success look like in six months? (goals)
3. What is likely to change or grow? (more bindings, platforms, an API becoming a service, a hot path going native, new data sources)
4. Binding limits: Python versions, platforms, performance, team size, release cadence.
5. Out of scope.

Then restate in six lines (Outcome, Users, Success, Growth, Constraints, Out of scope), get an explicit yes, save, and stop.

**Saved shape** (`## Project` in `AGENTS.md`, editable, short; the format follows the real `AGENTS.md` files in section 4b: short lines, a repo map, one canonical command):

```
purpose: ...
users: ...
goals: ...
growth: [ordered list of expected expansions]
constraints: ...
out-of-scope: ...
extension-points: [seams chosen because of growth, with the reason]
revisit: when a goal changes or a growth item arrives
```

**Using it.** `growth` drives structure: each item maps to a seam to build now and a thing not to build yet (for example "may move a hot path to Rust later": keep a typed Python reference implementation and a thin import seam; do not create a Cargo workspace yet). The rule is the existing "no speculative generality", with the user's own stated growth as the only exception. At the start of any later task, the agent reads `## Project`; if the task contradicts `goals` or `out-of-scope`, it asks before proceeding. Old answers are meant to go stale: say so in the section header and tell the agent to ask whether they still fit when a task conflicts.

## 4a. C and C++ sources found online (2026-11-09)

There is no C/C++ equivalent of BeautifulRust. These came closest. All are read as data; ideas are rewritten, no text copied, and the licence notice goes in `THIRD_PARTY_NOTICES.md`.

| Source | Licence | What it is | Take |
| --- | --- | --- | --- |
| OoriData/Amara `.claude/skills/python-c` | Apache-2.0 | Python plus native: when to go native, which interface (ctypes, cffi, Cython, nanobind, raw C-API, PyO3), always ship a visible pure-Python fallback, C-API hygiene 3.12-3.14, free-threading, wheels | Best fit. Basis for `native/architecture.md` and `native/c.md` |
| pganssle/dotfiles `consensus-cpp-and-native`, `pablogsal-cpp-and-ml` | Apache-2.0 | CPython C review: fallible-call table, borrowed references across calls, `tp_clear` vs `tp_dealloc`, GC tracking on error paths, single `goto exit` cleanup, PEP 7 | Basis for the C refcount review checklist. They are written as personas of named people; take the rules, not the persona |
| VincentChuWaiChow/vanguard-frontier-agentic `python-native-extension-interop` | Apache-2.0 | Static review of C-API, Cython, PyO3: ownership, buffer protocol release, exception translation, abi3, GIL release | Severity-ordered rules; evidence labels (confirmed, inference, assumption) |
| affaan-m/ECC `cpp-coding-standards` | MIT | Digest of the C++ Core Guidelines (RAII, const by default, ownership, `enum class`) | `native/cpp.md`, only if a baseline fails |
| ericrisco/rsc-harness `cpp`; Jeffallan/claude-skills `cpp-pro` | MIT | General modern C++ and CMake | Skim only; overlaps ECC |
| Panoptic-Huginn/mimir-agent-kit `c-pro` | Apache-2.0 | C23, CERT C, MISRA, real-time robotics | Too specialised; take only the sanitizer and `-Wall -Wextra -Werror` gate and checked arithmetic (`ckd_add`) |
| questdb/py-questdb-client `review-pr` | Apache-2.0 | 140 KB project review skill | Not read in full; mine for the Rust/Cython/C review steps if B2 fails |

Official sources still to fetch and summarise: PEP 7, CPython devguide, Python/C API reference-count and stable-ABI pages, C++ Core Guidelines, PyO3 guide, maturin, scikit-build-core, cibuildwheel.

## 4b. Real packages studied (cloned 2026-11-09, file trees plus build, CI and agent files read; nothing built or run)

| Project | Languages and build | Layout lesson |
| --- | --- | --- |
| pydantic-core | Rust + PyO3, maturin | `src/` (Rust), `python/pydantic_core/` (Python, `.pyi`, `py.typed`), `build.rs`; release profile `lto = "fat"`, `codegen-units = 1`; PGO wheel action; `.mypy-stubtest-allowlist` keeps stubs honest; codspeed benchmark workflow; Makefile as the command surface |
| orjson | Rust, maturin | `src/` + `pysrc/orjson/`; CPython-only classifiers; benchmarks and `integration/` dir |
| uv, ruff | Rust binary shipped on PyPI, maturin `bindings = "bin"` | About 80 small crates in `crates/` (flat, one purpose each); `python/uv/` is a thin shim (`_find_uv.py` locates the binary); `rust-toolchain.toml`, `clippy.toml`, `rustfmt.toml` pinned; sdist `include` for files maturin cannot see |
| polars | Rust workspace + PyO3, maturin | `crates/` for core with no Python dependency; `crates/polars-python` holds the bindings; `py-polars/` is the pure-Python API package; compiled code ships as separate `polars-runtime-*` wheels (32, 64, compat), so the Python layer and the binary vary independently |
| cryptography | Rust (PyO3) + C via cffi to OpenSSL, maturin | `src/cryptography/` Python; `src/rust/` is a workspace of small crates (`-cffi`, `-x509`, `-openssl`, ...); `src/_cffi_src` generates C bindings; PyO3 with `abi3`; `overflow-checks = true` in release; one canonical command, `nox -e local` |
| pandas | C, C++, Cython, Meson | `pandas/_libs/` holds all native code; `meson.build` sets `c_std=c17`, `cpp_std=c++20`, `warning_level=2`; templated `.pxi` generation; one `pixi.toml` task set drives CI |
| numpy | C, Meson | `meson.build`, `.clang-format`, `compiler_sanitizers.yml`, `stubtest.yml`, `linux_simd.yml`, `wheels.yml` as separate workflows |
| msgspec | C, setuptools | `src/msgspec` single C extension; `.cibuildwheel.toml` builds `cp310` through `cp315` and the free-threaded `cp314t`/`cp315t`; `build-frontend = "build[uv]"`; wheel tests run `pytest` |

Patterns that repeat and become the `native/architecture.md` candidates (each is a hypothesis for a baseline case, not a rule yet):
1. The native code sits behind one private module (`_pydantic_core`, `_libs`) with a typed Python package in front, plus `.pyi` stubs and `py.typed`; stubs are checked in CI (`stubtest`).
2. Rust core crates do not depend on PyO3; a separate binding crate does (polars, cryptography, uv). Small crates, flat `crates/` directory.
3. Packaging file choices follow the language: Rust gets maturin, C/C++ gets Meson or scikit-build-core or setuptools, all with cibuildwheel for wheels.
4. Free-threaded and sanitizer jobs are separate CI workflows (numpy, msgspec).
5. One canonical check command per project (`nox -e local`, `make`, `pixi run`), written in `AGENTS.md`.
6. Release profile and build settings are set on purpose (`lto`, `codegen-units`, `overflow-checks`).
7. Toolchain files are committed (`rust-toolchain.toml`, `rustfmt.toml`, `clippy.toml`, `.clang-format`).

**What their `AGENTS.md` files show** (design input for section 3). cryptography: one canonical command, "use `uv`, not `pip`", changelog rule. pandas: purpose in one line, a repository map, required tooling, a pointer list to the real docs, and a rule that the agent never acts on GitHub for the user. uv: terse `ALWAYS`/`NEVER`/`PREFER` lines for tests, `SAFETY` comments and lockfile changes. All three are short and none contains a project-goals section; that gap is what `## Project` fills.

## 4. Multi-language libraries (Python with Rust or C)

Folder: `python-engineering/references/fields/software-engineering/library/native/` (separate from `library/shared`).

| Leaf | Content | Source |
| --- | --- | --- |
| `index.md`, `architecture.md` | When native is justified (profile first, existing `faster-libraries.md`). Layouts: pure core crate or C library with no Python dependency, thin binding layer, Python package with typed public API and `.pyi` stubs, pure-Python reference implementation for differential tests. Workspace and `src/` layouts, what stays public | BeautifulRust (core plus `-sys`), our own `layout.md`, official PyO3 and maturin docs |
| `rust.md` | PyO3 rules that matter at the boundary: no panics across it, error mapping to Python exceptions, GIL and `detach`, `from_py_object` opt-in, free-threading, ownership across the boundary, lint and `unsafe` rules | BeautifulRust, PyO3 changelog (already verified in the handover) |
| `c.md` | CPython C style (PEP 7), reference counting (new vs borrowed references), error indicator discipline, GIL, stable ABI limits, buffer protocol, multi-phase init, sanitizers (ASan, UBSan), fuzzing | Amara `python-c`, pganssle/pablogsal rules (section 4a), official CPython docs and PEP 7 |
| `cpp.md` (only if a baseline fails) | nanobind or pybind11 boundary, RAII, ownership, `const` by default, CMake target layout | ECC digest of the C++ Core Guidelines, official docs |
| `ci-wheels.md` | maturin or scikit-build-core, wheels with cibuildwheel, abi3 vs per-version, free-threaded job, sdist, `Cargo.lock` and vendoring, release checks | Official docs |
| `style.md` | One page: what formatter and linter each language uses and the commands (rustfmt, clippy, clang-format, clang-tidy, ruff), and that project config wins | Official docs |

`which-type.md` gains one row: a `[project]` with `Cargo.toml`, `setup.py` ext modules or `CMakeLists.txt` points to `library/native`.

**Rule from the handover is kept.** Each leaf above ships only after a baseline case shows the bare model fails, then a with/without run shows a gain. The PyO3 API probes already passed, so the baselines target what is left:
- B1 layout task: "add a Rust hot path to an existing package" (does it split core and binding, keep the pure-Python reference, add stubs and a CI wheel job?). Graded against the repeated patterns in section 4b, not against one project.
- B2 refcount review: a C extension with three seeded bugs (leaked new reference, borrowed reference used after a call that can free it, error indicator ignored) and three look-alikes
- B3 wheel and CI task for an extension (abi3, free-threaded, cibuildwheel)
- B4 boundary review of a PyO3 module using the Cloudflare boundary table
- B5 panic or exception crossing the boundary
Only the leaves matching a failed baseline are written.

## 5. Review skill (`python-review`)

- Rename `reviewing-python-code` to `python-review`; update `name:`, README and notices.
- Add `references/native-boundary.md`: the per-boundary table and the FFI classes from Cloudflare's memory-safety file, restated for PyO3 and C-API, plus a per-language checklist (Rust: `unsafe` blocks, panics, `Send`/`Sync`; C: refcounts, error indicator, buffer lifetime).
- Report shape: confirmed vs needs-validation (exists), plus BeautifulRust's Must / Should / Consider / What is good and ponytail's four-part finding. One shape, not three.
- Debt ledger: `git grep -nE '(#|//) ?shortcut:'` in the review front matter. No script.

## 6. Documentation folded in, design split out

- Move `documentation/references/written/*` to `python-engineering/references/fields/documentation/` (same file names, one `index.md`). Add routing rows to the front door for README, docstring, ADR, runbook, troubleshooting, contributing.
- Keep the four add-ons that exist (ADR, runbook, symptom/fix matrix, contributing). Build the others (release notes, migration guide, incident manual, onboarding checklist, SLA, security policy, code standards) only after a baseline case fails. The onboarding checklist overlaps section 3: write one, not two.
- `python-design/`: `references/diagrams/style.md`, `references/animation/*`, `assets/animation/*` moved out of `documentation`. Keep the `design.md` integration and the no-PowerPoint rule (`grep -rniE "powerpoint|pptx|slide|deck" python-design` returns nothing).
- Fix the known fire-rate problem: the docs rows in the front door replace the weak docs-skill description. Re-run the 5 docs cases and the fire-rate method from the handover.

## 7. Phases, each ends in a commit and a push

| Phase | Work | Gate |
| --- | --- | --- |
| P0 | Resolve D1-D5. Check installed tools. | Your answers |
| P1 | Debloat: front door to at most 600 tokens, trim the 8 oversize leaves, remove any rule no case checks | Existing cases do not drop. **Done 2026-11-09:** trimmed leaves to within about 4% of 4,200 characters; front door 4,271 to about 3,750 characters (about 940 tokens, not 600: every routing path is kept). Full run, Haiku 5.5, 3 runs: old 0.841, new 0.818, cost $1.67 vs $1.44. Re-run of 9 dropped cases at 5 runs: mean 0.779 vs 0.775 (noise). Two real losses, both from wording I cut (front-door "extra, lazy import" and the stdlib-first opening bullets); restored: `optional-parquet-dependency` 0.32 to 0.77, `hard-problem-take-a-library` 0.71 to 0.84. Lesson: a one-line pointer in the front door is load-bearing. |
| P2 | Rename to `python-review`; fold documentation in; split `python-design` | Docs cases at least 0.91; link and name checks via grep |
| P3 | Onboarding (`start/`) | Two new cases: join an existing repo, start a repo (graded on: inferred facts labelled, at most three questions, restate with Out of scope, `## Project` written, stops after the yes). Run with and without. |
| P4 | Native baselines B1-B5 | Per-baseline scores recorded |
| P5 | Native leaves for failed baselines only, plus review `native-boundary.md` | With/without gain per leaf |
| P6 | Re-run the full case set serially with `--max-cost-usd` and the usage-limit guard; update README sizes, notices, handover | Score at least the 0.788 baseline; cost per run reported, not hidden |

## 8. Risks

- The routing test already showed cost rose 13% for no score gain. Adding native and onboarding material raises it further. Mitigation: load only the files a task names; onboarding runs once per project.
- Onboarding changes behaviour, so its test is graded on conduct (few questions, stops after yes), not knowledge. A grader is an LLM judge on one model, so treat the result as a signal.
- The interview needs a live user. In a non-interactive run the agent must say so, mark answers `(assumed)`, and continue, as the existing defaults rule does.
- Claude-first means Copilot behaviour (`#vscode/askQuestions`, nested folders) is no longer a target. Nothing is removed for Copilot; it simply is not tested.
