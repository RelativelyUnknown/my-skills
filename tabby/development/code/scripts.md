# Scripts and command-line tools

A script is code someone will run again. Make it safe to rerun and honest about failure. Use features available at the Python target.

## Shape

- Module docstring is the `--help` description. `def main(argv: list[str] | None = None) -> int:` does the work and returns the exit code; the file ends with `if __name__ == "__main__": raise SystemExit(main())`.
- Standard library first (`argparse`, `pathlib`). If a package is needed, declare it in the file so `uv run script.py` installs it:

  ```python
  # /// script
  # requires-python = ">=3.12"
  # dependencies = ["httpx"]
  # ///
  ```

## Behavior

- Paths are `Path` (`type=Path`). Results go to stdout; errors and diagnostics go to stderr (`print(..., file=sys.stderr)`, or `logging`).
- Exit codes: 0 success, 1 the task failed (missing file, bad data), 2 usage error (argparse does this). Helpers raise; only `main` turns an exception into a message and an exit code.
- Anything that deletes or rewrites gets `--dry-run`, which prints what would change and changes nothing.
- Rewrite files atomically: write a temporary file in the same directory, then `os.replace` it over the original. Never truncate the original first.
- Running twice is safe and gives the same result.

## When people run it by hand

- `--help` says what it does and shows one example. Options are named and have defaults; a positional argument is for the one thing the command is about.
- A machine-readable output (`--json`, one object per line) when another program may read it; no colour or progress bars when stdout is not a terminal (`sys.stdout.isatty()`); progress goes to stderr.
- Never prompt when stdin is not a terminal; take `--yes` or fail with the exact flag to pass.
- Settings come from, in order of priority: flags, environment variables, a config file, defaults. Say so in `--help`.
- Ctrl-C ends the run without a traceback (exit code 130) and leaves no half-written file.

## Tests

Call `main([...])` directly; use `tmp_path` for files and `capsys` for output; assert on the exit code.

## Report

Show the command line, a dry run, a real run, and the exit code for a failure case.
