# Security basics

- No secrets in code, tests or fixtures; read them from the environment. Parameterized SQL only. No `shell=True` with interpolated values. No `eval`, `exec`, `pickle` or `yaml.load` on untrusted data.

Apply a line only when its condition holds.

## Untrusted input and secrets

- SQL built from data: bind values as parameters; allowlist any dynamic identifier.
- Shell command from input: pass an argument list with `shell=False`; validate the arguments.
- `pickle.loads` or `yaml.load` on external data: use JSON or `yaml.safe_load()`.
- `eval()` or `exec()` on input: parse the data format; `ast.literal_eval()` only when Python literals are meant.
- `verify=False` in production: keep TLS verification on; configure a trusted CA.
- `random` for tokens, a fast hash for passwords: use `secrets`; Argon2, bcrypt or scrypt.
- Credentials in logs, exception messages or URL query strings: redact them; keep them out of URLs.
