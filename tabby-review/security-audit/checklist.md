# Security audit: class checklist for Python

Use after mapping the boundaries ([process.md](process.md)). For each class: where to look, what makes it a finding, and the fix. A class with nothing to check is recorded as `clean` or `not applicable` in the final `Checked` line; a class you could not check is listed as unverified. Every hit still needs the trace from attacker-controlled input to the sink and an attempt to refute it.

## Injection

- **SQL.** `execute`, `executemany`, `text()`, `.raw()`, `.extra()`, `RawSQL`, `cursor.execute` with an f-string, `%`, `.format` or `+`. A value is a finding when attacker-controlled and not bound. A dynamic table, column or `ORDER BY` cannot be bound: allowlist it. An ORM filter with keyword arguments built from request data (`filter(**request.GET)`) lets the caller pick fields and lookups.
- **OS command.** `subprocess` with `shell=True`, `os.system`, `os.popen`; also argument injection into a safe call (a value starting with `-` passed to `git`, `tar`, `curl`; pass `--` before it). `shlex.quote` is for building a shell string, not a substitute for a list.
- **Template.** `render_template_string`, `Template(user_text)`, `jinja2.Environment()` rendering user-chosen template text (use `SandboxedEnvironment`, and prefer no user templates at all).
- **Header, log, LDAP, NoSQL, XPath.** Newlines in a header or log value; operators in a Mongo filter built from a JSON body; unescaped filter strings. Log injection is low unless logs are trusted for audit.

## Code execution and deserialization

- `eval`, `exec`, `compile`, `__import__` or `importlib.import_module` on input; `getattr(module, user_name)()`.
- `pickle`, `marshal`, `shelve`, `dill`, `jsonpickle`, `pandas.read_pickle`, `joblib.load`, `numpy.load(allow_pickle=True)`, `torch.load` without `weights_only=True`, `yaml.load` without a safe loader: remote code execution when the data crosses a trust boundary (uploaded model, cache shared with another tenant, queue message, file from a user).

## Files and paths

- `open(os.path.join(base, user_value))`: an absolute `user_value` replaces `base`, and `..` climbs out. Check with `Path(base).resolve()` and `(base / value).resolve().is_relative_to(base)`; use the framework's safe send (`send_from_directory`). Symlinks inside an upload or archive defeat a string check.
- Uploads: name, size, type and content are all attacker-controlled; store under a generated name outside the web root; do not trust the extension or `Content-Type`.
- `tarfile.extractall` and `zipfile.extractall` on untrusted archives (path traversal, links, bombs): use a `filter=` (`"data"`) on tar, check member names on zip, and cap total size and file count.
- `tempfile.mktemp` (race), predictable names in a shared `/tmp`, world-writable files, a check followed by an open (TOCTOU): open first, then verify through the descriptor.

## Outbound requests (SSRF) and redirects

- A URL from the user fetched by `requests`, `httpx`, `urllib`, a webhook delivery or an image proxy. A finding when it can reach internal addresses, link-local metadata (`169.254.169.254`), `file://` or other schemes. A hostname check is not enough: resolve it, reject private, loopback and link-local ranges, connect to the resolved address, and revalidate every redirect (`allow_redirects=False`).
- Open redirect (`redirect(request.args["next"])`): low, unless it feeds an OAuth or login flow.

## Output (XSS) and CSRF/CORS

- Escape hatches only: `|safe`, `Markup`, `mark_safe`, `format_html` given unescaped text, `autoescape=False`, plain `jinja2.Environment()` (autoescape is off by default), HTML built with f-strings, user text inside `<script>` or an `href`/`src` (`javascript:` URLs). Framework auto-escaping is a control; use of the escape hatch on user data is the finding.
- Cookie-authenticated state-changing endpoints need CSRF protection (Django has it on by default; Flask needs `CSRFProtect`; FastAPI has none). `@csrf_exempt` on such a view is a finding. CORS with `allow_origins=["*"]` plus credentials, or a reflected `Origin`, is a finding.

## Authentication and sessions

