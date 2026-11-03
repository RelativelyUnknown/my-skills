# Web service security

Mapped to the OWASP API Security Top 10 (2023). Run through the relevant rows whenever a change touches auth, user input, uploads, CORS, rate limits or outbound requests.

## Contents

- OWASP API Top 10 checks
- Passwords
- Tokens and sessions
- CORS and browsers
- Uploads and request size
- Outbound requests

## OWASP API Top 10 checks

| Risk | Check in the code |
| --- | --- |
| API1 Broken object level authorization | Every lookup by ID filters by owner or tenant, or checks permission on the loaded object, in the handler or service |
| API2 Broken authentication | Login and token endpoints are rate limited; tokens are validated fully (below); no auth logic hand-rolled when the framework or a maintained library provides it |
| API3 Broken object property level authorization | Input models list only fields the caller may set (no `is_admin` in a profile update); output models list only fields the caller may see |
| API4 Unrestricted resource consumption | Page size caps, request body size limits, timeouts on outbound calls, rate limits on expensive endpoints |
| API5 Broken function level authorization | Admin routes require an admin role check, not only authentication; routes are deny-by-default |
| API6 Sensitive business flows | Purchases, sign-ups and resets have abuse controls (rate limits, idempotency keys, CAPTCHA where needed) |
| API7 Server-side request forgery | User-supplied URLs are validated against an allowlist; internal addresses are blocked (see Outbound requests) |
| API8 Security misconfiguration | Debug off, docs endpoints private when the API is, security headers set, CORS explicit, error responses without stack traces |
| API9 Improper inventory management | Old API versions and test endpoints are removed or protected; OpenAPI spec matches what is deployed |
| API10 Unsafe consumption of APIs | Responses from third-party APIs are validated with models and timeouts like user input |

## Passwords

- Hash with Argon2id: `pwdlib[argon2]` (what FastAPI's docs use) or `argon2-cffi`; Django's `Argon2PasswordHasher`. Not passlib, which is unmaintained; never MD5, SHA-x or unsalted hashes.
- Rehash on login when parameters change (`pwdlib`'s `verify_and_update`).
- Compare secrets with `hmac.compare_digest`, never `==`.

## Tokens and sessions

- JWT validation pins the algorithm list and checks expiry, audience and issuer:

```python
claims = jwt.decode(
    token, key, algorithms=["RS256"], audience=settings.jwt_audience,
    issuer=settings.jwt_issuer, options={"require": ["exp", "aud", "iss", "sub"]},
)
```

- Never accept `alg: none`; never decode with `verify_signature=False` outside tests.
- Access tokens are short-lived (minutes); refresh tokens are stored server-side or rotated so they can be revoked. No personal data in claims; they are readable by anyone holding the token.
- Browser sessions: cookies `HttpOnly`, `Secure`, `SameSite=Lax` or `Strict`; CSRF protection for cookie-authenticated state-changing requests.
- API keys are stored hashed and compared in constant time; they are shown once at creation.

## CORS and browsers

- List allowed origins explicitly. Never `allow_origins=["*"]` together with `allow_credentials=True`.
- Allow only the methods and headers the frontend uses.
- Set security headers at the app or proxy: `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, a Content Security Policy for HTML responses.

## Uploads and request size

- Limit body size at the proxy and in the app; stream large uploads to storage instead of reading them into memory.
- Check content type by inspecting the file, not the client's header or extension; never use a client-supplied filename as a path. Store outside the web root with generated names.

## Outbound requests

- Timeouts on every client (`httpx.AsyncClient(timeout=10)`); retries only for idempotent requests, with backoff.
- For user-supplied URLs: allow only `https`, resolve the host and reject private, loopback and link-local addresses, and do not follow redirects to unvalidated hosts.
