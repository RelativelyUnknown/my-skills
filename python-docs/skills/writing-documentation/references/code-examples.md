# Code examples

Readers copy examples before they read prose. A wrong example costs more than a wrong sentence.

## Rules

- **Runs as written.** Include imports, setup and teardown. A fragment is labelled as one ("Inside your `main()` function:") and shows enough context to place it.
- **Tested.** Doctests run with `pytest --doctest-modules`; Markdown examples run through a test that extracts code blocks (for example `pytest-examples`, `sybil`, or a small test that executes README fences); Sphinx projects can use `sphinx.ext.doctest`. An example outside a test needs a reason.
- **Minimal.** Show one concept. Remove parameters that keep their defaults, logging set-up, error handling unrelated to the point, and commented-out alternatives.
- **Realistic.** Names from the domain (`orders`, `customer_id`), not `foo`, `bar`, `x` (except in pure language mechanics). Values that look plausible. Fictional companies and `example.com` domains.
- **Current.** Uses the APIs and idioms the docs recommend today, at the project's minimum supported version.
- **Safe.** No real credentials, internal hostnames or personal data. Read secrets from the environment and show the variable name.
- **Output shown** when the reader needs it to confirm success or to understand the result. Mark it as output, separate from the code.

## Shell commands

```console
$ uv add httpx
Resolved 7 packages in 120 ms
```

or, when readers will copy the block:

```bash
uv add httpx
```

- Pick one convention per docs set. If prompts are shown, use a `console` block so copy buttons strip them, and never mix prompts into `bash` blocks.
- One command per line; avoid `&&` chains that hide which step failed.
- Long commands break with `\` at clear points, one option per line.
- Platform differences go in tabs or labelled blocks (macOS and Linux, Windows PowerShell), not prose like "on Windows, replace `/` with `\`".

## Placeholders

- Mark them consistently: `<API_URL>`, `<YOUR_TOKEN>`. Do not use `xxx`, `your-token-here` and `<token>` in one docs set.
- Explain each placeholder right after the block: "Replace `<API_URL>` with your server's URL, for example `https://api.example.com`."

## Annotating examples

- Explain in the prose before or after the block, not with a comment on every line.
- Comments inside code explain non-obvious lines only, in the same voice as the docs.
- When an example has several important lines, refer to them by what they do ("The `with` block closes the connection"), or use the docs tool's line annotations.

## Python specifics

- Doctest prompts (`>>>`, `...`) only in docstrings and doctest pages; regular pages use plain code blocks.
- No trailing `>>>` prompt; use `...` continuation lines sparingly (Python devguide).
- Show positional-only `/` and keyword-only `*` markers in signatures in reference docs (Python devguide).
- Type hints in examples when they help the reader, matching the project's style.
