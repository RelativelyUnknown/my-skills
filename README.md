# skills

Agent skills for Python development, for **GitHub Copilot first and any agent that reads `SKILL.md` folders and `AGENTS.md`**. The goal is a small, token-lean set: tests that can fail, small honest code, readable APIs and docs. Facts in the skills were checked against current documentation in November 2026.

## Skills

Three skills, each a folder you copy. Each holds a short `SKILL.md` and a tree of `references/` it reads on demand, so only the files a task needs enter the context.

| Folder | What it is |
| --- | --- |
| [`python-engineering/`](python-engineering/) | rules for writing, testing, packaging and running Python; the tree is `references/fields/<field>/<type>/<kind>/`, and a `kind:` path saved in `AGENTS.md` picks the folder to read |
| [`reviewing-python-code/`](reviewing-python-code/) | reviews a diff or your own change before you say done |
| [`documentation/`](documentation/) | writing documentation by what the reader needs (tutorial, how-to, reference, explanation, docstrings, README, changelog, ADR, runbook, troubleshooting) and minimalist explainer animations and diagrams |


## Size

Tokens are characters divided by four, so approximate. Only the description is always in context; the body loads when the skill fires; a reference file loads only when read.

| Skill | Description | Body | Reference files | Largest file | Eval cases |
| --- | --- | --- | --- | --- | --- |
| `python-engineering` | 76 | 980 | 79 (about 42k tokens in all) | 1.5k | 42 |
| `reviewing-python-code` | 71 | 76 | 3 (1.8k) | 1.0k | 2 |
| `documentation` | 73 | 587 | 28 (11k) | 1.4k | 5 |

All three descriptions together are about 220 tokens, against about 1.3k for the 20 flat skills they replace. A typical task reads the front door and two to five reference files. The `python-engineering` body is over its 600-token aim because it lists the files to read; naming them directly worked better than relying on index files (the model rarely read those). Eight reference files are above the 4,200-character aim (tables and process guides read on demand); they were not trimmed.

## Install

Copy the three folders into the folder your tool reads:

```bash
# GitHub Copilot (VS Code agent mode, CLI): project skills
mkdir -p .github/skills && cp -r python-engineering reviewing-python-code documentation .github/skills/
# Claude Code (VS Code and the Copilot CLI also read this folder)
mkdir -p .claude/skills && cp -r python-engineering reviewing-python-code documentation .claude/skills/
```

Delete each skill's `evals/` folder if you do not run evals. In VS Code run `/skills` to confirm they are listed; this repository was not run in Copilot.

## Project defaults, not arguments

Skills do not take arguments. They read a `## Python defaults` section of `AGENTS.md`, infer what is missing from the repo, ask only what is still unknown (once, with the agent's question tool if it has one), and save the answers there. Edit or delete a line to be asked again. Example:

```markdown
## Python defaults
python: 3.12
runner: uv
types: mypy
layout: src
rigor: full
report: normal
```

Add a `kind:` line (a path such as `software-engineering/library/shared`) to choose which part of the reference tree is read; without one the skill reads `references/which-type.md` once and saves it. Claude Code does not read `AGENTS.md`; add `@AGENTS.md` to `CLAUDE.md`.

## Checking the skills by hand

No scripts or tests: skills are markdown. From the repository root:

```bash
# description length (budget: 300)
for f in python-engineering reviewing-python-code documentation; do awk -v F="$f" '/^description:/{d=substr($0,14); gsub(/^"|"$/,"",d); print length(d), F; exit}' $f/SKILL.md; done
# folder name equals name:
for f in python-engineering reviewing-python-code documentation; do [ "$(sed -n 's/^name: //p' $f/SKILL.md | head -1)" = "$f" ] || echo "bad name: $f"; done
# leaves over budget (about 4,200 characters) and folders without an index
find python-engineering/references documentation/references reviewing-python-code/references -name '*.md' ! -name index.md -size +4200c
for d in $(find python-engineering/references/fields documentation/references/written -type d); do [ -f $d/index.md ] || echo "no index: $d"; done
# no grouped names
find python-engineering reviewing-python-code documentation -name '*-and-*' ! -path '*/evals/*'
```

## What the research says about skills

- **Curated skills help; generated ones do not.** SkillsBench ([arXiv:2602.12670](https://arxiv.org/abs/2602.12670)) measured a 16-point average pass-rate gain from human-curated skills and none from skills models wrote for themselves. Skills drafted with an AI, including these, need a person's review and evals before they are trusted.
- **Focused beats exhaustive.** In the same benchmark, two or three focused skills per task gained the most, and exhaustive documentation-style skills lowered pass rates. Hence small bodies, one home per rule, and references that load on demand.
- **Generic coding advice adds little.** SWE-Skills-Bench ([arXiv:2603.15401](https://arxiv.org/abs/2603.15401)) found most public coding skills changed nothing, while version-mismatched guidance made results worse. The skills spend their words on non-obvious, current facts and read the project's real versions first.
- **Extra context costs steps.** Evaluating AGENTS.md ([arXiv:2602.11988](https://arxiv.org/abs/2602.11988)) found context files raise inference cost by about 20% while agents follow every instruction in them.
- **Measure each skill.** Skills ship eval cases (`<skill>/evals/`, run with `claude plugin eval`); a skill that shows no gain is cut.

## License

MIT. Adapted third-party material keeps its own licence; see `THIRD_PARTY_NOTICES.md`.
