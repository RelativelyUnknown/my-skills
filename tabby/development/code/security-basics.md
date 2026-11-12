# Security basics

Security bugs come from one mistake: data crossing into something that interprets it (SQL, a shell, a deserializer, a template, a URL fetcher) or a secret crossing out. Ask of each boundary: who controls this value, and what will it be treated as? Keep data as data (parameters, argument lists, safe parsers) and keep secrets out of code, logs and URLs. These are the rules to write by; the audit side is in `tabby-review`. Web services also read [apis/shared/security.md](../application/apis/shared/security.md).

Environment variables, settings and the project's own constants are trusted. Request data, uploads, headers, cookies, queue messages from other parties and anything another user wrote are not.

## Interpreters

- SQL: bind values as parameters (`execute(sql, params)`, ORM filters, `text(":id")` with a dict). A table, column or sort order cannot be bound: choose it from an allowlist. Never build a query with an f-string, `%` or `+`, and do not pass request data as `filter(**kwargs)`.
- Commands: prefer a library call over a subprocess (`os.makedirs`, not `mkdir`). Otherwise an argument list with `shell=False`, and `--` before a value that could start with `-`.
- `eval`, `exec`, `__import__`, `getattr(module, name)()` on input: parse the format instead (`json`, `ast.literal_eval` for Python literals).
- Never load `pickle`, `marshal`, `shelve`, `joblib`, `pandas.read_pickle`, `numpy.load(allow_pickle=True)` or a `torch.load` of an untrusted file from anything an outsider can write. `yaml.safe_load`, never `yaml.load` (PyYAML 6 requires a `Loader`, and `Loader` and `UnsafeLoader` execute code).
- Templates: pass user text as a variable, never as the template (`render_template_string(user_text)` is code execution). `jinja2.Environment()` does not autoescape; use `select_autoescape()` or the framework's. Mark text safe (`|safe`, `Markup`, `mark_safe`) only after escaping it yourself.
- XML from outside: `defusedxml`. The standard library parsers expand entities.

## Files and archives

- A user-supplied name never becomes a path by joining: `os.path.join(base, "/etc/passwd")` is `/etc/passwd`. Resolve and compare with `is_relative_to`: `(base / name).resolve().is_relative_to(base.resolve())`. A `startswith` on strings accepts `/app/files_evil` for `/app/files`.
- `tarfile.extractall(path, filter="data")` (Python 3.12 and recent patch releases of 3.8 to 3.11; the default from 3.14). For zip, check every member path and cap the total size and file count from `infolist()`; `zipfile` stops at the declared size.
- Uploads: generated filename, stored outside the web root, size cap, type from the content and not the header, no inline serving of HTML or SVG.
- `tempfile.mkstemp`, `NamedTemporaryFile` or `TemporaryDirectory`; never `mktemp` or a fixed name in `/tmp`. Private files are mode `0o600`.

## Outbound requests

A URL from outside is fetched only after: an allowlist of hosts when you can have one; scheme `http` or `https`; the host resolved with `socket.getaddrinfo`, and every returned address rejected unless `ipaddress.ip_address(addr).is_global` (this covers loopback, private, link-local, the `169.254.169.254` metadata address, carrier-grade NAT and IPv4-mapped IPv6); no automatic redirects, each hop validated again. Check the resolved address, never the string: the OS resolver accepts `2130706433`, `0x7f000001` and `127.1` as `127.0.0.1`, and `ipaddress` does not. Connect to the address you validated and keep the hostname in the URL, so TLS still verifies; putting the IP in the URL breaks certificate checks. Where you can, also filter egress outside the app.

## Identity

- Passwords: Argon2id (`argon2-cffi`, `pwdlib`), scrypt or bcrypt through the framework's hasher; never MD5, SHA-1 or a bare SHA-256. Compare secrets and MACs with `hmac.compare_digest`. If the user does not exist, still hash a dummy password so timing and messages do not reveal accounts.
- Tokens, session ids, reset links: `secrets.token_urlsafe(32)`; `uuid1` is not random. A new session id at login and at every privilege change. Reset links are single use, expire, and are not logged.
- JWT: `jwt.decode(token, key, algorithms=[...], audience=..., issuer=...)` with a pinned list; never `verify_signature=False`.
- Authorize on every path to the data, and at the object: scope the query to the owner or tenant (`get(pk=pk, owner=request.user)`). Hiding a button or checking only in the UI is no check. Write the test: user B asking for user A's object gets 403 or 404.
- Accept only the fields a caller may set (a model without `is_admin`), and return only the fields a caller may see (a response model, never `obj.__dict__`).
- A security number (a lifetime, an attempt limit, a timeout) is positive and has a minimum and a maximum; `0`, a negative number or an empty secret is rejected, never read as "off" or "unlimited". Roles and permissions are `Enum` members or a `frozenset`, compared by equality, never by substring or in a comma-separated string. A password is rejected when it is too long, not truncated.
- Type hints are not validation: `request.json()["id"]` can be a list, a dict or a float. Parse request data into a typed model at the edge.

## Money, state and races

- A balance, stock count, coupon or counter changes in one statement or one locked transaction: `UPDATE ... SET balance = balance - :n WHERE id = :id AND balance >= :n`, or `SELECT ... FOR UPDATE`. A `threading.Lock` protects one process only. Locks taken in a fixed order do not deadlock.
- The server computes prices, totals and discounts. A quantity or amount is checked for sign and range; use `Decimal` or integers for money.
- A retry-safe endpoint stores its idempotency key with a unique constraint; read-then-insert races with itself.
- Status fields change through one function that checks the allowed transitions ([tabby-review/state-machines.md](../../../tabby-review/state-machines.md)).

## Secrets and errors

- Secrets come from the environment or a secrets manager. No `os.environ.get("KEY", "dev-secret")` fallback; a missing secret stops the process. Keep `.env` and keys out of git, images (`ARG`, `ENV`, `COPY .env`) and logs.
- A security check fails closed: if the permission service errors, deny. No `except Exception: return True` or `pass` around an authorization step.
- Clients get a generic error and an id; the traceback goes to the log. Debug mode is off outside development (`app.run(debug=True)` serves a code-running debugger).
- Never log passwords, tokens, keys or card numbers. Escape CR and LF in user values written to logs, or use structured logging.
- Dockerfiles for services: a non-root `USER`, a pinned base image, a `.dockerignore` that excludes `.env`, keys and `.git`.
