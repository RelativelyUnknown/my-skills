# python-engineering

Part of the [skills repository](../README.md). Skills for developing Python code and packages, for GitHub Copilot first and any agent that reads `SKILL.md` folders. They make an AI agent write less slop: tests that can fail, errors that surface, fewer concepts, honest reports. The rules come from the *Python Engineering Rules for AI Agents* (v2) and the sources credited in [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).

This is the interim, flat layout (20 skills in three folders). The plan is one routed `python-engineering` skill with a nested reference tree by field and kind of project; see the repository README.

## Skills

Folder `core` applies to every Python project.

| Skill | Loads when you... |
| --- | --- |
| `writing-python-code` | write, change or debug Python; holds the end-of-task report |
| `avoiding-code-snags` | write or change code: short watch-outs to follow as you go |
| `testing-python-packages` | add or fix tests, chase a flaky test, configure pytest |
| `typing-python-code` | add or fix type hints, or a type checker reports errors |
| `managing-python-resources` | open, pool or release files, connections, locks, subprocesses |
| `profiling-python-code` | chase slow code or memory, or consider a faster library |
| `choosing-python-design-patterns` | are asked for a pattern, new layers or an extension point |
| `auditing-python-dependencies` | add a dependency, answer a security alert, audit the supply chain |
| `using-uv` | the runner is uv: dependencies, locks, scripts, Docker, CI |
| `reviewing-python-changes` | review a diff, or check your work before saying done |
| `writing-python-scripts-and-clis` | are asked for a script or command-line tool |

Folder `library` is for packages others install: `setting-up-python-packages`, `designing-package-apis`, `releasing-python-packages`.

Folder `application` is for running services: `building-python-web-services`, `writing-async-python`, `running-background-jobs`, `adding-observability`, `configuring-python-applications`, `making-calls-resilient`.

## Install

See the repository README. Each skill folder is self-contained. Skills read project defaults from the `## Python defaults` section of `AGENTS.md` and do not take arguments.

## Evals

Cases are in `<folder>/skills/<skill>/evals/<case>/` (`prompt.md`, `case.yaml`, `graders/`, and `fixture.sh` where the case needs files), the layout `claude plugin eval` reads:

```bash
claude plugin eval core/skills/typing-python-code --scaffold --allow-tools Write Edit --judge-model sonnet --max-cost-usd 4
```

- `--scaffold` runs each case's `fixture.sh` as you; read it first.
- Granting `Bash` needs an OS sandbox (on Linux, `bubblewrap` and `socat`); without one the run refuses.
- A `tool_used: Skill` grader in each case shows whether the skill fired on a plain request. It is an indicator and is not scored.
- A run is a real model call on your account. Some cases may show no difference between the arms; that is a result to act on, not a pass.
- Trigger checks (prompts that should and should not load a skill) are in `evals/<skill>.triggers.json`.

## Known interactions

- A hook that blocks all edits under `tests/` and `conftest.py` also blocks adding new tests. Allow new test files for test-writing sessions.
- Skills do not run scripts; the few checks they need are `grep` and `git` one-liners inside the skill.

## License

MIT. Adapted material keeps its upstream licence next to it; see `SOURCE.md` in the skill folder.
