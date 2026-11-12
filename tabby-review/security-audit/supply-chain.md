# Security audit: dependencies, CI and release

CI configuration is authorization code: it decides whose code runs with which secrets and what gets published. Ask of each workflow: what event starts it, whose code does it run, which tokens and secrets exist while it runs, and what may it change? A finding needs the same four parts as any other ([process.md](process.md)): a lower-trust party, something they control, the trusted job or installer that consumes it, and what they gain. A floating version or a missing best practice with no such path is a hardening note.

Read with [dependencies.md](../../tabby/development/dependencies/dependencies.md), which covers vetting and scanning packages. Facts about GitHub Actions below are from GitHub's documentation and were not exercised here; branch protection, environment rules and registry settings are not in the repository, so a finding that depends on them is `needs validation`.

## Where packages come from

- Two indexes configured without pinning each package to one: a name that exists on the private index can be supplied by the public one. In uv, the private index needs `explicit = true` and the package an entry under `[tool.uv.sources]` ([uv.md](../../tabby/development/dependencies/uv.md)); `--extra-index-url` with pip has no such protection.
- An internal package name that is not registered on PyPI and is installed anywhere without a pinned index.
- A dependency name one typo away from a popular package, or one the repository's history shows was added by an agent or a paste without the check in `dependencies.md`.
- An install that does not use the lock (`pip install` in CI beside a committed `uv.lock`, `--frozen` where `--locked` was meant).
- Build inputs that can change without review: a Git dependency on a branch, a `curl | sh`, a downloaded tool with no checksum, a checksum fetched from the same place as the file.

## Workflows

- `pull_request_target` or `workflow_run` that checks out and runs the pull request's code: it runs a contributor's code with the base repository's secrets and a write token. `pull_request` from a fork gets neither.
- An expression from the event used inside `run:` (`${{ github.event.pull_request.title }}`, a branch name, an issue body, a commit message): it is pasted into the shell script before the shell parses it. Pass it through `env:` and quote the variable.
- No `permissions:` block, or `write` scopes on a job that only tests. Start from `contents: read` per workflow and add per job.
- A cache or artifact written by a job that runs untrusted code and restored by a job that publishes.
- Actions referenced by a branch (`@main`). A tag can also be moved; pin a commit SHA where the workflow holds secrets or publishes.
- A self-hosted runner reachable from pull requests of a public repository.

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

## AI agents in workflows

A workflow that runs an AI agent (a code-review bot, an issue triager, `claude-code-action`, Gemini CLI, Codex) treats text as instructions. Text from a pull request, issue, comment, commit message or file is attacker-controlled when the author is an outsider, so the agent's prompt is an injection sink and its tools and token are what the attacker gets.

- Which triggers expose it: `pull_request_target`, `issue_comment`, `issues` and `workflow_run` run for outsiders; "it only runs for maintainers" is true only if the workflow checks the author itself.
- Data reaches the prompt without a visible `${{ }}` in the prompt: through `env:`, through a file the agent reads (the PR diff, `README`, an issue body fetched with `gh`), or through error logs. Follow `env:` into the prompt field, not only the prompt text.
- Power the agent has: a write token or secrets in its environment, shell tools (an allowlist of `echo` still allows `echo $(env)`), a wildcard tool list (`Bash(*)`), flags that switch off the sandbox (`danger-full-access`, `--yolo`), the PR head checked out next to the base repository's secrets.
- Its output used as code: `eval`, `bash -c` or a step that applies a patch the agent wrote without review.
- Fix by removing power rather than filtering text: read-only token, no secrets in the job, no shell, outsiders' runs gated by a label a maintainer adds, the agent's output treated as untrusted input.

## Release

- Publishing with a stored API token where trusted publishing is possible, or `id-token: write` granted to more than the publish job ([release.md](../../tabby/development/library/shared/release.md)).
- The published artifact is rebuilt in the publish job instead of being the one that was tested: build once, upload the artifact, publish that file.
- A release triggered by any tag from any branch, with no environment protection, on a repository where many people can push tags.
- Secrets, `.env` files, test fixtures or local configuration inside the sdist or wheel: list the archive (`unzip -l dist/*.whl`, `tar tf dist/*.tar.gz`) and read it.
- Generated files committed without the command that regenerates them, so a reviewer cannot tell an edited file from a generated one.

Report as in [reporting.md](reporting.md).
