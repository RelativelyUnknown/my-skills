# Security audit: dependencies and release

A finding needs the same four parts as any other ([process.md](process.md)): a lower-trust party, something they control, the trusted installer or job that consumes it, and what they gain. A floating version or a missing best practice with no such path is a hardening note. Workflows and AI agents in CI are in [ci-workflows.md](ci-workflows.md).

Read with [dependencies.md](../../tabby/development/dependencies/dependencies.md), which covers vetting and scanning packages. Registry settings, branch protection and environment rules are not in the repository, so a finding that depends on them is `needs validation`.

## Measure, do not recall

Every figure about someone else's project (how many maintainers, downloads, last release, advisories) is a claim to be measured. The tool whose method this follows found that hand-collected counts were wrong: contributors on the code host and people with publish rights on the registry are different populations. Run the scanner or query the registry and quote the output; do not estimate from memory. Three rules from it: unavailable data is not evidence of risk (PyPI publishes no maintainer list, so "unknown" is not "one maintainer"); an absent measurement is not a clean verdict, so state how many dependencies were actually assessed; and check an advisory against the version in the lock file, not the latest release or a range. For a Python project that means advisories for the locked tree (`pip-audit`, OSV), archived or abandoned upstreams for direct dependencies, yanked releases, and which dependencies run code at install: an sdist builds with its `setup.py` or build backend on your machine, which `--only-binary :all:` (pip) or `--no-build` (uv) refuses.

## Where packages come from

- Two indexes configured without pinning each package to one: a name that exists on the private index can be supplied by the public one. In uv, the private index needs `explicit = true` and the package an entry under `[tool.uv.sources]` ([uv.md](../../tabby/development/dependencies/uv.md)); `--extra-index-url` with pip has no such protection.
- An internal package name that is not registered on PyPI and is installed anywhere without a pinned index.
- A dependency name one typo away from a popular package, or one the repository's history shows was added by an agent or a paste without the check in `dependencies.md`.
- An install that does not use the lock (`pip install` in CI beside a committed `uv.lock`, `--frozen` where `--locked` was meant).
- Build inputs that can change without review: a Git dependency on a branch, a `curl | sh`, a downloaded tool with no checksum, a checksum fetched from the same place as the file.

## Triage an advisory, a scanner alert or a report

A CVE, a `pip-audit` or Dependabot alert, a scanner finding or a bug report is a claim, not a verdict. Seven questions, adapted from William Woodruff's "Brocards for vulnerability triage" as cited in the Trail of Bits skill that carries them; stop at the first that dismisses it, and write down which:

1. **Threat model.** Who is the attacker, what can they do, how do they trigger it, what harm results? "An attacker with [capability] can [action] to achieve [impact]." A bug is not a vulnerability. If one element is missing, ask for it.
2. **Capability against impact.** If triggering it needs a power that already includes the harm (an active man-in-the-middle injecting content, memory corruption through `ctypes`), it adds nothing. Escalation from limited to elevated access is different and counts.
3. **Usage.** Is the vulnerable function reachable from how this project, or its dependents, actually call it? For a library with many users, check representative callers, not only its tests. Unreachable now can be reachable after a refactor: note it.
4. **Standard behaviour.** Conforming to a specification is the specification's problem, unless the project promises to be stricter than the specification and is not (HMAC-MD5 is not "broken MD5").
5. **Documented behaviour.** A documented, prominently warned behaviour (`http.server` is not for production, an `--insecure` flag) is not the component's vulnerability; a downstream project that ignores the warning has one. Documented is not the same as acceptable if no safe option exists.
6. **Proportion.** Weigh the real severity against the cost of the fix (a forced upgrade across thousands of dependents) and prefer a staged fix or a documentation change for a low-severity issue.
7. **The label.** Strip the CVE number and the CVSS score; does the description alone justify action? A high score with a vague description is a warning sign, and an unlabelled report with a concrete exploit may be critical.

Wrongly dismissing: "only in debug mode" (check production), "needs local access" (realistic in containers), "nobody uses that API" (check usage), "the spec allows it" (check what the project claims). Wrongly accepting: "it has a CVE", "the score is high", "better safe than sorry", "you cannot prove it is not exploitable" (the reporter carries the burden), "other projects patched it" (their usage differs). The verdicts are accept, dismiss with the reason, or need more information (and which).

## Release

- Publishing with a stored API token where trusted publishing is possible, or `id-token: write` granted to more than the publish job ([release.md](../../tabby/development/library/shared/release.md)).
- The published artifact is rebuilt in the publish job instead of being the one that was tested: build once, upload the artifact, publish that file.
- A release triggered by any tag from any branch, with no environment protection, on a repository where many people can push tags.
- Secrets, `.env` files, test fixtures or local configuration inside the sdist or wheel: list the archive (`unzip -l dist/*.whl`, `tar tf dist/*.tar.gz`) and read it.
- Generated files committed without the command that regenerates them, so a reviewer cannot tell an edited file from a generated one.

Report as in [reporting.md](reporting.md).
