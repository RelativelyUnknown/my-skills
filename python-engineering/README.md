# python-engineering

Part of the [skills monorepo](../README.md). Run the development commands from this folder.

Eleven agent skills for developing Python packages and writing Python code, for Claude Code and GitHub Copilot. They make an AI agent write less slop: tests that can fail, errors that surface, fewer concepts, honest reports. The rules come from the *Python Engineering Rules for AI Agents* (v2).

The skills follow the open [Agent Skills](https://agentskills.io/specification) format, so one folder works in both tools. Each skill loads only when the request matches its description; reference files load only when the skill points at them.

## Skills

| Skill | Loads when you... | Body (est. tokens) |
| --- | --- | --- |
| `testing-python-packages` | add or fix tests, chase a flaky test, reproduce a bug, configure pytest | 1.2k |
| `writing-python-code` | write, change or debug Python source; also holds the end-of-task report | 2.3k |
| `setting-up-python-packages` | create a package or change build, lint, type, dependency or CI config | 1.1k |
| `designing-package-apis` | add, rename or remove a public name, extra or exception | 1.3k |
| `releasing-python-packages` | prepare or cut a release, fix a wheel, edit publishing workflows | 1.0k |
| `reviewing-python-changes` | review a diff, or check your own work before saying done | 1.0k |
| `profiling-python-code` | chase slow code or high memory, or are about to swap in a faster library | 1.1k |
| `auditing-python-dependencies` | add a dependency, answer a security alert, or audit the supply chain | 1.1k |
| `avoiding-code-snags` | review a file or module for problems, clean up a file, or check your own diff before saying done | 1.8k |
| `choosing-python-design-patterns` | are asked for a design pattern, a refactor that adds classes or layers, or an extension point | 1.1k |
| `writing-python-scripts-and-clis` | are asked for a script, a command-line tool or a one-off utility | 0.4k |

Always-on cost is the eleven descriptions: about 800 tokens. Run `uv run python scripts/check_skills.py` for the current numbers.

## Install

Copy the folders you want from this folder's `skills/` into your project:

```bash
mkdir -p .claude/skills && cp -r /path/to/skills/python-engineering/skills/* .claude/skills/
```

- `.claude/skills/` is the one project path both Claude Code and Copilot (VS Code agent mode, cloud agent, CLI) read. `.github/skills/` is Copilot only. Personal installs: `~/.claude/skills/` or `~/.copilot/skills/`.
- **Minimal profile:** copy only `testing-python-packages` and `writing-python-code` (two descriptions, about 130 tokens). **Full profile:** all eleven.
- Each skill folder is self-contained, so any subset works.

`writing-python-code` keeps its always-needed rules in `SKILL.md`. Topic rules live in `references/` and load only when the task touches them: Python versions, docstrings and comments, logging and security, complexity tools, standard library or package, and faster libraries. `profiling-python-code` owns the faster-libraries material: the gate (no swap without a measurement), `references/faster-libraries.md` (curated replacements with their evidence and when not to switch) and `references/finding-replacement-packages.md` (when a swap is worth it, how to find candidates online, and how to judge them from PyPI, deps.dev and OpenSSF Scorecard data). Each rule has one home: the other skills point to it instead of restating it.

Skills load when the model judges them relevant. The rules that must never be missed (verify before "done", never edit a contradicting test, root cause not symptoms, do not silence tools) live in `writing-python-code` and `testing-python-packages`. If you want them unconditional, copy those bullets into your `AGENTS.md`.

## Arguments and project detection

Every skill starts by running `scripts/detect_project.py` (Python 3.11+, standard library only). It prints about 14 lines: the Python target from `requires-python`, the runner (uv, poetry, pdm, hatch, pip), layout, build backend, pytest import mode, type checker, linters, async plugin, CI system, and which declared tools are not installed. Anything it cannot find prints `# default`. Skills use the project's existing tools and never install anything silently.

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

Test cases are in `skills/<skill>/evals/<case>/` (`prompt.md`, `case.yaml`, `graders/`, and `fixture.sh` where the case needs files), the layout `claude plugin eval` reads. There are twenty-two cases: two that came with the profiling and dependency skills; sixteen converted from earlier scenarios (fifteen where a run without the skill missed something in my first tests, and one guard, `do-not-over-engineer-orders`, that checks a skill does not push too far); and four baseline cases for the package-versus-stdlib rule and candidate snags (`validate-one-function-stdlib`, `validate-with-existing-pydantic`, `hard-problem-take-a-library`, `review-new-snag-candidates`). Some cases may show no difference between the arms; that is a result to act on, not a pass. Trigger checks (prompts that should and should not load each skill) are in `evals/<skill>.triggers.json`.

Each case runs three times with the skill and three without; the difference is what the skill contributes. A skill with no difference should be cut or rewritten.

```bash
# from this folder; one skill, or add --case <name> for one case
claude plugin eval skills/avoiding-code-snags --scaffold \
  --allow-tools Write Edit "Bash(pytest *)" "Bash(git *)" \
  --judge-model sonnet --max-cost-usd 10
```

- `--scaffold` runs each case's `fixture.sh` (plain bash that writes the fixture files and a git history); read it first, it runs as you.
- Cases that run tests call whatever `pytest` is on your `PATH`. Granting `Bash` needs an OS sandbox (on Linux, `bubblewrap` and `socat`); without one the run refuses.
- `find-faster-json-library` also needs `--allow-tools "WebFetch(domain:pypi.org)" "WebFetch(domain:api.deps.dev)"` and the other package-health hosts it names.
- A `tool_used: Skill` grader in every case shows whether the skill fired on a plain request. It is an indicator and is not scored.
- Results go to `evals/results/` (ignored by git). Every run is a real model call on your account.

## Known interactions

- A hook that blocks all edits under `tests/` and `conftest.py` also blocks adding new tests. Allow new test files, or set the hook's override for test-writing sessions.
- Each skill's `argument-hint` line is outside the open spec (Claude Code and VS Code Copilot use it for autocomplete). Delete that line before uploading a skill to claude.ai or the Skills API, which reject unknown keys.
- `scripts/detect_project.py` is copied into every skill so each folder stands alone. `check_skills.py` fails if a copy differs from the canonical file; `check_skills.py --sync` rewrites the copies.

## Try it in your tool

Claude Code: ask `add a regression test for the bug in <file>` and check that the agent writes the failing test before the fix. Then `/testing-python-packages rigor=lite fix the flaky test in tests/test_x.py`.

Copilot (VS Code agent mode or cloud agent): run `/skills` to confirm the eleven skills are listed, then ask the same two prompts. Copilot does not guarantee that it picks a skill, so test both the slash command and the plain request. This repo was not tested in Copilot.

## Develop

```bash
uv sync
uv run pytest                        # tests for the scripts
uv run ruff check scripts tests && uv run mypy scripts tests
uv run python scripts/check_skills.py   # spec + budget check for skills/
uv run python scripts/check_skills.py --argument-keys scene,fps ../other/skills   # other skillsets; empty value accepts any key
```

After changing `scripts/detect_project.py`, run `uv run python scripts/check_skills.py --sync` to copy it into each skill that uses it.

## License

MIT.
