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

Final measurement: 84 cases, 3 runs per case and arm, 504 valid runs, Haiku 5.5 as agent and as judge, `claude plugin eval --ablation with-without`, shell and web fetch granted (`bubblewrap` and `socat` installed). Scores are weighted pass rates of the scored graders; graders marked `arm: with-only` are reported, not scored. With three runs, a difference under about 0.15 on one case is noise.

| | With Tabby | Without |
| --- | --- | --- |
| Mean score, all 84 cases | **0.85** | 0.76 |
| Outcome cases (74) | 0.84 | 0.77 |
| Protocol cases (10: interview, saved section, text in the repo) | 0.93 | 0.65 |
| Guard cases (9: the right result is to do little) | 0.94 | 0.70 |
| Cases where the bare agent already passed (5 baselines) | 0.93 | 0.96 |
| Cost per run | $0.0168 | $0.0142 (+19%) |
| Turns per run | 16.2 | 10.8 (+50%) |
| Score per dollar | 50 | 53 |
| Router loaded | 192 of 252 runs (76%) | |

By how much Tabby changed each case:

| Group | Cases | Score with / without | Cost per run |
| --- | --- | --- | --- |
| Helps by 0.10 or more | 26 | 0.90 / 0.56 | +17% |
| Within 0.10 | 51 | 0.87 / 0.86 | +22% |
| Hurts by 0.10 or more | 7 | 0.54 / 0.73 | +8% |

**Against the targets set before the run**

| Target | Result |
| --- | --- |
| Mean score at least the bare agent's | Met: +0.09 |
| Cost per run at most 15% above the bare agent | **Missed: +19%** |
| Turns at most 35% above | **Missed: +50%** |
| Each new senior, options and ladder case at least 0.1 above the bare agent, or reported as unproven | **3 of 12 met**; the rest are unproven (below) |

**What the evidence supports**

1. **Tabby makes the agent follow engineering habits it would otherwise skip.** The largest gains: deprecate instead of delete (1.00 against 0.18), join a project and run the interview (1.00 against 0.25), a dict of functions instead of a class hierarchy (0.94 against 0.33), take the ecosystem's standard HTTP client (0.90 against 0.30), ask before changing something the saved section rules out (1.00 against 0.43), find that a timeout is not the fix (0.54 against 0.00), ask instead of guessing on a vague request (0.80 against 0.30), take a library for a hard problem (0.77 against 0.27), keep a pip or poetry project's own tools (up to +0.35).
2. **It is not cheaper.** The score gain costs 19% more per run and half again as many turns, because it reads and reports more. Score per dollar is 50 against 53. On the 51 cases where it changes nothing it is overhead: +22% cost for a difference of 0.01.
3. **Where it hurts (7 cases):** `speed-up-matcher` (0.08 against 0.42; the router loaded in none of the 3 runs, so this is probably noise in a case with LLM-judged graders), `vague-feature-gets-a-short-spec` (0.15 against 0.41), `dev-tool-and-script-dependency` (0.79 against 1.00), `api-on-plain-sql-growth-known` (0.52 against 0.69), `new-package-one-check-command` (0.75 against 0.90), `cpp-binding-return-policy`, `niche-library-or-five-lines` (each -0.10).
4. **The senior-engineer additions are mostly unproven.** Of the 12 cases written for them, three show a lift: community standard over hand-rolled (+0.60), timeout is not the fix (+0.54), ecosystem fit, ordering (+0.22). No lift or a loss: the footprint of a similar change (1.00 both), learned-something note (0.86 both), scout (0.61 against 0.67), the API on plain SQL with growth known (0.52 against 0.69) and unknown (0.44 against 0.50), CLI to team tool (+0.04), the niche library case (-0.10). The options-and-seams method, which is what the API example was meant to test, did not show a benefit on this model; the lift on those two cases is not there.
5. **The leaves added in this audit show little.** Porting to Rust +0.04, C++ return policy -0.10, CI workflow audit +0.05, repo audit +0.11, specs and slices -0.26 on its one case. They are kept because the mission names those areas, and are unproven.
6. **Design:** with a design.md the diagram used the brand colours and fonts (0.89 against 0.81); without one the default case ties at 0.67 in both arms (the shell sandbox made the working directory read-only in some runs, so some runs could not save the file).

**How the numbers moved during the audit** (same cases where they overlap)

| Step | Change | Effect measured |
| --- | --- | --- |
| Interview first (the starting state) | A project with no saved section triggered the interview | `new-package-one-check-command` 0.36 against 0.98 |
| Interview as a command | Offered once at the end, never a gate | the same case 0.75 against 0.90 (the stall is gone) |
| Leaner front door | One leaf read instead of every match | Tabby reads of its own files per run 6.1 to 3.4 on 21 cases |
| Reuse ladder, senior method, kind index | This run | the table above |

**Incident:** the first full run of the final state reached the account's 5-hour usage limit; 236 of its 504 runs ended in an API error and scored nothing. The 41 cases that were cut off were re-run in full after the reset on the same commit, and the table above merges the 43 complete cases with those. Spend on measurement in this session was about $30 in total.

**Not measured or not run**
- Animation encoding (MP4, WebM, GIF): the example scene was rendered to PNG stills in light and dark and compared with a static diagram; the full encode was not run. The bundled fonts were not installed (npm), so renders used the system Inter.
- The nanobind CMake and pyproject templates were not built (nanobind not installed). The Cargo lints block was run under clippy.
- GitHub Copilot was never run. One model family, three runs, small single-turn fixtures, LLM judge of the same family.
- The router does not load on review, audit and documentation requests: the cases for them score 0 of 3 loaded, so Tabby's effect there is not measured.

**Per case, final run** (sorted by difference)

