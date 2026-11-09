# Debugging

- Reproduce first: a failing test, or the smallest failing input. A fix starts red ([testing.md](../testing/testing.md)).
- State the cause of a bug in one sentence before fixing it; if you cannot, investigate.
- Never special-case inputs or hardcode expected outputs. No sleeps, retries or longer timeouts until the cause of a race is known. Do not pin, downgrade or swap a dependency, or edit `sys.path`, to get past an error without explaining why.
- After two or three failed attempts at the same fix, stop guessing: re-read the code, state a hypothesis, then act.
- Do not silence the tool that found it: no `# type: ignore`, `# noqa`, `cast()`, `Any`, and no loosened linter, type-checker or pytest config. If an ignore is truly needed, name the code (`# type: ignore[arg-type]`) and say why in a comment.