- Passwords: stored with Argon2, bcrypt or scrypt (or the framework's hasher), never MD5, SHA-1 or a bare SHA-256; compared with `hmac.compare_digest` when comparing secrets or MACs.
- Sessions and cookies: a new session id on login, `Secure`, `HttpOnly`, `SameSite`, an expiry, server-side logout.
- JWT: the signature is verified, `algorithms=[...]` is pinned (never `none`, never `verify_signature=False`), `exp`, `aud` and `iss` are checked, the secret is long and random.
- Reset and invite tokens: from `secrets`, single use, short expiry, not logged, not returned in a response that is cached; no user enumeration through different messages.
- Webhook receivers: verify the signature over the raw body, constant-time, with a timestamp window against replay.

## Authorization

- Every handler checks who the caller is and **whether this object is theirs**: `Model.objects.get(pk=pk)` or `session.get(Model, id)` with no owner or tenant filter is an IDOR. Admin and internal routes need their own check, not just a hidden URL.
- Mass assignment: `Model(**request.json)`, `update(request.data)`, a ModelForm or serializer with `fields = "__all__"`, a pydantic model that accepts `is_admin`, `role` or `owner_id`.
- Enforcement can sit in any layer (middleware, dependency, decorator, the query). Before marking a finding, follow the whole chain; then check that every other path to the same data has it too: background jobs, the CLI, GraphQL, websockets, export endpoints. DRF's default permission is `AllowAny` unless settings change it.

## Cryptography, secrets and exposure

- `random` for tokens or keys (use `secrets`); MD5 or SHA-1 for anything security-related (checksums and cache keys are fine); AES-ECB, a fixed or reused IV or nonce, home-made encryption; a key derived from a short password without a KDF.
- TLS off: `verify=False`, `ssl._create_unverified_context`, `check_hostname = False`.
- Secrets in code, committed `.env`, logs, exception text, URLs, error pages, container images, or a settings object's `repr`.
- Debug on in production: `app.run(debug=True)` (the Werkzeug debugger runs code), Django `DEBUG=True`, `ALLOWED_HOSTS = ["*"]`, a committed or default `SECRET_KEY`, tracebacks returned to clients, listing endpoints that return more fields than the caller may see.

## Fail-open defaults

Look for the place where a missing or broken setting switches protection off: an auth check skipped when an environment variable is unset, `except Exception: return True` around a permission check, a default password or key, `bind 0.0.0.0` by default, permissive CORS as the default, a feature flag that defaults to the unsafe side. A missing setting must stop the process or fall back to the strict behaviour.

## Parsing and resource limits

- XML from outside: `xml.etree`, `minidom` and `sax` are exposed to entity-expansion bombs; use `defusedxml`, or `lxml` with `resolve_entities=False, no_network=True`.
- Unbounded request bodies, uploads, decompression, page sizes and regexes with nested quantifiers on attacker input. Report as a finding only where a small input from an unauthenticated or low-trust caller causes large amplification; otherwise it is a hardening note.

## Business logic

- Check-then-write races on money, stock, coupons and balances: use one transaction with a row lock (`SELECT ... FOR UPDATE`), an atomic `UPDATE ... WHERE balance >= x`, or a unique constraint.
- A client-supplied price, quantity, currency or discount; negative amounts; a step that can be skipped by calling a later endpoint; a replayed request or webhook without an idempotency key. See [../state-machines.md](../state-machines.md) for status flows.

## Native code and AI features

- Rust, C, C++ or Zig parsing untrusted bytes: bounds, integer overflow, use after free, `unsafe` blocks; sanitizers and fuzzing ([../native-boundary.md](../native-boundary.md)).
- An LLM given untrusted text and also given tools, files or credentials: injected instructions can act with those rights. Model output must not reach `eval`, a shell, SQL or a file path unchecked.

## Footgun APIs worth a grep

`yaml.load`, `pickle.loads`, `tarfile.extractall`, `subprocess(..., shell=True)`, `os.system`, `eval`, `exec`, `tempfile.mktemp`, `verify=False`, `random.` near tokens, `hashlib.md5`, `jinja2.Environment(` without autoescape, `mark_safe`, `|safe`, `.raw(`, `.extra(`, `debug=True`, `Model(**request`, `allow_origins=["*"]`, `algorithms=` missing from `jwt.decode`.