| Case | With | Without | Difference |
| --- | --- | --- | --- |
| `deprecate-instead-of-delete` | 1.00 | 0.18 | +0.82 |
| `join-existing-native-library` | 1.00 | 0.25 | +0.75 |
| `payment-strategy` | 0.94 | 0.33 | +0.61 |
| `community-standard-over-handrolled` | 0.90 | 0.30 | +0.60 |
| `saved-section-conflicts-with-task` | 1.00 | 0.43 | +0.57 |
| `timeout-is-not-the-fix` | 0.54 | 0.00 | +0.54 |
| `vague-ask-clarifies-briefly` | 0.80 | 0.30 | +0.50 |
| `hard-problem-take-a-library` | 0.77 | 0.27 | +0.50 |
| `existing-project-first-round` | 0.92 | 0.49 | +0.44 |
| `pip-requirements-project-keeps-its-tools` | 1.00 | 0.65 | +0.35 |
| `literal-defaults-fetch-json` | 0.78 | 0.44 | +0.33 |
| `typed-decorator-keeps-signature` | 1.00 | 0.67 | +0.33 |
| `interview-saves-after-yes` | 0.67 | 0.33 | +0.33 |
| `exhaustive-event-handling` | 1.00 | 0.77 | +0.23 |
| `dedupe-lines-script` | 1.00 | 0.77 | +0.23 |
| `ecosystem-fit-ordering` | 0.89 | 0.67 | +0.22 |
| `retry-a-flaky-http-call` | 1.00 | 0.79 | +0.21 |
| `interview-vague-yes-does-not-save` | 1.00 | 0.81 | +0.19 |
| `contradicting-test-left-alone` | 0.88 | 0.73 | +0.15 |
| `load-settings-house-rules` | 0.93 | 0.79 | +0.14 |
| `vague-request-larger-repo` | 1.00 | 0.87 | +0.13 |
| `adr-runbook-troubleshooting` | 0.99 | 0.86 | +0.13 |
| `find-faster-json-library` | 0.67 | 0.55 | +0.12 |
| `request-id-on-every-log-line` | 1.00 | 0.89 | +0.11 |
| `vet-before-adding` | 0.78 | 0.67 | +0.11 |
| `audit-repo-bloat-and-load` | 0.95 | 0.84 | +0.11 |
| `ecosystem-fit-shell-words` | 1.00 | 0.92 | +0.08 |
| `bug-fix-starts-red` | 0.50 | 0.42 | +0.08 |
| `optional-parquet-dependency` | 0.69 | 0.61 | +0.08 |
| `diagram-honours-design-md` | 0.89 | 0.81 | +0.07 |
| `poetry-black-unittest-keeps-its-tools` | 0.87 | 0.80 | +0.07 |
| `validate-with-existing-pydantic` | 1.00 | 0.94 | +0.06 |
| `clean-diff-no-noise` | 0.61 | 0.56 | +0.06 |
| `audit-ci-workflow` | 0.85 | 0.79 | +0.05 |
| `validate-one-function-stdlib` | 0.97 | 0.92 | +0.05 |
| `batches-and-utc` | 0.76 | 0.71 | +0.05 |
| `three-pages` | 0.89 | 0.85 | +0.05 |
| `cli-to-team-tool` | 0.93 | 0.89 | +0.04 |
| `port-hot-path-to-rust` | 0.88 | 0.84 | +0.04 |
| `add-owned-resource-endpoint` | 1.00 | 1.00 | +0.00 |
| `agents-md-for-a-repo` | 1.00 | 1.00 | +0.00 |
| `ci-job-for-a-uv-project` | 0.88 | 0.88 | +0.00 |
| `clean-up-ingest-module` | 0.53 | 0.53 | +0.00 |
| `clear-ask-no-interview` | 1.00 | 1.00 | +0.00 |
| `confine-unsafe-accessor` | 0.80 | 0.80 | +0.00 |
| `de-rerunnable-load` | 1.00 | 1.00 | +0.00 |
| `diagram-of-a-small-service` | 0.67 | 0.67 | +0.00 |
| `do-not-over-engineer-orders` | 1.00 | 1.00 | +0.00 |
| `enqueue-after-commit` | 1.00 | 1.00 | +0.00 |
| `footprint-of-a-similar-change` | 1.00 | 1.00 | +0.00 |
| `fresh-project-open-request` | 1.00 | 1.00 | +0.00 |
| `import-rows-some-fail` | 1.00 | 1.00 | +0.00 |
| `learned-something-offers-a-note` | 0.86 | 0.86 | +0.00 |
| `local-development-env-file` | 1.00 | 1.00 | +0.00 |
| `native-free-threaded` | 1.00 | 1.00 | +0.00 |
| `native-pyclass-by-value` | 0.90 | 0.90 | +0.00 |
| `numpydoc-docstrings` | 0.78 | 0.78 | +0.00 |
| `one-settings-object` | 0.44 | 0.44 | +0.00 |
| `readme-for-small-package` | 1.00 | 1.00 | +0.00 |
| `repo-text-addressed-to-the-agent` | 1.00 | 1.00 | +0.00 |
| `request-metrics-bounded-labels` | 0.86 | 0.86 | +0.00 |
| `settings-loaded-at-startup` | 0.91 | 0.91 | +0.00 |
| `single-source-version` | 0.56 | 0.56 | +0.00 |
| `stop-calling-a-failing-dependency` | 1.00 | 1.00 | +0.00 |
| `stop-early-from-an-async-generator` | 1.00 | 1.00 | +0.00 |
| `stream-command-output-with-limit` | 1.00 | 1.00 | +0.00 |
| `tiny-fix-stays-tiny` | 1.00 | 1.00 | +0.00 |
| `welcome-email-exactly-once` | 1.00 | 1.00 | +0.00 |
| `write-small-service-module` | 0.91 | 0.91 | +0.00 |
| `zig-extension-review` | 1.00 | 1.00 | +0.00 |
| `seeded-audit` | 0.86 | 0.88 | -0.02 |
| `scout-reports-what-it-noticed` | 0.61 | 0.67 | -0.06 |
| `native-gil-checksum` | 0.82 | 0.88 | -0.06 |
| `api-on-plain-sql-growth-unknown` | 0.44 | 0.50 | -0.06 |
| `bounded-fan-out-with-deadline` | 0.93 | 1.00 | -0.07 |
| `ml-leaky-validation` | 0.92 | 1.00 | -0.08 |
| `pick-a-set-representation` | 0.67 | 0.75 | -0.08 |
| `niche-library-or-five-lines` | 0.71 | 0.81 | -0.10 |
| `cpp-binding-return-policy` | 0.80 | 0.90 | -0.10 |
| `new-package-one-check-command` | 0.75 | 0.90 | -0.16 |
| `api-on-plain-sql-growth-known` | 0.52 | 0.69 | -0.17 |
| `dev-tool-and-script-dependency` | 0.79 | 1.00 | -0.21 |
| `vague-feature-gets-a-short-spec` | 0.15 | 0.41 | -0.26 |
| `speed-up-matcher` | 0.08 | 0.42 | -0.33 |

