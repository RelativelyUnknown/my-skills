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

All runs: Haiku 5.5 as agent and as judge, 3 runs per case and arm, `claude plugin eval --ablation with-without`. Scores are weighted pass rates of the scored graders. With three runs, a difference under about 0.15 on one case is noise: several cases swing by 0.5 or more between runs of the same arm.

| Run | Commit | Tools granted | Router description | With | Without | Outcome cases (57) | Protocol cases (3) | Router loaded | Cost per run | Turns |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | `f1fd402` | Write, Edit | as before the audit | 0.84 | 0.80 | 0.86 / 0.82 | 0.47 / 0.32 | 114 of 180 | $0.014 / $0.011 | 14.6 / 8.9 |
| B | `73752e0` | Write, Edit, Bash, WebFetch | my first rewrite | 0.82 | 0.82 | 0.84 / 0.84 | 0.59 / 0.44 | 49 of 180 | $0.015 / $0.014 | 13.3 / 10.5 |

Run A scores exclude nothing, but about 20 graders that need a shell could not pass in either arm. Run B has a real shell (`bubblewrap` and `socat` were installed in the session), so every grader can pass.

**What the two runs show**

1. **Loading is the lever, and my first description rewrite broke it.** Run A showed the router never loading on review, audit, documentation, diagram and onboarding requests, so I rewrote the description to name them. In run B it then loaded in 49 of 180 runs instead of 114, and the overall difference vanished. A spot check with a shell confirmed the cause: the old wording loaded in 8 of 8 code cases where the rewrite had loaded in 0 of 24. The description now committed keeps the old opening and adds the other tasks; on a 14-case spot check it loaded on all 6 code cases, on the diagram case and on the joining case, and still not on the 6 review, audit and documentation cases. **It has not had a full run.**
2. **Where the router loads, Tabby helps on its house rules and on the guard cases**: take a library for free-form dates (0.63 against 0.20 in A, 0.83 against 0.33 in B), literal defaults (1.00 against 0.38 in A), a dict of functions instead of a class hierarchy (1.00 against 0.40 in A), leaving a contradicting test alone (1.00 against 0.60 in A), script conventions (1.00 against 0.69 in A).
3. **On about half the cases there is nothing to gain**: the bare agent scores 1.00 on some 20 cases and both arms tie on 29 to 33. These cases cannot show a lift on this model.
4. **One large regression, in both runs**: `new-package-one-check-command` (0.14 against 0.83 in A, 0.36 against 0.98 in B). Asked to set up a named library with tests, linting and one check command, the agent with Tabby runs the interview and builds nothing; the eval has no user to answer. This is the designed behaviour ("write no code until the user answers") meeting a request that already says what to build. It is the open decision in this audit: see below.
5. **The README's earlier headline numbers do not hold.** "Joining an existing Rust-backed library: 1.00 with, 0.11 without" is 0.33 against 0.33 in A and 0.61 against 0.50 in B once the graders that match Tabby's own section names are no longer scored. The date-parsing, payment and literal-defaults lifts are confirmed in run A.
6. **The leaves added in this audit show no measured lift.** C++ return policy 0.93 against 0.90, CI workflow audit 0.90 against 0.95, vague bug report 1.00 against 1.00, tiny fix 1.00 against 1.00 (run B). The diagram case is 0.98 against 0.67 with the router loading in 2 of 3 runs. By the repository's own rule (build only where the bare model fails) the C++, supply-chain, commit and drift leaves are unproven on Haiku; they were built because the mission names those areas, not because a baseline failed.
7. **Tabby costs more**: about 10 to 25 percent per run and 3 to 6 more turns, because it reads before it writes.

**Run B, per case** (sorted by difference; "Loaded" is how many of the three with-runs invoked the skill)

