# Audit classes: defaults, configuration and exposure

Every hit needs the trace from attacker-controlled input or a reachable deployment state to the decision it affects ([process.md](process.md)). Settings, environment variables and the project's own constants are server-controlled: they are not a path, URL or command source on their own, but what they default to is the question here. Fixes are in `tabby/development/code/security-basics.md`. Built from Trail of Bits' `insecure-defaults` and `sharp-edges` skills and the Sentry misconfiguration references (see `THIRD_PARTY_NOTICES.md`), with claims checked by running code where marked.

## Fail-open defaults

A missing or broken setting must stop the process or fall to the strict behaviour. Two kinds of candidate, judged differently:

- **Configurable:** a lookup with a fallback. It is a bug only if the application actually runs with the fallback. `os.environ.get("SECRET_KEY", "dev")` runs; `os.environ["SECRET_KEY"]` stops with a `KeyError`, which is fail-secure. Before filing it, check how the deployment supplies the variable (Dockerfile `ENV`, compose, Kubernetes manifests, CI, a `.env.example`): every manifest that sets it lowers the severity, none that does is the worst case, and an unclear answer counts as reachable.
- **Unconditional:** insecure as written, with no setting involved: a hardcoded signing key, `bootstrap_admin()` that seeds `admin`/`admin123`, a bucket created `public-read`, `0o666` on a key file. About half of real findings are this kind, and a missing environment variable is no reason to refute one.

A candidate becomes a finding when each step holds: the file is reachable in production; the insecure value is the one that runs; the value is actually insecure; it reaches a security decision (name the sink); and for a configurable one, deployment does not always supply it. An incomplete trace means refuted. By category:

- **Fallback secrets:** a default that feeds signing, encryption, sessions or tokens (`getenv("TOKEN") or "changeme"`, `SECRET_KEY = "dev-secret"`). Not: values generated at random on each boot, cache keys, correlation ids.
- **Default credentials:** a login a running deployment can use, including accounts seeded on first boot and connection strings with a password in a fallback (`docker-compose.yml`, Kubernetes secrets, where base64 `YWRtaW4=` is `admin`). Not: accounts created disabled or with a forced reset, credentials in a README or test fixture ("a credential in prose is one nobody can use; one in `bootstrap_admin()` is a login").
- **Fail-open switches:** read the default, not the flag name: `REQUIRE_AUTH` defaulting to `"false"` requires nothing; an `except Exception: return True` or `pass` around a permission check; an `authenticate()` that returns `None` on error while the caller treats `None` as success. Not: switches whose unconfigured value is the secure one, or flags that are never consulted where the control is enforced.
- **Weak cryptography:** the algorithm alone is never the finding; trace to the use. `hashlib.md5` over a cache key is fine, over a password is not. See [files-network-and-crypto.md](files-network-and-crypto.md).
- **Permissive access:** ask who gains access, not how wide the value looks: `0o644` on a CDN asset is right, `0o666` on a key file is not; `os.umask(0)`; CORS `*` with credentials; a public bucket. Not: a deliberate public endpoint with a stated reason.
- **Debug and diagnostics:** needs both halves, on by default and a path to a reader who should not see it: `app.run(debug=True)` (the Werkzeug debugger runs code), Django `DEBUG = True`, `ALLOWED_HOSTS = ["*"]`, a traceback or `str(e)` in a response, `/debug`, `/env`, `/config`, `/metrics`, `.git` or `.env` reachable, directory listing (`python -m http.server` is not a production server). A verbose log written to a file only an operator reads is neither.
- **Exposure:** responses that return more fields than the caller may see; sensitive responses without `Cache-Control: no-store`; sensitive objects in a shared cache; passwords or tokens in logs, and whole request bodies logged on error.

Find the project's own configuration wrappers first (`get_setting("X", "default")`, a `Settings` class with defaults): a codebase that reads everything through one barely matches generic patterns. Say which patterns you searched. A search that matches nothing looks the same as a clean result, and in `grep -E` use `[[:space:]]` and `[0-9]` rather than `\s` and `\d`, which some builds silently ignore. Committed secrets are a job for a scanner such as gitleaks or trufflehog; a linter such as ruff's `S` rules is better than a hand search for fixed patterns.

## Security parameters and silent failure (API and configuration review)

