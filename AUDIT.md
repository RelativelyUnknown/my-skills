# Audit, November 2026

Three audits of Tabby against its mission: an opinionated, token-efficient skill set for the whole development process of a Python project and its native languages (C, C++, Rust, Zig), selected by a router from an interview or the project's scope. Each section says what was checked, what was found, what changed and what was left.

## 1. Third-party sources

Every listed source was cloned at its current commit and read for ideas Tabby did not yet use. An idea was adopted only when it closed a gap that could be named; it was restated in Tabby's words, principle first. No text was copied. Commits and licences are in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

| Source | Your target | Found | Decision |
| --- | --- | --- | --- |
| DietrichGebert/ponytail | Core skills, simpler inputs and types | Most of it was already in `minimalism.md` and `stdlib-first.md`. Missing: asking first whether code needs to exist, keeping values in the form they arrive in, a list of what minimalism never cuts, moved code keeping its checks, reviewing against the expected load | Adopted in `code/minimalism.md`, `workflow/refactoring.md`, `review/changes/self-review.md` |
| cloudflare/security-audit-skill | Review module | The boundary, trace and disprove method was already adapted. Missing: dependencies, CI and release | New leaf `review/security-audit/supply-chain.md`. Its 14 other domain files (cloud, mobile, protocols, AI) are outside a Python library or service audit and were left |
| morganlinton/BeautifulRust | Rust and PyO3 | Tabby's Rust leaf covered the binding only. The crate behind it had one line of style | New section "The core crate" in `library/native/rust.md` (error enum, invariants in types, lossy casts, trait contracts, map order). Bevy and port material left |
| pbakaus/impeccable, cathrynlavery/diagram-design, caru-ini/stack-diagram | One diagram and animation skill, no PowerPoint | `design/` had a visual style and an animation engine but nothing on whether to draw, which diagram, or how to check one. No PowerPoint wording remains (`grep -rniE "powerpoint|pptx|slide|deck" tabby` finds nothing) | New leaf `design/diagrams/choosing.md`. Their 45 diagram types, icon sets, importers and brand onboarding were left: too much to load for the diagrams a code project needs. impeccable is interface design and gave nothing new here |
| JuliusBrussee/caveman | Concise comments and docs | The rules against filler and dropped negations were in. Missing: when a short reply must become full sentences, leaving existing comments alone, commit messages | Adopted in `workflow/shipping.md`, `code/comments.md`; new leaf `documentation/commits.md`. The caveman voice itself is not used |
| addyosmani/agent-skills | API design | Call-site-first design and validation at the edge were in. Missing: observable behaviour becomes contract, state-dependent fields as a union, when to write an ADR and matching the project's convention, details that must survive an edit, a timeout as an unknown outcome | Adopted in `api-design.md`, `typing.md`, `history/adr.md`, `concision.md`, `resilience.md`. REST naming tables and TypeScript examples left |
| ComposioHQ/awesome-claude-skills | Architecture and patterns | Application connectors and office skills | Nothing taken |
| github/awesome-copilot | Architecture and patterns | Mostly other stacks. `docs-sync-audit` describes a docs drift audit Tabby lacked | New leaf `documentation/drift.md` |
| mukul975/Anthropic-Cybersecurity-Skills | Security workflows | 818 skills, mostly incident response and offensive tooling. Relevant: dependency confusion and typosquatting | Covered as checks in `supply-chain.md` and the existing `dependencies.md`; the tooling walkthroughs left |
| vercel-labs/agent-skills | Rewrite structure for Python | React, React Native and deployment rules, one rule per file with an impact rating | Not adopted. Tabby's per-area `smells.md` already holds one line per rule at a fraction of the tokens; splitting to a file per rule would multiply reads |
| heydamir/unslop | Rewrite structure for Python | Interface restyling. Its copy rules (no hype words, no unverifiable claims) are already in `documentation/ai-patterns.md` | Nothing taken |

The C++ leaf you asked for (`library/native/cpp.md`) was written from the nanobind and pybind11 documentation. One claim in my first draft was wrong and was corrected against the pybind11 docs before commit: an exception type not derived from `std::exception` becomes a `RuntimeError`, it does not terminate the process.

## 2. Skills against the mission

