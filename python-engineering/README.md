# python-engineering

Part of the [skills monorepo](../README.md). Run the development commands from this folder.

Agent skills for developing Python code and packages, for Claude Code and GitHub Copilot, grouped into **bundles by the kind of Python work**. They make an AI agent write less slop: tests that can fail, errors that surface, fewer concepts, honest reports. The rules come from the *Python Engineering Rules for AI Agents* (v2).

The skills follow the open [Agent Skills](https://agentskills.io/specification) format, so one folder works in both tools. Each skill loads only when the request matches its description; reference files load only when the skill points at them. Bundles are how this repository is organised: an install is still a flat list of skill folders.

## Which kind of work is yours?

Ask the `python-project-facts` skill: it prints `kind=`, `kinds=`, `bundles=` and `bundles.missing=` for your project (`kind=<kind>` overrides the guess). Or pick from this table.

| You are building | Kind | Install these bundles |
| --- | --- | --- |
| A package others `pip install` | `library` | shared, core, library |
| A web API or service | `application` | shared, core, application |
| A one-off script | `script` | shared, core |

More bundles for other kinds of work (native extensions, data engineering, machine learning and others) are listed in the `BUNDLES` map of `python-project-facts` and are being added. `shared` is the `python-project-facts` skill that every other skill runs; `core` is for all Python code.

## Bundles

Body tokens are estimates (2.8 characters per token, measured against the Claude CLI's reported usage); run `uv run python scripts/check_skills.py .` for the current numbers.

| Bundle | Skill | Loads when you... | Body (est. tokens) |
| --- | --- | --- | --- |
| shared | `python-project-facts` | start any of the other skills: it detects the Python version, runner, tools and kind of project | 0.8k |
| core | `testing-python-packages` | add or fix tests, chase a flaky test, reproduce a bug, configure pytest | 1.7k |
| core | `writing-python-code` | write, change or debug Python source; also holds the end-of-task report | 3.3k |
| core | `reviewing-python-changes` | review a diff, or check your own work before saying done | 1.5k |
| core | `profiling-python-code` | chase slow code or high memory, or are about to swap in a faster library | 1.6k |
| core | `auditing-python-dependencies` | add a dependency, answer a security alert, or audit the supply chain | 1.6k |
| core | `avoiding-code-snags` | write or change Python code: a short list of watch-outs to follow as you go | 1.5k |
| core | `choosing-python-design-patterns` | are asked for a design pattern, a refactor that adds classes or layers, or an extension point | 1.7k |
| core | `writing-python-scripts-and-clis` | are asked for a script, a command-line tool or a one-off utility | 0.5k |
| library | `setting-up-python-packages` | create a package or change build, lint, type, dependency or CI config | 1.7k |
| library | `designing-package-apis` | add, rename or remove a public name, extra or exception | 2.0k |
| library | `releasing-python-packages` | prepare or cut a release, fix a wheel, edit publishing workflows | 1.5k |
| application | `building-python-web-services` | add endpoints, wire a database or auth, or deploy a Python web service | 1.6k |

What loads for each kind, at most (always-on descriptions plus every body, if every skill fires):

| Kind | Skills | Always-on descriptions (tokens) | All bodies (tokens) |
| --- | --- | --- | --- |
| library | 12 | about 1,170 | about 19,400 |
| application | 10 | about 1,000 | about 15,900 |
| script | 9 | about 880 | about 14,300 |

A skill names only skills of its own bundle, `core` and `shared`; to point at another bundle it says "the library bundle, if installed", and `check_skills.py` enforces this. The `application` bundle is the former `python-web` skillset, whose notes follow.

`building-python-web-services` covers Python web APIs and services: FastAPI first (the stack in [Mallard](https://github.com/RelativelyUnknown/Mallard)'s server), Django, Litestar and Flask where a project already uses them. Its body holds eight rules that apply to every change (boundary validation, explicit response models, per-object authorization, settings from the environment, no blocking calls in `async def`, shared clients, stable errors, four tests per endpoint). Detail lives in five references that load only when the task touches them: `fastapi.md`, `django.md`, `persistence.md` (SQLAlchemy 2.x, SQLModel, Alembic), `security.md` (OWASP API Security Top 10 (2023) checks, Argon2 via pwdlib, JWT validation, CORS, uploads, SSRF) and `deployment.md` (servers and workers, a uv-based Dockerfile, health checks, structured logs, OpenTelemetry). Faster drop-ins for web code (orjson, msgspec, uvloop, granian) are in `writing-python-code`'s `references/faster-libraries.md`, behind its profile-first rule.

## Install

Copy the bundle folders for your kind of work into your project (`shared` is always needed):

```bash
mkdir -p .claude/skills
cp -r /path/to/skills/python-engineering/{shared,core,library}/skills/* .claude/skills/          # a library
cp -r /path/to/skills/python-engineering/{shared,core,application}/skills/* .claude/skills/      # a web service
cp -r /path/to/skills/python-engineering/{shared,core}/skills/* .claude/skills/                  # a script
```

- `.claude/skills/` is the one project path both Claude Code and Copilot (VS Code agent mode, cloud agent, CLI) read. `.github/skills/` is Copilot only. Personal installs: `~/.claude/skills/` or `~/.copilot/skills/`.
- **Minimal profile:** `python-project-facts`, `testing-python-packages` and `writing-python-code` (three descriptions, about 260 tokens).
- Without `python-project-facts` the other skills still work: they tell you once that project facts are assumed and use defaults.

`writing-python-code` keeps its always-needed rules in `SKILL.md`. Topic rules live in `references/` and load only when the task touches them: Python versions, docstrings and comments, logging and security, complexity tools, standard library or package, and faster libraries. `profiling-python-code` owns the faster-libraries material: the gate (no swap without a measurement), `references/faster-libraries.md` (curated replacements with their evidence and when not to switch) and `references/finding-replacement-packages.md` (when a swap is worth it, how to find candidates online, and how to judge them from PyPI, deps.dev and OpenSSF Scorecard data). Each rule has one home: the other skills point to it instead of restating it.

Skills load when the model judges them relevant. The rules that must never be missed (verify before "done", never edit a contradicting test, root cause not symptoms, do not silence tools) live in `writing-python-code` and `testing-python-packages`. If you want them unconditional, copy those bullets into your `AGENTS.md`.

## Arguments and project detection

Every skill starts by running `detect_project.py` from the `python-project-facts` skill (Python 3.11+, standard library only; install that skill next to the others). It prints about 18 lines: the Python target from `requires-python`, the runner (uv, poetry, pdm, hatch, pip), layout, build backend, pytest import mode, type checker, linters, async plugin, CI system, and which declared tools are not installed. Anything it cannot find prints `# default`. Skills use the project's existing tools and never install anything silently.

Pass `key=value` words after the skill name to override what was detected: `/testing-python-packages python=3.10 rigor=ultra`. The same words in a plain request also work. Order: argument, then detected, then default.

| Key | Values | Default |
| --- | --- | --- |
| `python` | 3.10 and up | `requires-python` lower bound, else 3.12 |
| `runner` | `uv`, `pip`, `poetry`, `hatch`, `pdm` | detected, else `uv` |
| `types` | `mypy`, `pyright`, `basedpyright`, `ty`, `pyrefly` | detected, else `mypy` |
| `layout` | `src`, `flat` | detected, else `src` |
| `backend` | `hatchling`, `uv_build`, `setuptools`, `poetry-core`, `pdm-backend`, `flit-core`, `maturin` | detected, else `hatchling` |
| `rigor` (testing) | `lite`, `full`, `ultra` | `full` |
| `report` (writing, reviewing) | `terse`, `normal`, `audit` | `normal` |

`rigor=lite` keeps the test rules; `full` adds boundary mocking, strict config, coverage floor; `ultra` adds Hypothesis, mutation testing, a lowest-dependencies run and an installed-wheel test. `report=terse` is at most 10 lines; `audit` lists every shortcut, assumption and thing left alone.

Complexity tools (`xenon`, `radon`) are advice in these skills, never a score to reach at the cost of readable code.

## Evals

Test cases are in `<bundle>/skills/<skill>/evals/<case>/` (`prompt.md`, `case.yaml`, `graders/`, and `fixture.sh` where the case needs files), the layout `claude plugin eval` reads. There are twenty-four cases (twenty-three in `core` and `library`, one in `application`): two that came with the profiling and dependency skills; fourteen converted from earlier scenarios (thirteen where a run without the skill missed something in my first tests, and one guard, `do-not-over-engineer-orders`, that checks a skill does not push too far); three baseline cases for the package-versus-stdlib rule (`validate-one-function-stdlib`, `validate-with-existing-pydantic`, `hard-problem-take-a-library`); `write-small-service-module`, which checks that code written without prompting avoids the common snags; `dedupe-lines-script` for the scripts skill, and two for the facts dependency (`facts-missing-warns`, `facts-present-silent`; they need a Bash sandbox, so they were smoke-tested by hand). Some cases may show no difference between the arms; that is a result to act on, not a pass. Trigger checks (prompts that should and should not load each skill) are in `evals/<skill>.triggers.json`.

Each case runs three times with the skill and three without; the difference is what the skill contributes. A skill with no difference should be cut or rewritten.

```bash
# from this folder; one skill, or add --case <name> for one case
claude plugin eval core/skills/avoiding-code-snags --scaffold \
  --allow-tools Write Edit "Bash(pytest *)" "Bash(git *)" \
  --judge-model sonnet --max-cost-usd 10
```

- `--scaffold` runs each case's `fixture.sh` (plain bash that writes the fixture files and a git history); read it first, it runs as you.
- Cases that run tests call whatever `pytest` is on your `PATH`. Granting `Bash` needs an OS sandbox (on Linux, `bubblewrap` and `socat`); without one the run refuses.
- `find-faster-json-library` also needs `--allow-tools "WebFetch(domain:pypi.org)" "WebFetch(domain:api.deps.dev)"` and the other package-health hosts it names.
- `claude plugin eval <skill folder>` loads that one skill, so `python-project-facts` is not installed in the run and the agent warns that project facts are assumed. Running a case with the facts skill present needs the facts skill in the same plugin; this is untested.
- A `tool_used: Skill` grader in every case shows whether the skill fired on a plain request. It is an indicator and is not scored.
- Results go to `evals/results/` (ignored by git). Every run is a real model call on your account.

## Known interactions

- A hook that blocks all edits under `tests/` and `conftest.py` also blocks adding new tests. Allow new test files, or set the hook's override for test-writing sessions.
- Each skill's `argument-hint` line is outside the open spec (Claude Code and VS Code Copilot use it for autocomplete). Delete that line before uploading a skill to claude.ai or the Skills API, which reject unknown keys.
- `detect_project.py` lives in one place, `shared/skills/python-project-facts/scripts/`, and the other skills run it from there (their `compatibility` field says so). If that skill is not installed they tell you once and continue with defaults. `check_skills.py` fails a skill that carries its own copy.

## Try it in your tool

Claude Code: ask `add a regression test for the bug in <file>` and check that the agent writes the failing test before the fix. Then `/testing-python-packages rigor=lite fix the flaky test in tests/test_x.py`.

Copilot (VS Code agent mode or cloud agent): run `/skills` to confirm the skills you installed are listed, then ask the same two prompts. Copilot does not guarantee that it picks a skill, so test both the slash command and the plain request. This repo was not tested in Copilot.

## Develop

```bash
uv sync
uv run pytest                        # tests for the scripts
uv run ruff check scripts tests && uv run mypy scripts tests
uv run python scripts/check_skills.py .   # spec, budget and bundle checks for every bundle
uv run python scripts/check_skills.py --argument-keys scene,fps ../other/skills   # other skillsets; empty value accepts any key
```

## License

MIT.
