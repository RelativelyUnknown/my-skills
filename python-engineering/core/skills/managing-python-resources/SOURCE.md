# Source

- Upstream: https://github.com/wshobson/agents
- Path: `plugins/python-development/skills/python-resource-management/`
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d
- Licence: MIT, Copyright (c) 2024 Seth Hobson. The upstream `LICENSE` is kept next to this file and applies to the adapted material.
- Adapted: 7 November 2026.

## What changed

- Rewritten as short rules; the upstream body (243 lines) and `references/details.md` (183 lines) are condensed to about 25 lines and one examples file.
- Dropped as restating the language docs: the protocol-method primer and the logging-based timing block.
- Added after running each one in the container (Python 3.13): `@contextmanager` needs `try`/`finally`; `ExitStack.pop_all`; generators that hold a resource and `contextlib.closing`; `subprocess.run` versus `Popen.communicate` timeouts; `ResourceWarning` is silent unless enabled; cancellation runs async cleanup.
- Code examples use stand-in resources instead of psycopg, asyncpg and structlog, so each block runs as written.
