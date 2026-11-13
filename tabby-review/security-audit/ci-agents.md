# Security audit: AI agents in CI workflows

Read [ci-workflows.md](ci-workflows.md) first for the threat model and the workflow classes; this page is for a workflow step that runs a model-driven agent.

A workflow that runs a model-driven agent (a review bot, an issue triager; `claude-code-action`, Gemini CLI, Codex, `actions/ai-inference`) treats text as instructions. The injection sink is the agent's input and its power is whatever tools and token the job gives it. Review in this order.

**1. What can the attacker put in front of it?** Any of these reaches the model, and several have no `${{ }}` in the prompt:

- a direct expression in `prompt`, `direct_prompt`, `override_prompt`, `system-prompt`, `prompt-file`, `claude_args` or `codex-args`. For an agent, `with:` is a sink even though it is not a shell;
- through `env:`: `ISSUE_BODY: ${{ github.event.issue.body }}` at workflow, job or step level, and a prompt that says "read `$ISSUE_BODY`". The prompt looks clean and the usual advice to move expressions into `env:` makes it worse here. Follow each `env:` name into the prompt. Also `echo "X=..." >> $GITHUB_ENV` in an earlier step;
- fetched at run time: a prompt that tells the agent to `gh issue view N`, `gh pr diff` or `gh api`, with only the number interpolated. The YAML has no attacker text at all, but the agent reads the body;
- files the agent reads from a checked-out pull request, which is why `pull_request_target` plus a head checkout is worse for an agent than for a build, and why project instruction files (`CLAUDE.md`, `AGENTS.md`, `.cursorrules`, Copilot instructions) from a fork are trusted context. Protect them with `CODEOWNERS` and require review for changes to them;
- CI output: error logs, test output, `workflow_dispatch` inputs or step outputs passed to a "fix the build" agent. A test or compiler error can contain whatever the contributor made it print.

**2. What can it do?** The cost of a successful injection is the agent's reach:

- Shell: `Bash(*)` and a broad `Bash(npm:*) Bash(curl:*)` list, `danger-full-access`, `safety-strategy: unsafe`, sandbox switched off, `--yolo`. A "restricted" list that includes an expandable command (`echo`, `cat`, `printf`) is only restricted by name: the shell runs `$(env)` inside `echo $(env)` first. That bypass was demonstrated against Gemini CLI in the source; for the other agents it is likely but was not confirmed there.
- The token and secrets in its environment: `GITHUB_TOKEN` write scopes, API keys, the base repository's secrets in a `pull_request_target` job.
- Who may trigger it: `allowed_non_write_users: "*"` (Claude Code Action) and `allow-users: "*"` (Codex) let anyone; so do `allowed_bots: "*"` and `allow-bots`. With the field absent the defaults in both are write-access users only, so absence is not a finding. Gemini CLI and AI Inference have no such field, so the workflow trigger and an author check are the only gate. Settings can also live in a file (`settings:` path) the workflow does not show.

**3. What happens to its output?** `eval`, `exec`, an unquoted `$(...)`, or a script that formats the model's JSON into a command line, in a later step that holds the token. The consuming step is the finding; the model is just an untrusted source. Posting the output as a comment, writing it to a file or testing it in `if:` is not code execution (the comment can still carry markup or links).

**Severity.** A sandbox or allowlist weakness, or a wildcard user list, with no injection path is Info or Low; with one, it raises the injection finding. The strongest combinations are an outsider trigger (`pull_request_target`, `issues`, `issue_comment`), a direct or indirect injection path, shell, and secrets in the job. Fork `pull_request` runs without secrets and `push`/`workflow_dispatch` runs lower it.

**Fix by removing power**, not by filtering text: a read-only token, no secrets in the job, no shell (or a fixed list of non-expandable tools), runs for outsiders gated on a label a maintainer adds or an author check, sandbox on, the output treated as untrusted input and validated against a schema before anything acts on it. Do not rely on the model refusing; in the documented attempt on a repository using `CLAUDE.md` poisoning, the agent flagged it and the workflow was still vulnerable.

**Field names changed.** `claude-code-action` v0.x used `direct_prompt`, `override_prompt`, `allowed_tools` (comma-separated), `disallowed_tools`, `custom_instructions`; v1 uses `prompt` and `claude_args` (`--allowedTools "Bash(a:*) Bash(b:*)"`, space-separated). Files pinned at `@v1` or a SHA can still carry the old names, so read the names in the file, not the ref. A search for one set misses the other. Other agents' fields differ; read the action's `action.yml` and README for the version pinned rather than trusting a list.

**Hidden agents.** Resolve `uses: ./path` (composite action: read its `action.yml`; JavaScript and Docker actions have no steps to read) and job-level `uses:` (reusable workflow) one level deep and say which references you did not follow. A composite action has no `secrets` context, so `${{ secrets.X }}` written in one is empty and a secret there arrived as an input; a reusable workflow gets secrets named by the caller or all of them with `secrets: inherit`, which raises severity. Inheritance does not pass down a second hop. Name the line that grants the secret.

## Report

Report each finding in the per-finding form in [ci-workflows.md](ci-workflows.md), with the agent's tool permissions as the impact.
