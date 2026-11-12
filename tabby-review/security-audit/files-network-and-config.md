# Audit classes: files, network, secrets and configuration

Every hit needs the trace from attacker-controlled input to the sink ([process.md](process.md)). Settings, environment variables and the project's own constants are server-controlled: they are not a path, URL or command source unless a secret is committed or the value is built from user input. Fixes are in `tabby/development/code/security-basics.md`.

## Paths, uploads, archives

- **Paths:** `open(os.path.join(base, user))` (an absolute `user` replaces `base`; `..` climbs out), `send_file(user_path)`, `Path(user).read_text()`, `shutil.copy(user_src, user_dst)`. A string `startswith(base)` check is itself a finding: `/app/files_evil` passes for `/app/files`. The check that holds is resolving, then `is_relative_to`. Symlinks inside an upload or archive defeat a name check.
- **Uploads:** the name, size, type and content are all attacker-controlled. Look for a client filename used as a path, a type taken from the header or extension, storage under the web root, HTML or SVG served inline (script runs on your origin), no size cap. Re-encoding images and mode `0o640` are hardening.
- **Archives:** `tarfile.extractall` without `filter="data"` (the default filter arrives in 3.14; 3.13 warns); `zipfile.extractall` or a hand-written loop without a per-member path check; no cap on total size or file count. `zipfile` stops reading at a member's declared size, so summing `infolist()` sizes is a valid pre-check in CPython (checked with a forged header).
- **Temp files and permissions:** `tempfile.mktemp`, a fixed name in `/tmp`, `os.chmod(path, 0o777)`, `os.umask(0)`, private keys at `0o644`. A check followed by an open (TOCTOU): open first and test the descriptor.

## Server-side requests (SSRF)

- **Look:** a URL from the request fetched by `requests`, `httpx`, `urllib`, `aiohttp`, a webhook sender, an image or link-preview proxy, a PDF renderer.
- **Finding:** the caller controls the **host or scheme**. Controlling only the path of a fixed host is not SSRF. The impact is what the server can reach that the caller cannot: internal services that trust localhost, the cloud metadata service (`169.254.169.254`, `169.254.170.2`, `metadata.google.internal`), `file://` or other schemes.
- **A check is weak when** it inspects the URL string. The OS resolver turns `2130706433`, `0x7f000001`, `0177.0.0.1` and `127.1` into `127.0.0.1` (all four checked), while `ipaddress.ip_address` rejects them; `::ffff:127.0.0.1` is the same host in IPv6 form. It is also weak when it validates, then lets the HTTP library resolve again (rebinding), or follows redirects (`allow_redirects=False` and revalidate each hop).
- **A check holds when** it resolves with `getaddrinfo`, requires `ip.is_global` for every returned address (private, loopback, link-local, IPv4-mapped and carrier-grade NAT `100.64.0.0/10` are all `is_global == False`), and connects to that address. Rewriting the URL to the IP and sending a `Host` header breaks TLS verification (`SSLError`, checked); keep the hostname and force the connection address instead.
- **Infrastructure side:** IMDSv2 on AWS and egress rules are the control that does not depend on the app. A client-side fetch in a browser is not SSRF.

## Cryptography and secrets

- `random` for tokens or keys (use `secrets`); `uuid.uuid1()` as an unguessable ID (it carries a timestamp and a node ID; `uuid4` is random); MD5 or SHA-1 for anything security-related (checksums and cache keys are fine).
- Encryption: use the `cryptography` package's `AESGCM`, `ChaCha20Poly1305` or `Fernet`. Findings: ECB mode, CBC without a MAC (padding oracle), a fixed or counter nonce that is not persisted, a nonce reused with the same key, a key built from a short password without a KDF, home-made schemes.
- TLS: `verify=False`, `ssl._create_unverified_context`, `check_hostname = False`, `urllib3.disable_warnings()`. Use `ssl.create_default_context()` and leave the cipher list alone.
- Key and secret handling: committed `.env` and keys, secrets in logs, URLs, error pages, container images or a settings object's `repr`; one key for every purpose; no way to rotate (tag ciphertext with a key version).
- Timing: `==` on tokens, MACs or password hashes (use `hmac.compare_digest`).

## Fail-open defaults and exposure

A missing or broken setting must stop the process or fall to the strict behaviour. Look for:

- Fallback secrets: `os.environ.get("SECRET_KEY", "dev")`, `getenv("TOKEN") or "changeme"`, default credentials (`admin/admin`, `postgres/postgres`, in `docker-compose.yml` and Kubernetes secrets, where base64 `YWRtaW4=` is `admin`).
- Switches that default to unsafe: auth off when an env var is unset, `except Exception: return True` or `pass` around a permission check, an `authenticate` that returns `None` on error and a caller that treats it as success.
- Debug and diagnostics: `app.run(debug=True)` (the Werkzeug debugger runs code), Django `DEBUG = True`, `ALLOWED_HOSTS = ["*"]`, stack traces or `str(e)` in responses, `/debug`, `/env`, `/config`, `/metrics`, `.git` or `.env` reachable, directory listing (`python -m http.server` is not a production server).
- Exposure: responses that return more fields than the caller may see; sensitive responses without `Cache-Control: no-store`; cache entries holding sensitive objects.
- Logging: passwords, tokens or personal data written to logs; whole request bodies logged on error (log flooding).

## Frameworks

- **Django:** `DEBUG`, `ALLOWED_HOSTS`, `SECRET_KEY` committed, `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` false, `SecurityMiddleware` or `CsrfViewMiddleware` missing; `.raw()`, `.extra()`, `RawSQL`; `|safe`, `mark_safe`, `{% autoescape off %}`; `@csrf_exempt`; `fields = "__all__"`.
- **Flask:** short or hard-coded `secret_key`; `debug=True`; `render_template_string(user_text)`; `Markup(user_text)`; no `CSRFProtect`; session cookie flags.
- **FastAPI/Starlette:** a route without the `Depends` its siblings have; a function behind `Depends(get_current_user)` whose dependency does not actually validate; a response that returns an ORM object or dict (extra fields leak); `CORSMiddleware` with `*` and credentials; an `UploadFile` read whole into memory; `StaticFiles` over a directory holding more than assets.

## Containers (a service's Dockerfile, compose file, manifests)

No `USER` (runs as root); `:latest` or an unpinned base image; secrets in `ARG`, `ENV` or `COPY .env` (all visible in `docker history`; build secrets belong in BuildKit `--mount=type=secret`); no `.dockerignore` excluding `.env`, keys and `.git`; at runtime `--privileged`, `--cap-add`, a mounted `/var/run/docker.sock` (root on the host), `-v /:/host`, `--network=host`.

## Limits and parsing

Unbounded request bodies, uploads, decompression, page sizes, or a regex with nested quantifiers on attacker input are findings only where a small input from a low-trust caller causes large amplification (an unauthenticated endpoint pinned by one request). Otherwise they are hardening notes, as are missing rate limits and missing security headers.
