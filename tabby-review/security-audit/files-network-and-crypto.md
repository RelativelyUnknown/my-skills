# Audit classes: files, network and cryptography

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
- A hash is not a key-derivation function (`sha256(password)` as a key is fast to brute force; use `hashlib.scrypt`, PBKDF2 or Argon2), and encryption is not password storage (one stolen master key exposes every password; store a salted one-way hash).
- Decryption that tells the caller *why* it failed ("invalid padding" against "MAC mismatch") is a padding oracle; fail with one error, and prefer authenticated encryption.
- Secrets in native code: general bignum libraries (GMP's `mpz_powm`) are not constant-time, and a freed buffer is not wiped; secrets belong in code written for it (libsodium, OpenSSL's constant-time paths, the `cryptography` package).