## 4. Design redesign and the 11 November run

What changed (all on branch `ccr-fafc7af6-jyh8oc`): one quiet look for diagrams, animations and interfaces; a spec-to-SVG builder; a vendored icon set (Tabler, MIT); animations as one self-contained HTML file; interface checks; a design review; completion gates for multi-part coding work; a reworded router description. The three checkers are tested by their own self-tests (nine, eight and fourteen seeded defects). Sources and what was taken from each: `THIRD_PARTY_NOTICES.md` and `tabby/design/SOURCE.md`.

### The run is incomplete

The full run (91 cases, 3 runs per arm, Haiku) was cut off by the account's usage limit: from about 10:14 UTC every run ended with `exit 1: You've hit your weekly limit · resets Nov 15, 5pm (UTC)` and scored 0 without being graded. **252 of 546 runs errored; 45 of 91 cases have at least one such run, 39 of them all six.** A mean over all cases (0.44 with Tabby, 0.40 without) would be an artefact of the limit and is not a result. The limit was spent by router tests, case development and this run.

### What the 46 fully valid cases show

No errored run in either arm. Mean score **0.80 with Tabby, 0.73 without**; 10 cases improve by 0.10 or more, 4 get worse by 0.10 or more, 32 tie; turns +49%, cost per run +27%.

On the 41 of them that also have a 10 November score: 0.86 then and 0.82 now with Tabby, 0.74 then and 0.72 now without. The lift went from +0.12 to +0.09. With three runs per case (about 0.15 of noise on one case, about 0.03 on the mean of 41) this is a signal to confirm after the re-run, not a finding; the router description, the larger front door and the new modules are the suspects.

### New and changed cases (valid runs only)

| Case | With Tabby | Without | Turns with | Turns without |
| --- | --- | --- | --- | --- |
| `diagram-of-a-small-service` | 0.67 | 0.96 | [23, 26, 30] | [8, 11, 9] |
| `diagram-state-machine` | 0.67 | 0.63 | [25, 18, 19] | [8, 10, 11] |
| `animation-self-contained-html` | 0.22 | 0.69 | [32, 27, 25] | [11, 7, 10] |
| `docs-site-brand-and-dark-mode` | 1.00 | 1.00 | [17, 16, 18] | [12, 11, 10] |
| `gates-multipart-missed-requirement` | 0.61 | 0.94 | [26, 28, 26] | [18, 17, 18] |
| `gates-trivial-no-ceremony` | 0.70 | 0.70 | [4, 5, 4] | [4, 4, 4] |

`ui-orders-page-accessibility`, `review-a-page-before-shipping` and `diagram-honours-design-md` had errored runs and are not measured.

**The three that score worse with Tabby are a turns problem, not a content problem.** The `with` runs used 23 to 32 turns against 7 to 18 for the bare agent, the cap is 30 for the design cases, and each of the three has at least one run that scored 0 because the deliverable was never written: the agent read five or six design pages, built, checked and rendered before saving the first file. Where a file was written, the Tabby-specific graders pass (the checker was run, every step has a purpose, the final message accounts for every part of the request: 3 of 3 against 0 of 3 for the bare agent on the gates case). The traces are deleted without `--keep-temp`, so the exact turn at which the file is written is not yet known. Fix applied (not yet measured): one quickstart per kind that contains everything needed for the first file (`design/diagrams/quickstart.md`, `design/animation/quickstart.md`), the deeper pages read only on need, and a missing tool reported instead of installed.

### Router wording (no baseline arm, 14 cases)

Metric: how often the skill is invoked, which is what the description controls. Identical wording gave 16 and 11 loads out of 28 runs, so two runs per case are too noisy to compare and four were used. Original wording: 27 of 56 (two runs of 28). "Code or page reviews, … docs sites, … animations" wording: 31 and 28 of 56 in two runs at four per case. Other wordings, four runs per case: one that replaced the original verbs ("use before writing, changing, reviewing, auditing or drawing") loaded 27 of 56; one that kept the original verbs and added "animations, web pages, dashboards" but not "page reviews" or "docs sites" loaded 21 and 19 of 56 (two measurements of the same text); one that kept the verbs and added "code or page reviews, docs sites, animations" but dropped "starting or joining a project" loaded 33 of 56. The final wording loads for the page review, docs-site and UI cases that the original never loaded for (0 of 4 to 3 or 4 of 4); the overall rate is about the same. Review and audit prompts about code (`audit-repo-bloat-and-load`, `clean-diff-no-noise`) are the ones that vary most between wordings.

### To re-run after the limit resets (Nov 15, 17:00 UTC)

Re-run only these, `--case <name>` one at a time, three at a time at most, stopping on the first limit error: `load-settings-house-rules`, `local-development-env-file`, `ml-leaky-validation`, `native-free-threaded`, `native-gil-checksum`, `native-pyclass-by-value`, `new-package-one-check-command`, `niche-library-or-five-lines`, `numpydoc-docstrings`, `one-settings-object`, `optional-parquet-dependency`, `payment-strategy`, `pick-a-set-representation`, `pip-requirements-project-keeps-its-tools`, `poetry-black-unittest-keeps-its-tools`, `port-hot-path-to-rust`, `readme-for-small-package`, `repo-text-addressed-to-the-agent`, `request-id-on-every-log-line`, `request-metrics-bounded-labels`, `retry-a-flaky-http-call`, `review-a-page-before-shipping`, `saved-section-conflicts-with-task`, `scout-reports-what-it-noticed`, `seeded-audit`, `settings-loaded-at-startup`, `single-source-version`, `speed-up-matcher`, `stop-calling-a-failing-dependency`, `stop-early-from-an-async-generator`, `stream-command-output-with-limit`, `three-pages`, `timeout-is-not-the-fix`, `tiny-fix-stays-tiny`, `typed-decorator-keeps-signature`, `ui-orders-page-accessibility`, `vague-ask-clarifies-briefly`, `vague-feature-gets-a-short-spec`, `vague-request-larger-repo`, `validate-one-function-stdlib`, `validate-with-existing-pydantic`, `vet-before-adding`, `welcome-email-exactly-once`, `write-small-service-module`, `zig-extension-review`. Then the three worse cases again with `--keep-temp` and read their traces.

## 5. Evidence map for the restructure (12 November; plan in the session's plan file)

Data: the complete Haiku run (91 cases, 3 runs per arm, no errored run: `tools/eval/results/2026-11-11-haiku-3runs.csv`), a Sonnet run (91 cases, one run per arm: `...-sonnet-1run.csv`) and one kept-trace Haiku run per case with the skill (read with `tools/eval/traces.py`). Re-running the 45 cases that the usage limit cut off on 11 November completed the picture.

| Model | With Tabby | Without | Lift | Improve / worse / tie | Turns | Cost per run |
| --- | --- | --- | --- | --- | --- | --- |
| Haiku, 3 runs | 0.812 | 0.754 | +0.057 | 17 / 7 / 67 | +46% | +24% |
| Sonnet, 1 run | 0.865 | 0.782 | +0.083 | 22 / 6 / 63 | +61% | +37% |

Tabby does not hurt the stronger model, but its overhead is larger there. The 10 November lift (+0.09 on Haiku) shrank to +0.057 on the same kind of cases; with three runs per case this is within noise of an unchanged skill, not proof of a regression.

**Where the extra cost goes (Haiku).** 36 cases where both arms score 0.9 or more take 30% of the extra cost; 17 where both score under 0.7, 16%; 12 middling ties, 12%; 7 cases where Tabby is worse, 17%; the 19 lift cases, 25%. Three quarters of the extra cost buys nothing measurable.

**What the agent actually reads (91 traces).** The skill loaded in 70 of 91 runs. Per run the agent opened a mean of 1.8 skill files (median 1, maximum 8) and the first file was written at turn 5.1 on average. Of 154 Markdown files only **38 were ever opened**. Most read: `development/index.md` (60 runs), `development/code/smells.md` (21), `development/testing/testing.md` (9), `development/which-type.md` (7), `development/code/validation.md` (5), `references/start.md` (5). The router and the front door are the effective skill; the hierarchy below them is almost never walked.

**Where the lift comes from.** 10 of the 19 lift cases read nothing beyond `development/index.md`, and the largest, `deprecate-instead-of-delete` (+0.82, the deprecation leaf never opened) and `payment-strategy` (+0.73), came from lines in the front door or the router: the "Never miss" list (deprecate a public name, climb the reuse ladder, never loosen a test, ask when the request is vague, use the project's own tools) and the router's "Section exists" rules. Two lift cases came from `references/start.md` (the interview and joining a project) and one from the documentation module. The cases that read the most (`adr-runbook-troubleshooting`, six documentation files) also lift, so reading is not harmful where the task matches the leaf.

**What probably costs turns.** Steps 2, 3, 6 and 7 of the front door's method (map the project in five commands, state the want in one line, scout and list `Noticed:`, offer what was learned) and the mandatory `Noticed:` closing line are instructions the agent follows (the AGENTS.md study found the same: agents follow context-file instructions and spend more steps and cost). This is a hypothesis to test by ablation, not a finding.

**Worse cases are still the design and gates cases** (`animation-self-contained-html` -0.46, `gates-multipart-missed-requirement` -0.33, `diagram-of-a-small-service` -0.29) plus two resource and resilience cases (`stream-command-output-with-limit` -0.33, `stop-calling-a-failing-dependency` -0.30). In the traces the design cases read the index and the quickstart and wrote their first file at turn 5 to 6, so the quickstarts worked on reading volume; the remaining gap on those cases is in the work itself (build, check, render loops) and in graders that need the checker to run, which the bare agent never does.

**Caveat.** The eval cases are small, single-turn fixtures. A leaf that is never opened here may matter in a large real task, so the 116 unread files are candidates to demote into a skill's on-demand reference folder, not to delete.


## 6. Flattening experiment (12 November; Haiku, 3 runs, all 91 cases, with-arm only, bare arm reused from section 5)

Question: does removing the router, the front-door method and the `Noticed:` rule cut turns and cost without losing lift (hypothesis H1)? Variants are in `tools/eval/variants/`: V1 = router text plus the "Never miss" list with direct leaf pointers, no method steps, no `Noticed:` (7.9 KB); V2 = V1 plus the seven-step method and `Noticed:` (10.0 KB). Same 298-character description; rest of the plugin unchanged.

| Arm | Score | Turns | Cost per run | Improve / worse vs bare (±0.10) |
| --- | --- | --- | --- | --- |
| Bare | 0.755 | 11.1 | $0.0119 | |
| Current plugin | 0.818 | 16.1 | $0.0147 | 17 / 6 |
| V1 flat, lean | 0.813 | 15.0 | $0.0145 | 24 / 16 |
| V2 flat, method | 0.802 | 14.3 | $0.0140 | 22 / 17 |

V2 had one errored case (`animation-self-contained-html`), excluded from its means (90 cases).

Reading: **the score does not change** (0.813 vs 0.818 is inside the noise of three runs), **turns fall 7% to 11% and cost 1% to 5%**, and the plugin still costs about +22% over bare. The gate (cost at most +10%) is not met. So the router and the method are not where the cost comes from; the cost is the agent following the "Never miss" rules (verify by running, read before writing, report). Per-case results move a lot (worse count 6 vs 16 with the same mean): `payment-strategy` 1.00 to 0.61, `community-standard-over-handrolled` 0.50 to 0.94, `hard-problem-take-a-library` 0.50 to 0.91, `timeout-is-not-the-fix` stays at 0.15 to 0.25 in every arm. With three runs, per-case differences under 0.3 should not be read.

Decision: flattening is **safe and slightly cheaper but not a lever**. It is adopted as part of the split (a router no longer exists once each module is its own skill), not as a cost fix. The cost lever that remains is making the rules fire only where they help (the 36 cases bare already passes), which is a hold-out and rule-scoping question for the next phase, not a structure question.


## 7. Split into six skills (12 November; Haiku, 3 runs, all 91 cases, with-arm only, bare arm reused from section 5)

The plugin was split into `tabby` (core, native fused in), `tabby-review`, `tabby-docs`, `tabby-diagrams`, `tabby-frontend` and `interview`, each with its own description. Two defects found in the first split run were fixed before this one: the `interview` skill returned no body while it was a command with `disable-model-invocation` (now a plain skill named `interview`), and the diagram quickstart failed in a read-only shell (it now says to print the SVG to stdout and save it with the Write tool). Results: `tools/eval/results/2026-11-11-haiku-split-6skills.csv`; no errored runs.

| Arm | Score | Turns | Cost per run |
| --- | --- | --- | --- |
| Bare | 0.754 | 11.1 | $0.0120 |
| Current plugin (one skill) | 0.812 | 16.2 | $0.0149 |
| V1 flat | 0.812 | 15.1 | $0.0147 |
| **Six skills** | **0.840** | 17.1 | $0.0153 |

Against the current plugin: 18 cases improve and 9 get worse by 0.10 or more. Biggest gains: `vague-ask-clarifies-briefly` +0.62, `hard-problem-take-a-library` +0.50, `interview-saves-after-yes` +0.48, `community-standard-over-handrolled` +0.35, `vague-feature-gets-a-short-spec` +0.32. Biggest losses: `three-pages` -0.36, `ci-job-for-a-uv-project` -0.30, `import-rows-some-fail` -0.30, `agents-md-for-a-repo` -0.21.

Reading: the split gives **+0.03 score over the current plugin and +0.09 over bare, at +2.7% cost over the current plugin (+27% over bare)**. The gain is real in size (more than the 0.01 noise between the two earlier arms) but not yet proven: three runs, no hold-out, and the cases were written next to the content. Cost is still above the +10% gate. Skill loading on unseen phrasings stays at about 35% on Haiku (see the trigger tests), so the next steps are description tuning with a held-out split and a Sonnet check.

**Sonnet 5.5, one run per case, all 91 cases, plugin arm only** (`tools/eval/results/2026-11-12-sonnet-split-6skills.csv`; the one-skill and bare figures are from the Sonnet run in section 5):

| Arm | Score | Turns | Cost per run |
| --- | --- | --- | --- |
| Bare | 0.782 | 7.7 | $0.085 |
| One skill | 0.865 | 12.5 | $0.117 |
| Six skills | 0.840 | 10.9 | $0.111 |

On Sonnet the split is 0.025 below the one-skill plugin (10 cases better, 17 worse by 0.10 or more; one run, so per-case moves are noise) and 6% cheaper. Two cases explain most of the gap: `diagram-of-a-small-service` (1.00 to 0.00) and `animation-self-contained-html` (0.78 to 0.09). The trace of the animation case shows why: the builder and checker wrote to the project from Bash, which was read-only in the sandbox, and the agent retried other paths until it gave up without writing the file. The diagram case scored 0.95 on a repeat, so it is flaky. The animation quickstart now says to print to stdout and save with Write (as the diagrams quickstart already did). That fix is **not yet measured**: the re-test hit the 5-hour usage limit (resets 01:30 UTC) and both runs errored, so they are not counted. Without those two cases the Sonnet means are within about 0.01 of each other.

**Re-test of the two Sonnet failures, after the stdout note** (the six-skill plugin, 3 runs each, plugin arm only, no errored runs): `diagram-of-a-small-service` 0.95, 0.95, 0.95 (was 0.00 in the full run); `animation-self-contained-html` 0.68, 0.68, 0.09 (was 0.09). The remaining 0.09 run again found the shell read-only, printed the 20 KB page to stdout, and stopped instead of copying it into the Write tool. The read-only shell is a property of the eval sandbox, so this costs score here but should not occur in a normal project; the animation quickstart still depends on the agent copying the printed page, which is the weak step. With these re-test means (0.95 and 0.49) the Sonnet total for the six skills moves from 0.840 to about 0.85, near the one-skill plugin's 0.865; this is an estimate, not a full run.


## 8. Skill loading: descriptions and an optional reminder hook (12 November; Haiku 5.5)

Question: why do the skills load on only a third of unseen prompts, and what raises it? The test is `tools/eval/triggers.py`: each prompt runs once per run with `claude -p` in an empty folder, with the plugin loaded, and the first `Skill` call decides the result (`none` if the run ends or writes a file first). 153 new prompts were written for this (`evals/triggers.dev.json`, 91, used while tuning; `evals/triggers.holdout2.json`, 62, run only to report), covering the five task skills and 25 prompts that need no skill. 3 runs per prompt, cost about $0.80 to $1.25 per run of a set.

| Arm | Dev (273 runs) | Hold-out (186 runs) |
| --- | --- | --- |
| Old descriptions ("Invoke before ..."), no hook | 116 (42%) | 86 (46%) |
| Old descriptions + reminder hook | 179 (66%, first wording) | 176 (95%, final wording) |
| New imperative descriptions, no hook | 209 (77%) | 129 (69%) |
| New descriptions + reminder hook | not run | 170 (91%) |

- The failure is almost never a wrong skill: the confusion matrix is nearly empty off the diagonal. It is **no skill at all** (on the hold-out, 56 of 156 task prompts loaded nothing with the old descriptions). The one real confusion is `tabby-frontend` prompts that load `tabby` (9 of 24 on the hold-out, no hook).
- Descriptions that say "MUST be your first tool call, before reading files, asking questions or answering" raise loading on unseen prompts from 46% to 69% (hold-out). The dev figure is inflated because the wording of three descriptions was adjusted after reading its misses.
- A `UserPromptSubmit` hook that prints a 120-word reminder naming the skill for each kind of task raises loading to 91% to 95% on the hold-out, including 30 of 30 correct "no skill" prompts. A weaker, descriptive reminder ("invoke the Skill ...") gave 66% on dev; the imperative form with a bullet per skill gave 93%. With the hook the description wording matters little (95% old vs 91% new, inside the noise of 3 runs).
- This mechanism is the one the popular packs use (superpowers injects its bootstrap at session start). Here it ships **off by default**: `/tabby:hooks on` shows the reminder text and the settings entry, then writes it to `.claude/settings.json` on a yes; `/tabby:hooks off` removes it. It runs one `cat` and nothing else.
- Limits: empty-folder prompts, Haiku only, one prompt per run, so a real session with a repository and a saved `## Tabby` section may load more often; the hook result is the loading rate; the task score is in the next paragraph.


