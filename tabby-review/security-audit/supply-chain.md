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

## Release

- Publishing with a stored API token where trusted publishing is possible, or `id-token: write` granted to more than the publish job ([release.md](../../tabby/development/library/shared/release.md)).
- The published artifact is rebuilt in the publish job instead of being the one that was tested: build once, upload the artifact, publish that file.
- A release triggered by any tag from any branch, with no environment protection, on a repository where many people can push tags.
- Secrets, `.env` files, test fixtures or local configuration inside the sdist or wheel: list the archive (`unzip -l dist/*.whl`, `tar tf dist/*.tar.gz`) and read it.
- Generated files committed without the command that regenerates them, so a reviewer cannot tell an edited file from a generated one.

Report as in [reporting.md](reporting.md).
