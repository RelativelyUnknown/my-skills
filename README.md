<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/cat-head-dark.png">
    <img src="assets/cat-head-light.png" width="150" alt="The Tabby logo: a painted tabby cat's head, orange in light mode and grey in dark mode.">
  </picture>
</p>

# Tabby

Tabby is a set of six agent skills for Python projects, and for the Rust, C, C++ and Zig code behind a Python API. It works in OpenCode, GitHub Copilot and Claude Code. It makes the agent find the cause before the fix, reuse before it writes, keep the diff small, and never edit a test to get green.

![6 skills](https://img.shields.io/badge/skills-6-2a8f89?style=flat-square)
![OpenCode, Copilot, Claude Code](https://img.shields.io/badge/works%20in-OpenCode%20%7C%20Copilot%20%7C%20Claude%20Code-2a8f89?style=flat-square)
![MIT licence](https://img.shields.io/badge/license-MIT-2a8f89?style=flat-square)

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/cat-sleeping-dark.png">
    <img src="assets/cat-sleeping-light.png" width="560" alt="A tabby cat asleep in a curl, painted in brushstrokes: orange in light mode and grey in dark mode.">
  </picture>
</p>

## Install

Tabby is plain `SKILL.md` folders in the open [Agent Skills](https://agentskills.io/specification) format, so one copy of each folder works in all three tools. Pick your tool:

**Claude Code.** Run these as two separate prompts:

```
/plugin marketplace add RelativelyUnknown/my-skills
```

```
/plugin install tabby@tabby
```

On Claude Code 2.1.275 or later, one command does both: `/plugin install tabby --marketplace RelativelyUnknown/my-skills`.

**OpenCode and GitHub Copilot.** Clone the repository and copy the skills into your project:

```
git clone https://github.com/RelativelyUnknown/my-skills
cd your-project
python3 ../my-skills/tools/install.py agents
```

`agents` installs to `.agents/skills/`, which both tools read. Add `--user` to install for every project (`~/.agents/skills/`). Other targets: `github` (`.github/skills/`, Copilot), `opencode` (`.opencode/skills/`), `claude` (`.claude/skills/`, read by all three). The installer never deletes anything and skips folders that already exist unless you pass `--force`.

Install Tabby only from `RelativelyUnknown/my-skills` on GitHub.

| | Claude Code | OpenCode | GitHub Copilot |
| --- | --- | --- | --- |
| Skills load when the request matches | yes | yes | yes |
| Run the interview | `/tabby:interview` | `@interview` | `/interview` |
| Project memory file | `CLAUDE.md` containing `@AGENTS.md` | `AGENTS.md` | `AGENTS.md` or `.github/copilot-instructions.md` |
| Reminder before each prompt | optional hook (`hooks` skill) | paste [`remind.txt`](hooks/remind.txt) into `AGENTS.md` | paste [`remind.txt`](hooks/remind.txt) into `.github/copilot-instructions.md` |

## Example

Give the agent this bug report:

```
Bug report: `apply_discount(19.99, 15)` returns 16.9915 but the docstring says results are rounded to cents, half up. Fix it.
```

With Tabby, the agent writes a test that asserts 16.99, runs it and sees it fail, fixes the rounding, runs the whole suite, and leaves the existing tests alone. The eval case `evals/bug-fix-starts-red` checks each of those steps. To run it (needs the `claude` CLI; it costs a few cents):

```
python3 tools/eval/run.py --out results --cases bug-fix-starts-red --plugin . --plugin-dir . --model claude-haiku-5-5 --runs 3
python3 tools/eval/summarise.py results
```

## The six skills

The harness keeps the six descriptions in context (about 2,400 characters, roughly 600 tokens). When a task matches one, it loads that skill's body and only the files the body names for that task. The skills point at each other by relative path, so keep the folders side by side.

| Skill | The agent loads it when you | What it adds |
| --- | --- | --- |
| [`tabby`](tabby/) | write, fix, test, speed up, package or release Python, or the Rust, C, C++ or Zig behind it | Rules the agent never skips, and files on errors, typing, dependencies and uv, CI, performance, libraries, services, design, and native layouts, PyO3, the C API and wheels |
| [`tabby-review`](tabby-review/) | ask for a review of a diff or pull request, a repository audit or a security audit | Self-review, a security audit that separates confirmed bugs from look-alikes, and a checklist for the Python and native boundary |
| [`tabby-docs`](tabby-docs/) | write a README, docstrings, a tutorial, a changelog, an ADR or a runbook | One page type per reader need, and a check of the docs against the code |
| [`tabby-diagrams`](tabby-diagrams/) | ask for a diagram, an architecture picture or an animation | A builder that turns a small spec into an SVG or an HTML animation, and checkers for crowded labels, contrast and loop jumps |
| [`tabby-frontend`](tabby-frontend/) | build a page, dashboard, data app or docs site | A method, design tokens, a list of things it refuses to ship, and `ui-check` for contrast, focus, motion and layout |
| [`interview`](interview/) | run `/tabby:interview` | Researches the repository read-only, asks at most three questions a round, and saves a `## Tabby` section to `AGENTS.md` |

Skills load more reliably with a short reminder before each prompt. In Claude Code an optional hook in [`hooks/`](hooks/) prints it, and it is off by default; in the other tools the reminder lives in the instructions file (see the table above).

## The rules it holds

- Done means the real problem is solved and verified by running the code. Passing tests are evidence, not the goal.
- It never edits, deletes, skips or loosens an existing test to get green.
- It finds the cause before the fix. No special-casing inputs, no sleeps or retries to hide a symptom.
- It does not silence tools (`# type: ignore`, `# noqa`, `Any`, looser config).
- It keeps the diff small. It adds no dependency, changes no public API and makes no commit or push unless you ask.
- It uses your project's own tools, and reuses in this order: your project, the standard library, the community's standard library, then code you write yourself.

## Project memory

Tabby does the task first and never interviews you before it. Project memory lives in `AGENTS.md` for every tool. It infers the project from the repository and your request, and marks guesses `(assumed)`. `/tabby:interview` saves what the project is for and where it is going to a `## Tabby` section in `AGENTS.md`; later tasks read that section and ask before contradicting it. Tool and style defaults live in a `## Python defaults` section. Both are plain text you can edit.

## Measured effect

The same agent with and without Tabby on Claude Haiku 5.5, 98 eval cases, 3 runs each (`claude plugin eval`, regex and model-judged graders), 13 November 2026.

| | Without Tabby | With Tabby |
| --- | --- | --- |
| Mean score | 0.775 | 0.832 |
| Turns per run | 11.4 | 14.8 |
| Cost per run | $0.0131 | $0.0152 |

Tabby scored higher on 23 cases, lower on 11 and the same on 64.

### What each case tests

Each case in [`evals/`](evals/) gives the agent a task in a small fixture repository and grades the result.

| Case | Tests |
| --- | --- |
| `add-owned-resource-endpoint` | An endpoint for user-owned data filters by owner, hides internal fields and tests the other-user case |
| `adr-runbook-troubleshooting` | An ADR, a runbook and a troubleshooting page, each with the sections its reader needs |
| `agents-md-for-a-repo` | A short AGENTS.md with the check command, the regenerate command and the Python defaults, and no generic advice |
| `animation-self-contained-html` | One self-contained HTML animation of a webhook flow, with a static end state and reduced-motion handling |
| `api-on-plain-sql-growth-known` | An API on plain SQL whose design choices are grounded in the saved growth and workload |
| `api-on-plain-sql-growth-unknown` | The same API with no saved section: it still builds, and asks the questions that would change the design |
| `audit-ci-workflow` | A CI audit that finds the two real workflow vulnerabilities and does not flag the two look-alikes |
| `audit-repo-bloat-and-load` | An audit that finds a query-per-item loop, a race and untested arithmetic, and changes nothing |
| `batches-and-utc` | Standard library `batched` and `fromisoformat` instead of regexes and helper wrappers |
| `bounded-fan-out-with-deadline` | Concurrent calls with a concurrency cap, ordered results and one deadline |
| `bug-fix-starts-red` | A failing test first, then the fix, then the whole suite, with no existing assertion weakened |
| `ci-job-for-a-uv-project` | A CI job using `uv sync --locked` |
| `clean-diff-no-noise` | A clean diff gets a short "no findings" verdict, not speculative observations |
| `clean-up-ingest-module` | A small clean-up that keeps three deliberate choices and creates no new files |
| `clear-ask-no-interview` | A clear request is done without a first question or an unasked `## Tabby` section |
| `cli-to-team-tool` | A personal script made usable by others: paths, entry point, errors, install notes |
| `community-standard-over-handrolled` | The standard HTTP library for timeouts and retries instead of a hand-rolled loop |
| `confine-unsafe-accessor` | A narrowly scoped `unsafe fn` with a documented safety precondition |
| `contradicting-test-left-alone` | A test that contradicts the docstring is left alone and the contradiction is reported |
| `cpp-binding-return-policy` | A C++ binding with a correct return value policy, bounds checking and no leak warnings switched off |
| `de-rerunnable-load` | A nightly load that can be re-run for a day and backfilled without duplicating rows |
| `debug-order-dependent-test` | Finding a mutated module-level default as the cause of an order-dependent test |
| `dedupe-lines-script` | A CLI script with `main(argv)`, `--dry-run`, errors on stderr and an atomic rewrite |
| `deprecate-instead-of-delete` | A public function kept as a warning alias, with a changelog entry, when asked to remove it |
| `dev-tool-and-script-dependency` | Dev tools in the dev group and a one-off script dependency in inline metadata |
| `diagram-honours-design-md` | An SVG and an animated HTML diagram that follow the project's `design.md` |
| `diagram-of-a-small-service` | An architecture SVG containing only components that exist in the repository |
| `diagram-state-machine` | A state diagram showing exactly the transitions the code allows |
| `do-not-over-engineer-orders` | No abstract classes or patterns where a pure function and function arguments do |
| `docs-site-brand-and-dark-mode` | A docs site with a light and dark switch and the brand colour |
| `ecosystem-fit-ordering` | `graphlib` for dependency ordering, with clear cycle errors |
| `ecosystem-fit-shell-words` | `shlex` for shell-style splitting instead of a regex |
| `enqueue-after-commit` | A job enqueued only after the transaction commits |
| `exhaustive-event-handling` | Typing that makes a new event kind a type error |
| `existing-project-first-round` | On an existing project, at most three researched questions with recommended answers and no files written |
| `fake-needs-contract-test` | An in-memory fake plus a contract test that runs against the fake and the real client |
| `find-faster-json-library` | Measuring, then recommending and vetting a faster library without migrating |
| `first-endpoint-from-a-library` | A thin first endpoint over an existing function, with no speculative layers |
| `fix-ssrf-in-link-preview` | An SSRF fix that checks resolved addresses and redirects instead of a string blocklist |
| `footprint-of-a-similar-change` | A new flag touches every place the previous flag touched |
| `fresh-project-open-request` | An open request in an empty repo gets a minimal start or at most three questions |
| `gates-multipart-missed-requirement` | A cross-cutting requirement applied to all four call sites |
| `gates-trivial-no-ceremony` | A one-word typo fix with no checklist or ceremony |
| `hard-problem-take-a-library` | A maintained library for date parsing instead of a hand-written parser |
| `import-rows-some-fail` | Every row attempted, failures collected and reported together |
| `interview-saves-after-yes` | The `## Tabby` section is saved only after an explicit yes |
| `interview-vague-yes-does-not-save` | A vague "whatever you think" is not treated as a yes |
| `join-existing-native-library` | Joining a native-library repo: read first, then save a short section with guesses marked assumed |
| `learned-something-offers-a-note` | A discovered project rule is followed and offered as a note, not written unasked |
| `literal-defaults-fetch-json` | Literal parameter defaults instead of `DEFAULT_` constants |
| `load-settings-house-rules` | A TOML settings loader with validation, literal defaults and tests |
| `local-development-env-file` | A committed `.env.example`, an ignored `.env` and no real-looking secrets |
| `ml-leaky-validation` | Fixing train/validation leakage: pipeline fit, time-ordered split, grouped stores |
| `native-free-threaded` | A PyO3 module declaring free-threaded support |
| `native-gil-checksum` | A PyO3 function releasing the interpreter lock with current API, no panics, a stub entry and a test |
| `native-pyclass-by-value` | A PyO3 0.30 function taking a class by value or by reference correctly |
| `new-package-one-check-command` | A new package with strict tooling and one command that runs every check |
| `niche-library-or-five-lines` | A few lines of standard library instead of a niche package |
| `numpydoc-docstrings` | A numpydoc docstring with the required sections |
| `one-settings-object` | A frozen settings object built at the program edge instead of a singleton |
| `optional-parquet-dependency` | An optional extra imported lazily with a clear error when missing |
| `payment-strategy` | A dict of functions instead of a strategy class hierarchy |
| `pick-a-set-representation` | A bitset in place of a hash set of flags, sized from the enum and tested for every variant |
| `pip-requirements-project-keeps-its-tools` | A pip and tox project keeps its tools when a dependency is added |
| `poetry-black-unittest-keeps-its-tools` | A poetry, black and unittest project keeps its stack |
| `port-hot-path-to-rust` | A hot path ported to Rust with identical behaviour, a stub and a Python reference |
| `readme-for-small-package` | A landing-page README with one install command and a runnable example |
| `real-own-code-stubbed-edge` | Real own code in tests, with only the external payment call stubbed |
| `repo-text-addressed-to-the-agent` | Instructions found in repository text are reported, not obeyed |
| `request-id-on-every-log-line` | A request id on every log line through a context variable and a filter |
| `request-metrics-bounded-labels` | Metrics labelled by route template, never the raw path |
| `retry-a-flaky-http-call` | A bounded retry with jitter for transient errors only, tested without sleeping |
| `review-a-page-before-shipping` | A page review with located problems and fixes, without editing the page |
| `review-pyo3-diff` | A review of a Rust change that finds a reachable panic and a silent truncation |
| `saved-section-conflicts-with-task` | A task that contradicts the saved section is flagged before any code changes |
| `scout-reports-what-it-noticed` | Problems noticed beside a small change are reported, not rewritten |
| `seeded-audit` | A security report of three real vulnerabilities, excluding three look-alikes |
| `seeded-audit-hard` | Ten defects that need several files read together, excluding eight look-alikes |
| `seeded-audit-hard-b` | A second set of ten multi-file defects, excluding eight look-alikes |
| `seeded-audit-python` | Twelve planted Python defects, excluding eight look-alikes |
| `settings-loaded-at-startup` | A frozen config built at startup with all errors reported together and secrets hidden |
| `single-source-version` | A version bumped in one place, a changelog entry and a smoke-tested wheel, with no tag or publish |
| `speed-up-matcher` | A baseline, a set-based fix and before/after numbers |
| `stop-calling-a-failing-dependency` | A circuit breaker with an injectable clock |
| `stop-early-from-an-async-generator` | Early exit from an async generator with guaranteed cleanup |
| `stream-command-output-with-limit` | Line-by-line command output with a deadline and a killed, reaped child |
| `three-pages` | A tutorial, a how-to and a reference page, each written to its type |
| `timeout-is-not-the-fix` | Finding a per-customer query loop behind a request to raise a timeout |
| `tiny-fix-stays-tiny` | A one-line typo fix with no refactor and a short reply |
| `typed-decorator-keeps-signature` | A retry decorator typed with `ParamSpec` |
| `ui-orders-page-accessibility` | Accessibility fixes: language, labels, alt text, headings, focus, contrast |
| `vague-ask-clarifies-briefly` | A vague request gets one to three questions and no edits |
| `vague-feature-gets-a-short-spec` | A short spec and a first slice for a feature with several readings |
| `vague-request-larger-repo` | Finding a CSV quoting bug from a vague report and fixing it with the `csv` module |
| `validate-one-function-stdlib` | Plain `raise ValueError` checks, with no dependency or model class |
| `validate-with-existing-pydantic` | The project's existing pydantic used for validation |
| `vet-before-adding` | Checking that a package really exists before adding it |
| `welcome-email-exactly-once` | An atomic claim so a double delivery sends one email |
| `write-small-service-module` | Common smells avoided unprompted: encoding, timeouts, time zones, broad `except` |
| `zig-extension-review` | A Zig function added following the project's existing extension pattern |

Limits: measured on Claude Code only. The skills follow the same standard in OpenCode and Copilot, but those tools differ in how they load skills, in tool names and in permission prompts, and the evals have not been run there. One model family, three runs per case, and cases written by the same author as the skills, so the gain is likely overstated. A difference under about 0.3 on one case is noise. Large repositories and multi-turn work are not measured. The cases are in [`evals/`](evals/) and the runner is in [`tools/eval/`](tools/eval/).

## Links

- [`evals/`](evals/): the eval cases, trigger sets and seeded-audit fixtures
- [`tools/eval/`](tools/eval/): the runner, summaries, trace reader, quality, smell and judge tools
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md): ideas adapted from other projects, with sources and licences
- [Issues](https://github.com/RelativelyUnknown/my-skills/issues)

## License

MIT. Fonts, icons and adapted material are credited in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