## 9. Worst-case fixes and the detect script (12 November; Haiku, 14 cases, 3 runs, plugin arm only)

What the traces of the cases that scored worst said, and what was changed:

- `speed-up-matcher` (0.25 in every arm): a **broken case**. The prompt names `matcher.py` and `test_matcher.py`, but the case had no fixture, so the agent searched for files that did not exist (once it read Tabby's own eval folder). The case now has a fixture. Its earlier scores are not comparable.
- `dev-tool-and-script-dependency`, `import-rows-some-fail` (one of two runs 0 or 0.38): the shell was read-only (`mount` showed `ro`), `Write` still worked, and the agent gave up and pasted code into its reply. New core rule: on `Read-only file system`, make the change with Write and Edit, run what can run, and say which command could not.
- `timeout-is-not-the-fix` (0.25 in every arm): the skill did not load in either traced run, so no rule could apply. New core rule: asked to raise a timeout, limit or retry count, first read what the failing code does; name and fix or offer a fixable cause, then do what was asked. **Not shown to work**: the skill still did not load in 3 of 3 runs of the re-test inside `plugin eval` (it did load in 2 of 3 under `claude -p` with the hook).
- `agents-md-for-a-repo`, `ci-job-for-a-uv-project`: 1.0 in both arms on repeat. The earlier drops were noise.
- Added `tabby/scripts/detect.py` (files only; runner, Python target, tests, format and lint, types, check command, CI, docs, native, project memory). First attempt: injecting its output into the skill with `` !`...` `` made the whole skill body vanish in a read-only shell (the shell wrapper failed writing its own state file, and Claude Code treated that as a failed command), which dropped `deprecate-instead-of-delete` from 1.00 to 0.22 and `hard-problem-take-a-library` from 1.00 to 0.52 in that run. The skill now tells the agent to run the script as its first command, so a failure costs one line, not the skill. Lesson: never make a skill's body depend on a command that can fail.

Result with the final core (hook on in the test plugin; `tools/eval/results/` has the CSV):

| Cases (14) | Bare | One skill | Six skills (old) | Six skills + new core |
| --- | --- | --- | --- | --- |
| Mean score | 0.699 | | 0.785 | **0.824** |

Turns fell on 12 of the 14 (for example `new-package-one-check-command` 33.3 to 20.7, `bug-fix-starts-red` 15.7 to 11.7); `detect.py` was run in 3 of 3 runs on 12 of the 14 cases. `speed-up-matcher` is not comparable, `timeout-is-not-the-fix` is unchanged (loading), `bug-fix-starts-red` 0.44 against 0.74 in the hook run (noise or a real loss; 3 runs cannot tell).

**What the agent reads** (165 kept traces of the hook run and this run): `development/code/smells.md` 74, `scripts/detect.py` 36, `development/which-type.md` 30, `development/code/reuse.md` 20, `development/testing/testing.md` 16, `interview/references/start.md` 9, `tabby-diagrams/diagrams/quickstart.md` 9, then 7 or fewer for everything else; 58 distinct files in all. No leaf was demoted or deleted: unread leaves cost nothing until opened, the single-turn cases cannot show what a rarely read leaf is worth, and the only place leaves cost tokens is the core's reading list, which was left as it is until an ablation shows a line can go.


**Full run with the new descriptions and the hook** (Haiku, 91 cases, 3 runs, plugin arm only, no errored runs, `tools/eval/results/2026-11-12-haiku-hook-descriptions.csv`; compared on the 90 cases whose fixture did not change):

| Arm | Score | Turns | Cost per run | Skill loaded |
| --- | --- | --- | --- | --- |
| Bare | 0.760 | 11.2 | $0.0118 | |
| Six skills, old descriptions, no hook | 0.844 | 17.2 | $0.0152 | about 77% (earlier trace sample) |
| Six skills, new descriptions + hook | 0.822 | 16.7 | $0.0160 | 96% (259 of 270 runs) |

Loading went up, the score did not: 7 cases better and 14 worse by 0.10 or more than the old six-skill run. The biggest drops are `vague-ask-clarifies-briefly` (-0.42) and `vague-feature-gets-a-short-spec` (-0.40), which were the biggest gains in the previous run, so part of this is regression to the mean; the difference of 0.02 is inside the noise of three runs. Reading: on cases that run inside a repository the skill already loaded most of the time, so a reminder buys little there; its value is for short prompts in real sessions, which is what the trigger test measures (46% to 95%). It stays **opt-in**; it is not a score lever. These two arms also differ in the rewritten descriptions, so the run cannot separate the two changes. The new core (section 9) was measured on 14 cases only.

## 10. Seeded-defect fixture for the rebuilt audit content (12 November 2026)

Case `evals/seeded-audit-python`: a small shop backend with 12 planted defects (SQL string building, missing owner check, mass assignment, pickle upload, SSRF, JWT algorithm from the header, tar extraction, read-then-write race, fail-open empty key, unsigned webhook, order shipped unpaid, non-constant-time compare) and 8 look-alikes (parameterised query, fixed-URL fetch, auto-escaped template, md5 cache key, test-only helpers, `yaml.safe_load`, constant subprocess list, `random.choice` for a banner). 12 regex graders score recall (a defect counts when the report names its function, route or class), 8 LLM graders score the look-alikes. Haiku, 3 runs per arm, with and without the plugin, no run errored.

| Arm | Recall (per run) | Look-alikes not flagged (per run) |
| --- | --- | --- |
| with plugin | 12/12, 12/12, 12/12 | 8/8, 5/8, 8/8 (21/24) |
| without | 12/12, 12/12, 12/12 | 7/8, 7/8, 6/8 (20/24) |

Reading: this fixture does not separate the arms. Recall is at the ceiling in both, and the regex graders credit any mention of the function name, so a bare agent that lists the files scores full recall; it measures naming, not a correct explanation. The precision gap (87.5% against 83.3%) is one look-alike in 24 and inside the run-to-run spread (the plugin's own runs range from 5/8 to 8/8). It is not evidence that the rebuilt content helps. A harder fixture is needed before claiming a gain: subtler defects, graders that require the cause and the entry point in the same finding, and more runs. Not done here.

## 11. Harder seeded-defect fixture (12 November 2026)

Case `evals/seeded-audit-hard`: a small ledger service of 12 modules with 10 defects that each need two or more files read together, 8 look-alikes, and 19 LLM graders (a defect counts only when the report gives the cause and how it is reached). Planted: an export job trusting a `user_id` copied from the request body; a path check on the raw name while the NFKC-normalised name is opened; a string-prefix directory check; a refund check-then-act race; a login rate limit keyed on `X-Forwarded-For`; a `None == None` password-reset bypass; a signature check skipped by the truthy string `"0"`; mass assignment from `vars(user)`; an order status written outside the transition table by the webhook and a nightly job; a per-user response cached under the path. The prompt names no bug class, and hints in the first draft (an "untrusted" docstring, a comment on the skip flag, a function called `safe_call`) were removed before any run. Several defects were run by hand (fullwidth dots through the check, the prefix, `None == None`, `bool("0")`, `vars`).

Sonnet (`claude-sonnet-5-5`), effort requested as low through `CLAUDE_EFFORT` and `CLAUDE_CODE_EFFORT_LEVEL` (the eval command has no effort option and the traces do not record it, so low is not verified), 3 runs per arm, no run errored, Haiku as the judge.

| Run | Defects found (of 10) | Look-alikes not flagged (of 8) | Turns | Cost |
| --- | --- | --- | --- | --- |
| with 1 | 9 (missed the normalised path) | 7 | 6 | $0.159 |
| with 2 | 10 | 6 | 8 | $0.181 |
| with 3 | 10 | 7 | 8 | $0.171 |
| without 1 | 8 (missed export job, normalised path) | 7 | 2 | $0.125 |
| without 2 | 6 (missed export job, refund race, reset bypass, status writers) | 4 | 2 | $0.117 |
| without 3 | 8 (missed export job, skipped signature) | 5 | 2 | $0.116 |

Totals: with 29/30 defects and 20/24 look-alikes correct; without 22/30 and 16/24. The export job through the queue was missed in 3 of 3 runs without the skill and 0 of 3 with it. The `fetch_preview` look-alike was reported as a plain SSRF in 5 of 6 runs in both arms, so the skill did not fix that false positive. The report separated confirmed from unconfirmed in 1 of 3 runs with and 0 of 3 without.

Reading: unlike section 10, this fixture separates the arms, mostly on recall of the cross-file defects, at about 45% more cost (the agent read more files: 6 to 8 turns against 2). Caveats: 3 runs per arm, one model, an LLM judge that is generous with partial credit, effort unverified, and the fixture was written by the same author as the content it tests. No page was edited to fit this fixture, so the result is a measurement and not a tuned score. Pages were not changed for it.

## 12. Output length and the two-places page (12 November 2026)

Question: are the audit reports token efficient? Before any change, the kept traces of `evals/seeded-audit-hard` (Sonnet, effort requested low) gave final reports of about 1,000 words in both arms (with skill 982, 1,043, 1,142; without 1,021, 953, 981), and one smoke run showed 1,342 against 890 words. The skill pages had no length or shape rule. Added: `tabby-review/two-places-agree.md` (a general page on checks and uses that disagree) and a "Report shape" paragraph in `security-audit/reporting.md`, designed from the caveman skills (answer first, no preamble or recap, each fact once, a floor that never drops negations, numbers or paths) and Tabby's own `report` levels. Words are counted from the last assistant message in kept traces; the token counts in the traces are not usable.

| Version of the pages | With skill: words per report | Defects (of 30) | Look-alikes ok (of 24) | Cost per run |
| --- | --- | --- | --- | --- |
| before | 982, 1043, 1142 (mean 1056) | 27 | 20 | $0.16 |
| report shape + two-places page | 1101, 1009, 1008 (mean 1039) | 28 | 20 | $0.17 |
| plus a 50-word cap per finding, no sub-bullets | 1088, 842, 1027 (mean 986) | 26 | 20 | $0.15 |

Reading: **the rules did not shorten the reports in any way that stands out from run-to-run spread** (a 2% and then a 7% drop, ranges of 150 to 250 words). The agent read the rule (the trace shows `reporting.md` loaded) and followed the verdict-first structure, but still wrote about 90 words per finding for 11 findings, plus a rejected list and a coverage block. Defects found were flat (27, 28, 26 of 30) and the missed ones moved between runs, so the new page did not measurably raise recall either; it was written after seeing the misses, so a gain would have been partly tuned anyway. Output words are also not what costs: the with-skill arm costs about 45% more than the bare arm because it reads more files (6 to 8 turns against 2), which a report-shape rule cannot change. The bare arm's reports are about as long (890 to 1,100 words) and, on this fixture, noisier (more look-alikes reported as findings).

Not tried, and where I would look next: a fixed fill-in template for each finding instead of a prose budget, or making `report: terse` the default for audits. Both change the format, so they need the owner's decision. n is 3 runs per arm, one model, effort unverified.

## 13. Sharpening the audit references, and a hold-out fixture (12 November 2026)

Why: in the nine with-skill runs of `seeded-audit-hard` so far, the agent opened `security-audit/process.md` in 6, `repo-audit.md` in 5, `reporting.md` in 2, and **never** any class page, `bug-hunt.md` or `two-places-agree.md`; so about 8,000 of the 14,000 words in `tabby-review` were not reaching an audit. Changes: the 50-word cap was reverted; `process.md` was cut from 1,842 to 1,188 words and gained a "Read next" table that maps what the code shows (`startswith`, a `user_id` copied into a queue, a flag read from the environment, `setattr` on request data, and so on) to the page to open, with the rule to open every page whose trigger appears and name it in the coverage line; the four class pages were trimmed by 7% to 22% (`defaults-and-config` 1,396 to 1,215, `identity-and-access` 1,159 to 968, `files-network-and-crypto` 915 to 804, `injection-and-output` 704 to 657); `SKILL.md` points the audit branch at the table. A second fixture, `seeded-audit-hard-b` (a clinic booking service, same ten defect families, different code), was written and run once on the old pages before any edit, and was not read while editing, so it is a hold-out.

Sonnet (`claude-sonnet-5-5`, effort requested low, unverified), 3 runs, plugin arm only for the new pages; the old-page figures are from the earlier runs (hard: three runs each of sections 11 and 12; hard-b: one run of 3).

| Fixture | Pages | Defects (of 30) | Look-alikes ok (of 24) | Words per report | Cost per run | Class pages opened |
| --- | --- | --- | --- | --- | --- | --- |
| hard (tuned on) | old (3 runs of sec. 11, 12 and 12b) | 29, 27, 28, 26 | 20 to 21 | about 1,000 | $0.16 to $0.17 | 0 of 9 |
| hard | sharpened | 29 | 21 | 1,043 (1,122, 917, 1,091) | $0.172 | 0 of 3 |
| hard-b (hold-out) | old | 27 | 17 | 1,095 (903, 1,147, 1,234) | $0.149 | not counted |
| hard-b | sharpened | 28 | 22 | 1,080 (1,031, 1,129, 1,079) | $0.165 | 0 of 3 |

Reading: the sharpened pages did **not** change what the agent reads: still no class page in any of the six runs, and the "Read next" table was not followed (`two-places-agree.md` was opened in 2 of 6 runs, `bug-hunt.md` in 1). Defects found are flat to slightly up (29 against 26 to 29 on the tuned fixture; 28 against 27 on the hold-out), look-alike precision is up on both (21 and 22 of 24 against 20 and 17), report length and cost did not move. With 3 runs per cell and the run-to-run spread seen above (a fixture swings by two or three defects between identical runs), none of these differences is established. The smaller front door may help the agent read less noise, but the evidence is that the lift of the skill over bare comes from loading it and `process.md` and from doing more reading, not from the class pages. The hold-out behaves like the tuned fixture, which is some evidence the lift is not specific to the fixture the pages were written beside.
