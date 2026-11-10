# Reuse before you write

Somebody has usually already written the thing well. Before writing a piece of code, ask which rung of the ladder answers the need, and take the highest rung that does the job well. What exists on each rung, job by job: [ecosystem.md](../ecosystem.md).

## The ladder

1. **What the project already uses** for the job: its validator, HTTP client, test tool, config loader. Use it. Do not add a second mechanism or rewrite working code to switch. A project with pydantic models gets a pydantic model; a project without pydantic does not get it for one function.
2. **The standard library**, when it does the job well.
3. **The community's standard library**: the libraries the ecosystem treats as its de facto standard for a job (an HTTP client, pydantic for structured input, pytest, numpy, SQLAlchemy, click or typer). Take one without apology when the standard library does not do the job well. This is a peer of rung 2, not an exception to it. In Rust, whose standard library is deliberately small, this rung is the norm (serde, thiserror, clap, tokio); in C++ it is fmt, abseil, Boost components.
4. **A niche library, or your own code.** The burden of proof is here. A niche library needs the vetting in [dependencies.md](../dependencies/dependencies.md). Your own code needs a reason: the job is a few lines, nothing above covers it, or the dependency would cost more than the code.

Rung 3 or rung 4? Signals, not a list: the ecosystem's own documentation points to it; most projects in that niche already depend on it; an organisation or several maintainers stand behind it; its API has stayed stable across versions; it is already installed because something you use needs it.

## Rules

- Do not hand-roll what rung 2 or 3 does well (HTTP with retries and pooling, time zones and free-form dates, hashing passwords, HTML sanitising, untrusted XML). Do not take a rung-3 library for a job rung 2 does in a few lines (two arguments to check: `if ... raise ValueError(...)`, not a model class).
- Never regex-parse a structured format: dates, URLs, HTML, JSON, CSV, versions. Quote for a shell, JSON or CSV with `shlex.quote`, `json.dumps` and `csv`, never by hand. Never write your own crypto, password hashing or token handling.
- Weigh the cost of a dependency: a dev-only one costs users nothing, a runtime one does. A library's dependencies become its users', so keep its base install small and put heavy ones in extras; an application or a single-file script may take more (PEP 723 `# /// script` declares a script's dependencies inline). Count install size, import time, transitive packages, licence and maintenance ([dependencies.md](../dependencies/dependencies.md)).
- When you add one, say so in the report: the package, the rung, the reason. Check that the exact name exists on the index before adding it.

## Validation ladder

- One function, one to three arguments: `if not ...: raise ValueError(f"unknown region {region!r}; expected one of {sorted(REGIONS)}")`
- A few related records you construct: a frozen dataclass with `__post_init__` checks
- Untrusted nested JSON, many models, coercion, error lists, schema output: pydantic, or the project's validator
- Config file: `tomllib` and a dataclass. Command-line arguments: argparse `type=` and `choices=`

Version-gated features follow [python-versions.md](python-versions.md).
