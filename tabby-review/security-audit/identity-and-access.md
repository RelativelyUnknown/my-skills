# Audit classes: identity, access and business logic

Every hit needs the trace from attacker-controlled input to the decision ([process.md](process.md)). Fixes are in `tabby/development/code/security-basics.md` and `tabby/development/application/apis/shared/security.md`.

## Authorization (the commonest serious bug)

First learn how this project enforces access: decorators, middleware, base classes, DRF `permission_classes`, custom managers and `get_queryset()`, and which field owns a row (`owner_id`, `organization_id`). Then ask for each endpoint that handles user data: **if I am user A and know the ID of user B's object, can I read, change or delete it?** Trace it: where the ID enters (path, query, body), where the object is fetched, and what stands between (the query's own scope, an object-level check, a parent class, middleware, a URL-level decorator). A check anywhere on the path counts; a check on one path does not cover another.

- **Gap indicators:** `get_queryset()` returns `.all()`; `Model.objects.get(pk=pk)` or `session.get(Model, id)` with no owner or tenant in the query; a permission class that checks login but not ownership (`IsAuthenticated` is not ownership; DRF's default permission is `AllowAny` unless settings change it); no `has_object_permission` and an unscoped queryset; an ID from the request body for a sensitive operation.
- **Compare siblings:** the delete route lacks the decorator its list route has; the new route skips what the others do. Admin and internal routes need their own check, and so does every other way to reach the data: background jobs, CLI commands, GraphQL, websockets, export endpoints.
- **Follow-ups:** list endpoints filter to the caller's data; on create, the server sets the owner; bulk operations are scoped; related objects (the comments of a document) follow the parent's rule; a tenant ID in the URL cannot be swapped.
- **Permission matching:** `"admin" in user.role` matches `readonly_admin_viewer`; `any(...)` where `all(...)` was meant; roles kept as comma-separated strings. Compare against an `Enum` or `frozenset`.
- **Mass assignment:** a `for k, v in data.items(): setattr(obj, k, v)` loop is the same bug; `Model(**request.json)`, `update(request.data)`, `serializer.save(**request.data)`, a serializer with `fields = "__all__"`, a pydantic model that accepts `is_admin`, `role` or `owner_id`.
- **Field level:** a response built from the whole ORM object, `__dict__` or `to_dict()` (leaks `password_hash`, internal IDs); fields that only an admin or the owner may see.
- **Not a finding:** hidden or missing authorization in client-side code (the server decides); a path that needs a login the attacker can obtain freely is still a finding.

## Authentication and sessions

- **Passwords:** never silently truncated (`password[:72]` before bcrypt; reject an over-long one, the limit is in bytes); Argon2id, scrypt or bcrypt (or the framework's hasher), never MD5, SHA-1 or a bare SHA-256. Quote current OWASP parameters before putting numbers in a report. Length matters more than composition or forced rotation.
- **Enumeration:** identical messages for unknown user and wrong password, and for reset and sign-up ("if that address exists we sent a link"). Timing counts too: when the user is missing, hash a dummy password.
- **Brute force:** lockout or throttling per account, not only per IP; reset stays available to a locked user. Missing rate limits are a hardening note, not a finding.
- **One-time codes:** an expiry that `0` or a negative number disables, no cap on attempts (a six-digit code has 1,000,000 values), a code valid until the next is issued, a reset token that is never invalidated. A token is single use only if it is marked used atomically (`UPDATE ... WHERE used = false`), not by read-then-write.
- **MFA:** checked only in the front end; a "remember this device" token built from the User-Agent; recovery codes derived from the user ID, reusable or unlimited in attempts.
- **Sessions:** a session ID taken from the request (`request.cookies.get("session") or new_id()`) is fixation; a new ID at login and when privileges change (fixation); IDs from `secrets` (never `user_id + time`); `Secure`, `HttpOnly`, `SameSite`; idle and absolute expiry; server-side invalidation on logout; tokens never in URLs.
- **Re-authenticate** before changing the password, e-mail address or MFA, deleting an account or moving money. An e-mail change notifies the old address and confirms the new one.
- **JWT:** the header must not choose the algorithm. `algorithms=[...]` pinned (PyJWT 2 refuses `decode` without it, and rejected an `alg: none` token when the list was pinned); an RSA public key accepted as an HMAC secret is the RS256-to-HS256 confusion, `exp`, `aud` and `iss` checked, a long random key, no personal data in claims.
- **API keys:** in a header, not the URL; stored hashed; compared with `hmac.compare_digest`.
- **Webhook receivers:** verify the signature over the raw body, in constant time, with a timestamp window against replay.

## CSRF, CORS, websockets, GraphQL

- **CSRF:** a cookie-authenticated state-changing endpoint needs a token or an Origin check (Django has it by default, Flask needs `CSRFProtect`, FastAPI has none). `@csrf_exempt` on such a view and any state change on `GET` are findings.
- **CORS:** the real holes are a reflected `Origin` with credentials and `Access-Control-Allow-Origin: null` (`*` with credentials is rejected by browsers).
- **Websocket:** check `Origin` at the handshake and authenticate the connection; a token in the query string lands in logs.
- **GraphQL:** depth and cost limits, introspection off in production, a cap on batched operations, authorization per field.

## Business logic

- **Races:** check-then-write on money, stock, coupons and balances without one transaction and a lock or an atomic conditional `UPDATE`. A `threading.Lock` protects one process only; locks in a fixed order avoid deadlock. Test with two concurrent requests.
- **Client-supplied values:** price, quantity, currency, discount or user ID taken from the request; negative quantities that refund; the same discount code applied twice or stacking below zero; overselling when stock is read first and decremented after payment.
- **Idempotency keys** must be claimed by a unique insert; look-up-then-create lets two identical requests both run.
- **Workflow:** later steps callable without the earlier ones. See [../state-machines.md](../state-machines.md).
