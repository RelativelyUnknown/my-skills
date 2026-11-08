# skills

Agent skills for Python development, for **GitHub Copilot first and any agent that reads `SKILL.md` folders and `AGENTS.md`**. The goal is a small, token-lean set: tests that can fail, small honest code, readable APIs and docs. Facts in the skills were checked against current documentation in November 2026.

This repository is mid-restructure: the skills are being folded into three routed skills (`python-engineering`, `reviewing-python-code`, `documentation`) with a nested reference tree, and the third-party material is being absorbed with attribution. Until that lands, the layout below is the interim one.

## Skillsets

| Folder | What it is |
| --- | --- |
| [`python-engineering/`](python-engineering/) | 20 skills for developing Python, grouped in `core`, `library` and `application` folders |
| [`python-docs/`](python-docs/) | `writing-documentation`: documentation to the conventions of well-documented projects |
| [`powerpoint-animations/`](powerpoint-animations/) | clean looping explainer animations rendered to MP4/GIF (to be generalized and moved under documentation) |
| [`third-party/`](third-party/) | unmodified copies of other publishers' skills (MIT), each with licence and `SOURCE.md` (being absorbed) |

## Install

Copy skill folders into the folder your tool reads:

```bash
# GitHub Copilot (VS Code agent mode, CLI): project skills
mkdir -p .github/skills && cp -r python-engineering/{core,library,application}/skills/* python-docs/skills/* .github/skills/
# Claude Code (VS Code and the Copilot CLI also read this folder)
mkdir -p .claude/skills && cp -r python-engineering/{core,library,application}/skills/* python-docs/skills/* .claude/skills/
```

Each skill is self-contained, so any subset works. In VS Code run `/skills` to confirm they are listed; this repository was not run in Copilot.

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

Claude Code does not read `AGENTS.md`; add `@AGENTS.md` to `CLAUDE.md`.

## Checking the skills by hand

No scripts or tests: skills are markdown. From a skills folder:

```bash
# description length (budget: 300)
for f in */skills/*/SKILL.md; do awk -v F="$f" '/^description:/{d=substr($0,14); gsub(/^"|"$/,"",d); print length(d), F; exit}' "$f"; done | sort -rn | head
# folder name equals name:
for f in */skills/*/SKILL.md; do n=$(sed -n 's/^name: //p' "$f" | head -1); [ "$n" = "$(basename "$(dirname "$f")")" ] || echo "bad name: $f"; done
# size (budget: about 4,200 characters per body)
wc -c */skills/*/SKILL.md | sort -rn | head
```

## What the research says about skills

- **Curated skills help; generated ones do not.** SkillsBench ([arXiv:2602.12670](https://arxiv.org/abs/2602.12670)) measured a 16-point average pass-rate gain from human-curated skills and none from skills models wrote for themselves. Skills drafted with an AI, including these, need a person's review and evals before they are trusted.
- **Focused beats exhaustive.** In the same benchmark, two or three focused skills per task gained the most, and exhaustive documentation-style skills lowered pass rates. Hence small bodies, one home per rule, and references that load on demand.
- **Generic coding advice adds little.** SWE-Skills-Bench ([arXiv:2603.15401](https://arxiv.org/abs/2603.15401)) found most public coding skills changed nothing, while version-mismatched guidance made results worse. The skills spend their words on non-obvious, current facts and read the project's real versions first.
- **Extra context costs steps.** Evaluating AGENTS.md ([arXiv:2602.11988](https://arxiv.org/abs/2602.11988)) found context files raise inference cost by about 20% while agents follow every instruction in them.
- **Measure each skill.** Skills ship eval cases (`<skill>/evals/`, run with `claude plugin eval`); a skill that shows no gain is cut.

## License

MIT. Adapted third-party material keeps its own licence; see `THIRD_PARTY_NOTICES.md`.
