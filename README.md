# skills

A monorepo of my agent skills. Each folder is one self-contained skillset with its own README, skills and tooling. The skills follow the open [Agent Skills](https://agentskills.io/specification) format, so they work in Claude Code and GitHub Copilot.

## Skillsets

| Folder | What it is | Skills |
| --- | --- | --- |
| [`python-package-development/`](python-package-development/) | Rules that make an AI agent write less slop when developing Python packages, plus the scripts that validate them | `testing-python-packages`, `writing-python-code`, `setting-up-python-packages`, `designing-package-apis`, `releasing-python-packages`, `reviewing-python-changes` |
| [`powerpoint-animations/`](powerpoint-animations/) | Clean looping explainer animations rendered to MP4/GIF and put into PowerPoint | `powerpoint-animation-style`, `building-animation-scenes`, `exporting-animations-to-powerpoint` |

## Install

Skills live in `<skillset>/skills/<skill-name>/`. Copy the ones you want into a project or your home folder:

```bash
# one skillset into a project
mkdir -p .claude/skills && cp -r python-package-development/skills/* .claude/skills/

# one skill, for all your projects
mkdir -p ~/.claude/skills && cp -r powerpoint-animations/skills/powerpoint-animation-style ~/.claude/skills/
```

`.claude/skills/` is read by both Claude Code and Copilot. Every skill folder is self-contained, so any subset works. Skillset-specific requirements and arguments are in each skillset's README.

## Layout

```
skills/
├── README.md                       this index
├── LICENSE
├── python-package-development/     skillset (own README, pyproject, tests, check script)
│   ├── skills/<skill>/SKILL.md
│   ├── scripts/  tests/
│   └── pyproject.toml  uv.lock
└── powerpoint-animations/          skillset
    └── skills/<skill>/SKILL.md
```

## Adding a skillset

1. Create `<skillset>/` with a `README.md` and a `skills/<skill-name>/SKILL.md` per skill (`name` must equal the folder name).
2. Keep tooling inside the skillset folder, so it can be used or removed on its own.
3. Add a row to the table above.

Python skillsets can reuse the checker: `cd python-package-development && uv run python scripts/check_skills.py ../<skillset>/skills`.

## License

MIT.
