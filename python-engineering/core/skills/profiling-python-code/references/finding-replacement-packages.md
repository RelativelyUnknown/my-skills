# Finding a replacement package

Read when a measured hot path needs a faster or better library and `faster-libraries.md` has no good fit, or when you must judge one of its entries for this project. The facts about the data sources below were checked on 2026-11-06.

## When to look, and when not to

- **Look** when a profile names a function and a number ("`parse_rows` takes 4.1 s of 5 s"); when the incumbent is unmaintained, has an unfixed security advisory, or blocks a Python version you need; or when a requirement (async, typing, licence) cannot be met by what the project has.
- **Do not look** when nothing was measured; when the gain would be inside the run-to-run spread; when the time goes to waiting on I/O rather than computing; when you merely prefer another library; or when the project has already settled the choice. Recommend in the report; switch only when asked.
- **Why this is strict:** every dependency adds maintenance, security surface, licence terms, install size and a second API to learn. A swap earns its place only when the measured gain, or the risk it removes, is larger than that cost. Fewer dependencies is the default.

## Does it fit this project

Check each against the detected facts and `pyproject.toml`:

- `requires_python` includes the Python target and the newest Python the project tests on.
- Wheels exist for every platform and Python version the project ships to. A missing wheel means a compiler in CI.
- The licence is compatible with the project's (`license_expression`).
- Its own dependencies are few and light, and the install size is acceptable.
- Behavior matches where it matters: return types (`bytes` or `str`), error types, rounding, time zones, ordering, and the threading or async model.
- It is typed (`py.typed`), so the type checker keeps working.

## Finding candidates

In this order, stopping when one fits:

1. The standard library, and what the project already depends on (including features it does not use yet).
2. The incumbent's own documentation and issue tracker: performance pages, "alternatives", maintainers' replies.
3. What comparable, well-run projects use: open their `pyproject.toml` on GitHub.
4. A search of PyPI and GitHub for the job plus "faster" or "alternative", then the project's README.
5. Treat any README benchmark as a claim: note who ran it, on what data, against which version.

Shortlist at most two and judge those. Do not collect ten.

## Judging a candidate

Read-only requests. PyPI asks callers to send a unique `User-Agent` and to avoid bursts of requests.

- Python versions, licence, links → `https://pypi.org/pypi/<name>/json`: `info.requires_python`, `info.license_expression`, `info.classifiers`, `info.project_urls`. Skip `releases` and `downloads`: deprecated, and `downloads` is always -1
- Release cadence, deprecation → `https://api.deps.dev/v3/systems/pypi/packages/<name>`: each version's `publishedAt`, `isDefault`, `isDeprecated`
- Repository health → `https://api.deps.dev/v3/projects/github.com%2F<owner>%2F<repo>`: stars, forks, open issues, licence, `scorecard`
- Security practices → `https://api.securityscorecards.dev/projects/github.com/<owner>/<repo>`: overall score and the checks, such as `Maintained`, `Security-Policy`, `Signed-Releases`
- Popularity → `https://pypistats.org/api/packages/<name>/recent`: `last_week`, `last_month`
- Advisories → osv.dev (search the name, ecosystem PyPI), or the audit tool in `auditing-python-dependencies`: any unfixed high-severity advisory
- Wheels → the "Download files" tab on the PyPI page: the project's platforms and Python versions

Example: `curl -s -A "my-project" https://pypi.org/pypi/orjson/json | python3 -c "import json,sys; i=json.load(sys.stdin)['info']; print(i['requires_python'], i['license_expression'])"`

If a source does not respond, say so in the report. Do not guess its values.

## Reading the signals

- The date of the last release, an open-issue count that is not climbing, and the Scorecard `Maintained` check matter more than stars.
- Popularity is not quality or safety. Millions of weekly downloads can still be an abandoned or compromised package; confirm with release cadence and advisories.
- A low overall Scorecard does not disqualify a package: widely used orjson scored 4.4 on 2026-11-02. Read which checks failed and whether they matter to you.
- Red flags: no release in a long time (for example 18 months) with open issues and no maintainer replies; a single maintainer; a recent ownership change; a yanked or deprecated latest release; an unfixed high-severity advisory; no licence; no wheels for your platform.

## Proving the swap

Benchmark the incumbent and the candidate on the project's own input with the method in `profiling-python-code`. Run the full test suite. List the behavior differences you found. Report the number before and after, and the dependency added (name, version, licence). Keep the change small enough to revert in one commit.
