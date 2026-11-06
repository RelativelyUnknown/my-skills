# Recommended third-party skills

Skills from other publishers worth installing or borrowing ideas from, for Python development, data engineering, documentation, design patterns and code snags. Researched 6 November 2026 by reading each source page. Counts and scores below are as shown on those pages that day.

Rule of thumb: prefer skills published by the vendor of the tool they cover, read the `SKILL.md` and any `scripts/` before installing, and check the licence before copying a file into a repository. A skill that you install does not need to be copied; a skill you copy must allow it.

## Where to look, and how to judge

| Place | Use it for | Signals it shows |
| --- | --- | --- |
| [Tessl registry](https://tessl.io/registry) | Judging quality | Quality %, eval-based impact (with and without the skill), Snyk scan, version, review date |
| [skills.sh](https://skills.sh) and its [audits page](https://skills.sh/audits) | Judging safety and popularity | Install counts; per-skill results from Gen, Socket and Snyk. Several of the most installed skills show medium or high risk |
| [anthropics/skills](https://github.com/anthropics/skills) | What a well-formed skill looks like | Spec and template. Described as demonstration only; no scans. The document skills are source-available, not open source |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) | Copilot-oriented picks | 40.9k stars; says the content is third-party and must be inspected before installing |
| [claudemarketplaces.com](https://claudemarketplaces.com), [agent-skills.md](https://agent-skills.md) | Discovery only | Skill counts (about 23k and 84k); no safety signals |

SkillsMP returned 403 and was not read. Install counts measure popularity, not quality.

## Data engineering and Databricks

| Skill source | Licence | Verdict | Notes |
| --- | --- | --- | --- |
| [databricks/databricks-agent-skills](https://github.com/databricks/databricks-agent-skills) ([docs](https://docs.databricks.com/aws/en/agent-skills/)) | Not stated on the docs pages | **Install, do not copy** | 32 stable skills (core, jobs, pipelines, bundles, Python SDK, Unity Catalog, structured streaming, Iceberg, SQL warehouses and more) and one experimental. Official. `databricks aitools install`, or the Claude Code or Copilot plugin marketplace. The Copilot cloud agent takes no plugins, so its skills must be copied into `.github/skills/`: check the licence first |
| [dbt-labs/dbt-agent-skills](https://github.com/dbt-labs/dbt-agent-skills) | Apache-2.0 | **Install if you use dbt** | Vendor-published. `adding-dbt-unit-test`, `using-dbt-for-analytics-engineering`, `maintaining-dbt-documentation`, plus migration skills. Pin a tag: the default install tracks `main` |
| [astronomer/agents](https://github.com/astronomer/agents) | Apache-2.0 | **Install if you use Airflow, skills only** | `authoring-dags`, `testing-dags`, `debugging-dags` and others. The plugin route adds an MCP server, anonymous telemetry from the `af` CLI and a credentials file; the skills-only route avoids that |
| Generic "data-engineer" skills (alirezarezvani, davila7, sickn33 and similar) | Mixed | **Skip** | Low installs, marketing-style claims, mixed scan results, and generic advice, the kind public evaluations found to change nothing |

## Documentation

| Skill source | Licence | Verdict | Notes |
| --- | --- | --- | --- |
| [blader/humanizer](https://github.com/blader/humanizer) | MIT | **Borrow the method** | 26 patterns of AI-sounding prose in six groups, and a mark, rewrite, check-for-unsupported-additions loop. The `SKILL.md` is about 32k characters, too large to keep loaded, and it covers prose, not docstrings or code comments |
| [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit), `writing-clearly-and-concisely` | MIT (per the repo page) | Already folded into `documentation/` | Strunk's composition rules plus AI-pattern list |
| Diátaxis skills (sammcj, joshuadavidthomas, mcollina and others) | Mixed | Skip | Covered by `documentation/`'s Diátaxis reference |
| dbt `maintaining-dbt-documentation` | Apache-2.0 | **Borrow the idea** | Audit which items lack documentation, then draft the missing text in the project's own style |

## Design patterns and code snags

| Skill source | Licence | Verdict | Notes |
| --- | --- | --- | --- |
| [wshobson/agents](https://github.com/wshobson/agents), `python-design-patterns` | MIT (repo) | **Borrow the stance** | KISS, rule of three, delete before abstracting, a dict lookup instead of a factory |
| wshobson/agents, `python-anti-patterns` | MIT (repo) | **Borrow the structure, not the advice** | BAD, fix, GOOD per entry and a pre-merge checklist. It recommends Repository and DTO layers, pydantic-settings and a retry library, which conflicts with a minimal-abstraction, standard-library-first style |
| `bfmcneill/agi-marketplace`, `design-patterns` | Not stated; source repo returned 404 | Skip | Textbook patterns and SOLID with no Python code. Its "when not to use patterns" list is the useful part |
| [The Little Book of Python Anti-Patterns](https://docs.quantifiedcode.com/python-anti-patterns/) | CC BY-NC-SA 4.0 | Ideas only | NonCommercial and ShareAlike: do not copy text into an MIT repository. Last updated 2021 |
| Write-ups on AI-generated code (Anaconda "deslopping AI code", dev.to "14 patterns", "8 AI coding traps") | Blogs | Source of examples | Narrative comments, duplicate helpers, tests that only assert non-null, over-mocking |

`python-package-development/skills/avoiding-code-snags` and `choosing-python-design-patterns` are this repository's own versions, written against these sources and checked with and without the skill.

## Install commands

```bash
# Databricks (CLI v1.0.0 or newer), or in Claude Code: /plugin marketplace add databricks/databricks-agent-skills
databricks aitools install

# dbt, one skill (pin a tag for reproducible installs)
npx skills add dbt-labs/dbt-agent-skills --skill adding-dbt-unit-test

# Airflow, skills only
npx skills add astronomer/agents --skill authoring-dags --skill testing-dags --skill debugging-dags
```

## Not verified

- Licence of the Databricks skills: the docs pages do not state it. Read the repository's `LICENSE`.
- Security-scan statistics quoted by third-party articles (for example "36.8% of 3,984 scanned skills had an issue") were not checked against the scanner's own data.
- `davideast/piebox` and `sac11k/python-patterns` returned 404, so those skills were not assessed.
