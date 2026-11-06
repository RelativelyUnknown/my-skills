# third-party

Unmodified copies of other publishers' skills for Python coding practices and writing, kept here so everything lives in one repository. They are **not** covered by this repository's MIT licence: each folder has its own `LICENSE` (all MIT) and a `SOURCE.md` with the upstream URL, the pinned commit, the file hashes and the review notes. Keep the licence file when you copy a skill elsewhere; the MIT licence requires it.

Nothing here is installed by default. Copy only what you want (see Install), and read the skill first.

## What is here

| Folder | Skills | Upstream and commit | Licence |
| --- | --- | --- | --- |
| `wshobson-python/` | 16: `async-python-patterns`, `python-anti-patterns`, `python-background-jobs`, `python-code-style`, `python-configuration`, `python-design-patterns`, `python-error-handling`, `python-observability`, `python-packaging`, `python-performance-optimization`, `python-project-structure`, `python-resilience`, `python-resource-management`, `python-testing-patterns`, `python-type-safety`, `uv-package-manager` | [wshobson/agents](https://github.com/wshobson/agents), `4bde316` | MIT, Seth Hobson |
| `humanizer/` | `humanizer`: rewrite AI-sounding prose (26 patterns in six groups, and a mark, rewrite, check loop) | [blader/humanizer](https://github.com/blader/humanizer), `0ef9fe5` | MIT, Siqi Chen |
| `softaworks-writing/` | `writing-clearly-and-concisely`: Strunk's composition rules and a field guide to AI writing patterns | [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit), `3027f20` | MIT, Leonardo Flores |

## Install

Each skill folder is self-contained:

```bash
mkdir -p .claude/skills
cp -r third-party/wshobson-python/skills/python-error-handling .claude/skills/
cp -r third-party/humanizer/skills/humanizer .claude/skills/
cp -r third-party/softaworks-writing/skills/writing-clearly-and-concisely .claude/skills/
```

`.claude/skills/` is read by Claude Code and Copilot. Every installed skill adds its description to every conversation, so install few. These copies are unmodified, so they do not meet this repository's budgets (the humanizer `SKILL.md` is about 32 KB and softaworks' `signs-of-ai-writing.md` about 94 KB); the checker is not run on this folder.

## Overlap with this repository's skills

Pick one skill per topic, not both.

| Vendored | Overlaps with | Note |
| --- | --- | --- |
| `python-anti-patterns` | `avoiding-code-snags` | Conflicts: it recommends Repository and DTO layers, pydantic-settings and a retry decorator, which this repository's minimal-abstraction, standard-library-first rules avoid. |
| `python-design-patterns` | `choosing-python-design-patterns` | Same stance (KISS, rule of three, delete before abstracting); ours gives the Python form of each pattern. |
| `python-testing-patterns`, `python-error-handling`, `python-type-safety`, `python-code-style`, `python-resource-management` | `testing-python-packages`, `writing-python-code` | Same topics. Not compared line by line. |
| `python-packaging`, `uv-package-manager`, `python-project-structure` | `setting-up-python-packages`, `releasing-python-packages` | Same topics. Not compared line by line. |
| `python-performance-optimization` | `profiling-python-code` | Same topic. Not compared line by line. |
| `humanizer`, `writing-clearly-and-concisely` | `python-docs` (`writing-documentation`) | `writing-documentation` already builds on the softaworks skill and adds Diátaxis, docstring conventions and a prose linter. |

## Not vendored

Databricks' official skills (the licence is not stated on the pages I read), dbt's and Airflow's (Apache-2.0, vendor-published): off-focus for Python coding practices. Install them from their vendors if you need them.

## Judging a skill before trusting it

| Place | Shows |
| --- | --- |
| [Tessl registry](https://tessl.io/registry) | Quality score, eval-based impact with and without the skill, Snyk scan, version |
| [skills.sh audits](https://skills.sh/audits) | Per-skill results from Gen, Socket and Snyk; several widely installed skills show medium or high risk |
| [anthropics/skills](https://github.com/anthropics/skills) | The spec and template; described as demonstration only, no scans |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | Community picks; says third-party content must be inspected before installing |

Install counts measure popularity, not quality. Read the `SKILL.md` and every script, check the frontmatter for permission fields (`allowed-tools`, hooks), and check the licence before copying.

## Updating a copy

Download the files again at a newer commit (raw files, not a rendered page), repeat the review in `SOURCE.md`, replace the files, and update the commit, date and hashes.
