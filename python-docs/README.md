# python-docs

Part of the [skills monorepo](../README.md). Run the development commands from this folder.

One agent skill, `writing-documentation`, for writing and editing software documentation, plus `lint_prose.py`, a standard-library prose linter the skill runs on every draft.

## Where it comes from

It starts from softaworks' [writing-clearly-and-concisely](https://github.com/softaworks/agent-toolkit/tree/main/skills/writing-clearly-and-concisely) (MIT): Strunk's composition rules and the AI-writing patterns Wikipedia editors catalogued. That skill targets any prose. This one targets documentation and adds the conventions that well-documented projects follow:

| Source | What the skill takes from it |
| --- | --- |
| [Diátaxis](https://diataxis.fr/) | One page, one purpose: tutorial, how-to, reference or explanation |
| [Google developer documentation style guide](https://developers.google.com/style) | Voice, tense, sentence-case headings, procedures, link text, timeless wording |
| [Microsoft Writing Style Guide](https://learn.microsoft.com/style-guide/welcome/) | Plain words, scannable structure, global readers |
| [Python devguide style guide](https://devguide.python.org/documentation/style-guide/) | Economy of expression, affirmative tone, security sections, no Latin abbreviations |
| [PEP 257](https://peps.python.org/pep-0257/), [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html), [Google Python style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) | Docstring formats, and when each applies |
| [Keep a Changelog](https://keepachangelog.com/) | Changelog structure for users |
| READMEs of HTTPX, Polars, Ruff, uv | Landing-page README shape |

Two choices differ from the original skill:

- **Shorter.** The original loads Strunk's full text (up to 4,500 tokens per section). This skill keeps the rules in about 2,600 tokens and moves detail into seven reference files that load only when needed. In SkillsBench (arXiv:2602.12670), focused skills raised pass rates by about 17 to 19 points while exhaustive, documentation-style skills lowered them by about 3.
- **Checked by a script.** `lint_prose.py` enforces the word-level rules instead of leaving them to the model's memory. It covers puffery, AI vocabulary, minimizers, filler, Latin abbreviations, time-relative words, conversation residue, directional references, vague link text, title-case headings, long sentences and em-dash density.

## Skill

| Skill | Loads when you... | Body (est. tokens) |
| --- | --- | --- |
| `writing-documentation` | write or review docs, a README, docstrings, a tutorial, a guide or release notes | 2.6k |

References: `diataxis.md`, `style-guide.md`, `docstrings.md`, `readme-and-changelog.md`, `code-examples.md`, `ai-patterns.md`, `composition.md`.

Docstring *content* rules (no conversation residue, no restated signatures) stay in `writing-python-code` in the core bundle of [python-engineering](../python-engineering/); this skill covers format and everything outside code. Install both for Python projects.

## Install

```bash
mkdir -p .claude/skills && cp -r /path/to/skills/python-docs/skills/writing-documentation .claude/skills/
```

Arguments: `style=` (`google`, `microsoft`) and `docstrings=` (`numpy`, `google`, `sphinx`) override what the skill detects in the project.

## The linter

```bash
python3 scripts/lint_prose.py docs/ README.md          # every rule
python3 scripts/lint_prose.py docs/ --future           # also flag "will ..." in reference pages
python3 scripts/lint_prose.py docs/ --rules puffery,minimizer
```

It reads Markdown, reST and text; skips code blocks, inline code, URLs, quoted words and front matter; skips the `timeless` rule in changelogs; and exits 1 when it finds anything, so it can run in CI. Findings are advice: a technical term or a deliberate word can stay. Silence a line with `lint-prose: ignore`, or a block between `lint-prose: off` and `lint-prose: on` (in HTML comments in Markdown).

Projects that already use [Vale](https://vale.sh/) keep it; the skill runs both.

## Evals

`skills/writing-documentation/evals/` holds three cases (a README from scratch, numpydoc docstrings, and a README plus docstrings for a reader who has never seen the code) and `evals/writing-documentation.triggers.json` holds trigger checks.

## Develop

```bash
uv sync
uv run pytest
uv run ruff check scripts tests && uv run mypy scripts tests
cp scripts/lint_prose.py skills/writing-documentation/scripts/   # after changing the script; a test checks the copy
cd ../python-engineering && uv run python scripts/check_skills.py --argument-keys style,docstrings ../python-docs/skills
```

## License

MIT. The AI-pattern list paraphrases Wikipedia's "Signs of AI writing" (CC BY-SA 4.0) via softaworks' skill; Strunk's *The Elements of Style* (1918) is in the public domain.
