---
name: auditing-python-dependencies
description: "Vets and audits Python dependencies: checks a package is real and maintained before adding it, scans the lock file for known vulnerabilities with uv audit or pip-audit, triages and fixes findings, checks licenses and update policy. Use when adding a dependency, answering a security alert, or auditing a project's supply chain."
argument-hint: "[runner=uv report=normal]"
---

# Auditing Python dependencies

Every dependency is code you run without reading. Add few, verify each, and fix vulnerabilities with the smallest upgrade that removes them.

## Start

Run `python3 <this skill's folder>/scripts/detect_project.py` from the project root (`runner`, `python.target`, `tools.missing`; `# default` means nothing was found). Arguments (`key=value` after the skill name) override detected facts. Commands below use uv; with another runner, export its lock to a requirements file and run the same checks.

Never change the lock file, upgrade, downgrade or remove a package as a side effect of an audit. Show the findings and the proposed change; act when asked.

## Before adding a package

Agents suggest package names that do not exist, and attackers register those names. Check before `uv add`:

1. The exact name exists on PyPI and links to a source repository whose name and owner match what you expect. Look for near-duplicates and misspellings.
2. It is maintained: a release within the last year or a stable, finished scope; more than one maintainer or an organization behind it; open issues answered.
3. Its license is compatible with the project's license.
4. It ships wheels for every Python version and platform the project supports, or builds from a pure-Python sdist.
5. No unresolved advisories (search the name on osv.dev or the repository's security tab).
6. It earns its place: the rules in `writing-python-code` (standard library first, nothing for a few lines of code).

State the result of each check in the report. If any fails, propose an alternative or ask.

## Scan for known vulnerabilities

```bash
uv audit --locked                      # preview feature in uv 0.13; flags may change
uv audit --locked --output-format sarif > audit.sarif   # for code-scanning upload
```

Without `uv audit`, use pip-audit on the exported lock:

```bash
uv export --format requirements-txt --locked --no-emit-project -o /tmp/requirements-audit.txt
uvx pip-audit -r /tmp/requirements-audit.txt --disable-pip   # hashes from the export make --disable-pip safe
```

Audit what ships: dependencies plus extras. Audit dev groups separately; a finding there matters for CI and developer machines, not users.

## Triage each finding

| Question | Then |
| --- | --- |
| Is a fixed version available? | Upgrade only that package: `uv lock --upgrade-package <name>`, then `uv sync --locked` and the full test suite |
| Does the fix need a new major version or a raised lower bound in `pyproject.toml`? | Propose it with the changelog's breaking changes; get approval |
| No fix yet, but the vulnerable code path is unused? | Document why, with the advisory ID and a review date; ignore it only with approval (`pip-audit --ignore-vuln <ID>`) |
| No fix and the path is used? | Report it as blocking; suggest a replacement or a mitigation |

Never run `uv lock --upgrade` (everything) to fix one advisory without asking; it changes far more than the fix. Never downgrade to make a scanner quiet.

## Keep it healthy

- Commit `uv.lock`; CI installs with `uv sync --locked` so it uses exactly the audited set.
- Run the audit in CI on a schedule (weekly) as well as on pull requests that change the lock file.
- Automated updates (Dependabot or Renovate) with a waiting period before adopting new releases (Dependabot `cooldown`, Renovate `minimumReleaseAge`) reduce exposure to compromised fresh releases.
- Pin GitHub Actions to release tags (or commit SHAs for high-assurance repos), and give workflows the least `permissions` they need. Publishing uses trusted publishing, never a stored token (`releasing-python-packages`).
- Licenses of the installed set: `uvx pip-licenses` inside the project environment; flag anything incompatible with the project's license.
- Code-level security rules (ruff `S` rules, or bandit if the project uses it) are separate from dependency audits; run both.

## Report

List each package checked or finding triaged: name and version, advisory ID or check failed, severity, decision (upgrade, ignore with reason and review date, blocked), and the commands run with their output. Separate what you changed from what you only propose.