When reviewing a library's API or a configuration schema, put yourself in three seats: the **attacker** who controls a value, the **lazy developer** who copies the first example, and the **confused developer** who swaps two arguments. For every security-relevant choice ask: what happens with zero, empty, `None`, negative, a value of the wrong type, and an error?

- **Zero, empty, None, negative.** A lifetime or timeout of `0` that means "accept everything" or "never expires"; a negative timeout that makes `now - created > timeout` never true; `max_attempts=0` or `-1` meaning unlimited; `if not key: return True` (no key means skip the check); `stored == ""` equal to an empty submitted password (`"" == ""` is true, and so is `hmac.compare_digest(b"", b"")`, both checked). Reject them: a security number must be positive and have both a minimum and a maximum; an empty secret must be refused.
- **Switches.** A boolean that disables a control (`verify_ssl`, `require_auth`) is a cliff; double negatives (`disable_auth: false`) invite mistakes. Config parsers surprise: PyYAML's `safe_load` turns `no`, `NO`, `off` into `False` (the "Norway" problem, checked), a typo such as `fasle` becomes the truthy string `"fasle"`, and `bool("false")` is `True` (checked). Validate the type, reject unknown keys, and reject contradictory pairs (`require_auth: true` with `allow_anonymous: true`). State the precedence when a file, an environment variable and a flag can all set one value.
- **Defaults are not validation.** A secure default protects only callers who omit the argument. A constructor or settings class takes `algorithm`, `mode`, `cipher`, a lifetime, a hostname or a URL from the caller: validate them against an allowlist and a range at construction, so an insecure value is refused when it is created, not when it is used.
- **The caller picks the mechanism.** Any parameter that selects a security mechanism and can come from input (`alg` in a JWT header, a cipher or hash name) lets an attacker downgrade it. Fix the algorithm in code.
- **Silent failure.** A verify function that returns `False` while a caller discards the result; one library raises on failure and another returns a bool, and developers mix them up; `except` blocks that log and carry on as if authentication succeeded; a parse error replaced by a default.
- **Stringly typed security.** Roles or permissions kept as comma-separated strings (`perms += ",admin"`), matched by substring (`"admin" in role` matches `readonly_admin_viewer`) or with any-match logic. Use an `Enum` and `frozenset` equality.
- **Primitive-typed secrets.** Keys, nonces and ciphertexts that are all `bytes` can be swapped without an error. Wrap them in distinct types, and generate the nonce inside the function.
- **Severity for an API review:** critical when the default or obvious usage is insecure; high when an easy misconfiguration breaks security; medium when an unusual one does; low when only deliberate misuse does. Documentation lowers the severity but does not excuse the design.

## Frameworks

- **Django:** `DEBUG`, `ALLOWED_HOSTS`, `SECRET_KEY` committed, `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` false, `SecurityMiddleware` or `CsrfViewMiddleware` missing; `.raw()`, `.extra()`, `RawSQL`; `|safe`, `mark_safe`, `{% autoescape off %}`; `@csrf_exempt`; `fields = "__all__"`.
- **Flask:** short or hard-coded `secret_key`; `debug=True`; `render_template_string(user_text)`; `Markup(user_text)`; no `CSRFProtect`; session cookie flags.
- **FastAPI/Starlette:** a route without the `Depends` its siblings have; a function behind `Depends(get_current_user)` whose dependency does not actually validate; a response that returns an ORM object or dict (extra fields leak); `CORSMiddleware` with `*` and credentials; an `UploadFile` read whole into memory; `StaticFiles` over a directory holding more than assets.

## Containers (a service's Dockerfile, compose file, manifests)

No `USER` (runs as root); `:latest` or an unpinned base image; secrets in `ARG`, `ENV` or `COPY .env` (all visible in `docker history`; build secrets belong in BuildKit `--mount=type=secret`); no `.dockerignore` excluding `.env`, keys and `.git`; at runtime `--privileged`, `--cap-add`, a mounted `/var/run/docker.sock` (root on the host), `-v /:/host`, `--network=host`.

## Limits and parsing

Unbounded request bodies, uploads, decompression, page sizes, or a regex with nested quantifiers on attacker input are findings only where a small input from a low-trust caller causes large amplification (an unauthenticated endpoint pinned by one request). Otherwise they are hardening notes, as are missing rate limits and missing security headers.