| Case | With | Without | Delta | Spread (with) | Loaded |
| --- | --- | --- | --- | --- | --- |
| `hard-problem-take-a-library` | 0.83 | 0.33 | +0.50 | 0.30 | 3/3 |
| `diagram-of-a-small-service` | 0.98 | 0.67 | +0.31 | 0.07 | 2/3 |
| `literal-defaults-fetch-json` | 0.63 | 0.41 | +0.22 | 0.56 | 1/3 |
| `load-settings-house-rules` | 0.98 | 0.79 | +0.19 | 0.07 | 3/3 |
| `existing-project-first-round` | 0.72 | 0.54 | +0.18 | 0.46 | 2/3 |
| `clean-diff-no-noise` | 0.61 | 0.44 | +0.17 | 0.17 | 0/3 |
| `dedupe-lines-script` | 0.92 | 0.77 | +0.15 | 0.23 | 2/3 |
| `fresh-project-asks-first` | 0.43 | 0.29 | +0.14 | 0.43 | 3/3 |
| `payment-strategy` | 0.58 | 0.45 | +0.12 | 0.36 | 0/3 |
| `join-existing-native-library` | 0.61 | 0.50 | +0.11 | 0.42 | 2/3 |
| `pick-a-set-representation` | 0.89 | 0.78 | +0.11 | 0.17 | 1/3 |
| `native-pyclass-by-value` | 1.00 | 0.90 | +0.10 | 0.00 | 0/3 |
| `request-metrics-bounded-labels` | 0.95 | 0.86 | +0.10 | 0.14 | 2/3 |
| `optional-parquet-dependency` | 0.61 | 0.53 | +0.08 | 0.67 | 1/3 |
| `bug-fix-starts-red` | 0.46 | 0.38 | +0.08 | 0.12 | 0/3 |
| `bounded-fan-out-with-deadline` | 1.00 | 0.93 | +0.07 | 0.00 | 0/3 |
| `clean-up-ingest-module` | 0.60 | 0.53 | +0.07 | 0.20 | 1/3 |
| `settings-loaded-at-startup` | 0.91 | 0.85 | +0.06 | 0.00 | 0/3 |
| `native-gil-checksum` | 0.88 | 0.82 | +0.06 | 0.18 | 0/3 |
| `cpp-binding-return-policy` | 0.93 | 0.90 | +0.03 | 0.10 | 0/3 |
| `retry-a-flaky-http-call` | 0.94 | 0.91 | +0.03 | 0.09 | 2/3 |
| `single-source-version` | 0.67 | 0.64 | +0.03 | 0.08 | 0/3 |
| `validate-one-function-stdlib` | 0.95 | 0.92 | +0.03 | 0.08 | 0/3 |
| `add-owned-resource-endpoint` | 1.00 | 1.00 | +0.00 | 0.00 | 0/3 |
| `agents-md-for-a-repo` | 1.00 | 1.00 | +0.00 | 0.00 | 0/3 |
| `batches-and-utc` | 0.71 | 0.71 | +0.00 | 0.00 | 0/3 |
| `de-rerunnable-load` | 1.00 | 1.00 | +0.00 | 0.00 | 0/3 |
| `do-not-over-engineer-orders` | 1.00 | 1.00 | +0.00 | 0.00 | 1/3 |
| `enqueue-after-commit` | 1.00 | 1.00 | +0.00 | 0.00 | 0/3 |
| `exhaustive-event-handling` | 1.00 | 1.00 | +0.00 | 0.00 | 3/3 |
| `find-faster-json-library` | 0.55 | 0.55 | +0.00 | 0.00 | 0/3 |
| `local-development-env-file` | 1.00 | 1.00 | +0.00 | 0.00 | 0/3 |
| `ml-leaky-validation` | 1.00 | 1.00 | +0.00 | 0.00 | 0/3 |
| `native-free-threaded` | 1.00 | 1.00 | +0.00 | 0.00 | 0/3 |
| `one-settings-object` | 0.44 | 0.44 | +0.00 | 0.00 | 0/3 |
| `readme-for-small-package` | 1.00 | 1.00 | +0.00 | 0.00 | 3/3 |
| `seeded-audit` | 0.86 | 0.86 | +0.00 | 0.05 | 0/3 |
| `speed-up-matcher` | 0.42 | 0.42 | +0.00 | 0.50 | 0/3 |
| `stop-calling-a-failing-dependency` | 1.00 | 1.00 | +0.00 | 0.00 | 0/3 |
| `stop-early-from-an-async-generator` | 1.00 | 1.00 | +0.00 | 0.00 | 0/3 |
| `tiny-fix-stays-tiny` | 1.00 | 1.00 | +0.00 | 0.00 | 0/3 |
| `typed-decorator-keeps-signature` | 1.00 | 1.00 | +0.00 | 0.00 | 2/3 |
| `vague-request-larger-repo` | 1.00 | 1.00 | +0.00 | 0.00 | 0/3 |
| `validate-with-existing-pydantic` | 1.00 | 1.00 | +0.00 | 0.00 | 0/3 |
| `welcome-email-exactly-once` | 1.00 | 1.00 | +0.00 | 0.00 | 0/3 |
| `zig-extension-review` | 1.00 | 1.00 | +0.00 | 0.00 | 1/3 |
| `three-pages` | 0.85 | 0.86 | -0.02 | 0.14 | 0/3 |
| `contradicting-test-left-alone` | 0.67 | 0.70 | -0.03 | 0.09 | 0/3 |
| `audit-ci-workflow` | 0.90 | 0.95 | -0.05 | 0.15 | 0/3 |
| `request-id-on-every-log-line` | 0.85 | 0.93 | -0.07 | 0.22 | 3/3 |
| `confine-unsafe-accessor` | 0.70 | 0.80 | -0.10 | 0.30 | 0/3 |
| `numpydoc-docstrings` | 0.89 | 1.00 | -0.11 | 0.33 | 0/3 |
| `vet-before-adding` | 0.67 | 0.78 | -0.11 | 0.00 | 0/3 |
| `ci-job-for-a-uv-project` | 0.88 | 1.00 | -0.12 | 0.38 | 0/3 |
| `stream-command-output-with-limit` | 0.83 | 1.00 | -0.17 | 0.50 | 3/3 |
| `dev-tool-and-script-dependency` | 0.79 | 1.00 | -0.21 | 0.62 | 2/3 |
| `adr-runbook-troubleshooting` | 0.67 | 0.88 | -0.22 | 1.00 | 0/3 |
| `write-small-service-module` | 0.61 | 0.91 | -0.30 | 0.91 | 3/3 |
| `import-rows-some-fail` | 0.67 | 1.00 | -0.33 | 1.00 | 0/3 |
| `new-package-one-check-command` | 0.36 | 0.98 | -0.62 | 0.67 | 3/3 |

**Open decision: the interview against a request that already specifies the work.** Options: (a) keep it, and accept that a fully specified "set up X" stalls until answered; (b) let the agent build what the request names and ask round one alongside, writing the memory section only after a yes; (c) skip the interview when the request states purpose, kind and what to set up. I recommend (b): it keeps the interview and the no-memory-before-yes rule and removes the stall. I did not change it, because "ask before building" is a decision you made.

**Not done**
- A full run on the description now committed. The spot check says it loads on code tasks again; the numbers above are not its numbers.
- Getting the router to load on review, audit and documentation requests. Three wordings were tried; none loaded there.
- Cases in a large or messy repository, multi-turn cases, a second model, a different judge.

Spend on measurement in this session: about $13 (run A $4.46, a stopped run about $2, run B $5.27, trials and spot checks about $1).