| Question | Finding | Action |
| --- | --- | --- |
| Does the router select a subset from an interview or the project scope? | Yes: `kind:` and `modules:` in `## Tabby` are written by the interview (`references/start.md`) and read before each task. A small fix on a project with no section skips the interview by design | None |
| One home for each fact? | `kind` was defined in both `## Tabby` and `## Python defaults` | `kind:` now lives only in `## Tabby` |
| Names from earlier layouts? | `adding-observability` (two files), "detected `async` fact", `render.py`, "engineering" in the marketplace manifest, `tabby/review/references/` in the notices, a doubled word in the router | Fixed |
| Principle first? | The handover's earlier audit holds. The five new leaves open with the question to ask | None |
| Token cost | Always-on description 297 characters. No content file is over about 5,300 characters except `SOURCE.md`, which is never loaded for a task | None |
| Every file reachable? | Every content file is named by an index or the front door; 0 broken links | Check script result recorded in the handover's working rules |
| Coverage of the mission's scope | Missing: C++, commit messages, docs drift, CI and release security, how to choose a diagram | Added. Web apps and data or ML leaves were not built, by your choice |
| Claims checked against real source? | New versioned claims name what they were checked against and say that nothing was compiled. GitHub Actions facts in `supply-chain.md` are from GitHub's documentation and were not exercised | Stated in the files |

Not done: a line-by-line check of every existing versioned claim (Django 6, uv 0.13, PyO3 0.30 and others) against current releases. They carry their own "checked on" dates.

## 3. Eval cases

### What was wrong

| Bias | Where | Effect | Fix |
| --- | --- | --- | --- |
| Graders that match Tabby's own vocabulary | `join-existing-native-library` (`## Tabby`, `kind:`, `modules:`, `(assumed)`), `agents-md-for-a-repo` (`## Python defaults`), `seeded-audit` ("confirmed", "needs validation") | The bare agent cannot know these words, so the lift was partly credited for wording. The README's largest lift (1.00 against 0.11) came from the first of these | Marked `arm: with-only`: reported, not scored. Outcome graders that either arm can pass were added in their place |
| Prompts that name the answer | `request-metrics-bounded-labels` ("think about what you label the metrics with"), `do-not-over-engineer-orders` ("Don't over-engineer"), `retry-a-flaky-http-call` and `stop-calling-a-failing-dependency` ("tests that run instantly"), `enqueue-after-commit` (the requirement spelled out the fix) | Both arms were handed the rule the case was meant to test | Rewritten as a task and a symptom |
| One accepted spelling of a correct answer | `bounded-fan-out-with-deadline` (`asyncio.timeout` and `TaskGroup` only), `batches-and-utc` (`batched` only), `payment-strategy` (a dict literal starting with `"card"`) | A correct solution in another form scored as wrong | Widened, or replaced by a rubric that states the behaviour |
| Graders that cannot pass | About 20 graders need a `Bash` call and one needs `WebFetch`; the eval cannot grant `Bash` here | They fail in both arms, lowering every absolute score and hiding part of the difference | Kept, because they are right when `Bash` is granted. Scores below exclude them and say so |
| Unbalanced, outdated trigger set | 58 should-trigger against 17 should-not; negatives such as "add type hints to src/pkg/io.py" contradicted the current description | A trigger test would have rewarded not firing on Python work | Rebuilt: 30 and 30 |
| Old tags | `python-engineering`, `using-uv` and 12 more from the 20-skill layout | Results could not be grouped by module | Retagged; `protocol`, `baseline` and `guard` tags added |

### What remains biased, and is labelled instead of fixed

- **Protocol cases** (`existing-project-first-round`, `fresh-project-asks-first`, `join-existing-native-library`) test behaviour Tabby itself defines: ask before building, at most three questions, save a memory section. A bare agent that starts building is doing what many users expect. These are reported apart from the outcome cases.
- **Opinion cases** (`literal-defaults-fetch-json`, `payment-strategy`, `one-settings-object`, `load-settings-house-rules`, `dedupe-lines-script`) grade Tabby's house style. The style has reasons, but the expected outcome comes from the skill, not from an outside standard.
- **Prompts are still tidier than real requests**: one task each, a named file, a small fixture (about 70 lines). `vague-request-larger-repo` is the one case that starts from a complaint. There is no multi-turn case and no case in a large or messy repository.
- **One model family** runs the agent and judges it (Haiku), three runs per arm.
- **Two-sidedness**: six cases can catch the skill over-applying a rule (`do-not-over-engineer-orders`, `hard-problem-take-a-library`, `validate-one-function-stdlib`, `clean-diff-no-noise`, `contradicting-test-left-alone`, `tiny-fix-stays-tiny`). The other 54 only reward applying one.

### Results

The full run after these changes (60 cases, 3 runs, with and without the skill) is in progress; this section is filled in from its results file.

