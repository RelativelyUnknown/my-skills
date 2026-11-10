# Commit messages and pull request descriptions

A commit message is read by someone running `git log` or `git blame` on a line they do not understand, long after the conversation that produced it is gone. Ask: what would they need to know that the diff does not show? Almost always that is why, and what else was considered or deliberately left out.

Commit only when asked ([planning.md](../development/workflow/planning.md)). These rules apply when you are asked to commit or to draft a message.

- The project's convention comes first: read `git log --oneline -20` and CONTRIBUTING. If it uses Conventional Commits (`fix(parser): ...`), a ticket prefix or a sign-off, match it; do not introduce one.
- Subject: imperative mood ("Add", "Fix", "Remove"), what changed for the reader of the log, about 50 characters and never past 72, no trailing period.
- Body only when the subject is not enough. It says why, not what: the problem, the cause for a bug fix, the constraint that shaped the choice. Wrap at 72 characters. The diff already says what changed and which files.
- Always a body for: a breaking change (what breaks, how to migrate), a security fix, a data migration, a revert (what is reverted and why), a workaround (what would make it unnecessary).
- One logical change per commit. A refactor and a behaviour change are two commits, so either can be reverted alone.
- Leave out: "this commit", "I", "we", "now", "as requested", the conversation, praise, emoji, and file lists.
- Reference an issue at the end (`Closes #128`) when one exists; never invent a number.

```
Fix timeout doubling on each retry

The retry loop passed the previous attempt's timeout to backoff(), so
the third attempt waited four times the configured value. Compute the
delay from the attempt number instead.

Closes #412
```

## Pull request description

Written for the reviewer, who decides in a minute where to look:

1. What changes for users or callers, in one or two sentences.
2. Why, and what was ruled out.
3. How it was verified: the commands run and their result; what was not verified.
4. What a reviewer should look at first, and anything deliberately left for later.

Follow the repository's pull request template when there is one. A new dependency, a public API change and a changed or removed test are always stated, never left for the reviewer to find.
