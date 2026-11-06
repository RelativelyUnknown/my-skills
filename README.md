# skills

A monorepo of my agent skills. The Python ones are about good coding practices: tests that can fail, small honest code, readable APIs and docs. Each folder is one self-contained skillset with its own README, skills and tooling. Facts in the skills were checked against current documentation in November 2026. The skills follow the open [Agent Skills](https://agentskills.io/specification) format, so they work in Claude Code and GitHub Copilot.

## Skillsets

| Folder | What it is | Skills |
| --- | --- | --- |
| [`python-engineering/`](python-engineering/) | Rules that make an AI agent write less slop when developing Python packages, plus the scripts that validate them | `testing-python-packages`, `writing-python-code`, `setting-up-python-packages`, `designing-package-apis`, `releasing-python-packages`, `reviewing-python-changes`, `profiling-python-code`, `auditing-python-dependencies`, `avoiding-code-snags`, `choosing-python-design-patterns`, `writing-python-scripts-and-clis` |
| [`python-web/`](python-web/) | Web APIs and services with FastAPI, Django, SQLAlchemy: validation, per-object auth, async, security, deployment | `building-python-web-services` |
| [`python-docs/`](python-docs/) | Documentation to the conventions of well-documented projects, plus a prose linter | `writing-documentation` |
| [`third-party/`](third-party/) | Unmodified copies of other publishers' Python coding-practice and writing skills (MIT), each with its licence, source commit and review notes | `wshobson-python` (16 skills), `humanizer`, `writing-clearly-and-concisely` |
| [`powerpoint-animations/`](powerpoint-animations/) | Clean looping explainer animations rendered to MP4/GIF and put into PowerPoint | `powerpoint-animation-style`, `building-animation-scenes`, `exporting-animations-to-powerpoint` |

## Install

Skills live in `<skillset>/skills/<skill-name>/`. Copy the ones you want into a project or your home folder:

```bash
# one skillset into a project
mkdir -p .claude/skills && cp -r python-engineering/skills/* .claude/skills/

# one skill, for all your projects
mkdir -p ~/.claude/skills && cp -r powerpoint-animations/skills/powerpoint-animation-style ~/.claude/skills/
```

`.claude/skills/` is read by both Claude Code and Copilot. Every skill folder is self-contained, so any subset works. Skillset-specific requirements and arguments are in each skillset's README.

Skills from other publishers are vendored, unmodified and with their licences, in [`third-party/`](third-party/); nothing there is installed by default.

## Layout

```
skills/
├── README.md                       this index
├── LICENSE
├── python-engineering/             skillset (own README, pyproject, tests, check script)
│   ├── skills/<skill>/SKILL.md     (+ references/, scripts/, assets/, evals/)
│   ├── evals/                      trigger checks per skill
│   ├── scripts/  tests/
│   └── pyproject.toml  uv.lock
├── python-web/                     skillset (uses the shared checker)
├── python-docs/                    skillset (prose linter, tests)
├── third-party/                    vendored skills (own licences, SOURCE.md each)
└── powerpoint-animations/          skillset
    └── skills/<skill>/SKILL.md
```

## What the research says about skills

These skills follow what 2026 evaluations of agent skills and context files found:

- **Curated skills help; generated ones do not.** SkillsBench ([arXiv:2602.12670](https://arxiv.org/abs/2602.12670)) measured a 16-point average pass-rate gain from human-curated skills and none from skills models wrote for themselves. Skills drafted with an AI, including these, need a person's review and evals before they are trusted.
- **Focused beats exhaustive.** In the same benchmark, two or three focused skills per task gained the most, and exhaustive documentation-style skills lowered pass rates. Hence the 200-line body limit, one home per rule, and references that load on demand.
- **Generic coding advice adds little.** Software engineering showed the smallest gains, and SWE-Skills-Bench ([arXiv:2603.15401](https://arxiv.org/abs/2603.15401)) found most public coding skills changed nothing, while version-mismatched guidance made results worse. The skills therefore detect the project's real tools and versions first (`detect_project.py`) and spend their words on non-obvious, current facts.
- **Extra context costs steps.** Evaluating AGENTS.md ([arXiv:2602.11988](https://arxiv.org/abs/2602.11988)) found context files raise inference cost by about 20% while agents follow every instruction in them. Rules that are not needed for the task stay out of the always-loaded text.
- **Measure each skill.** New skills ship eval cases and trigger checks; run them with and without the skill and drop any skill that shows no gain.

## Adding a skillset

1. Create `<skillset>/` with a `README.md` and a `skills/<skill-name>/SKILL.md` per skill (`name` must equal the folder name).
2. Keep tooling inside the skillset folder, so it can be used or removed on its own.
3. Add a row to the table above.

Any skillset can reuse the checker (frontmatter, token budgets, links): `cd python-engineering && uv run python scripts/check_skills.py ../<skillset>/skills`. If its skills use `argument-hint`, pass the allowed keys with `--argument-keys a,b`, or an empty value to accept any.

## License

MIT.
