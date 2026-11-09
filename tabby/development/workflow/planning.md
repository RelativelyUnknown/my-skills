# Planning a change

- Before a non-trivial change, state the approach in a few lines. Read the code and its callers first; find every caller (code, tests, scripts, config, docs) before renaming or changing a signature.
- Ask first when requirements are ambiguous and a wrong guess is expensive. If a rule conflicts with the request, say so and ask.
- Smallest diff that solves the problem properly. No unrelated refactors, renames or reformatting; mention what you noticed. No summary, changelog or demo files nobody asked for; delete scratch files. Do not edit CI, lint or pytest config unless that is the task.
- Prefix commands with the project's `runner`. Keep the project's existing tools (poetry, black, pyright, ...); never add a second tool for the same job. Never install a tool or dependency silently.
- **Stop and report** instead of working around a problem when a test contradicts the spec or task; the task cannot be done properly with the code and dependencies available; the fix needs a new dependency, a public API change or a deleted file; or you catch yourself justifying test-specific behavior with a reason like "backward compatibility".
- Do not commit, push or run destructive commands (`git reset --hard`, `rm -rf`, force-push, dropping tables) unless asked. Never skip hooks with `--no-verify`. Deleting data or files, dropping columns, changing a public API or irreversible migrations need approval first.
