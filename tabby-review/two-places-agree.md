# Two places that must agree

Many serious bugs are not on any one line. A rule is enforced in one place and the value it protects is used in another, and they disagree. For each situation below: read both places, then confirm with the cheap probe.

- **Checked in one form, used in another.** The name is tested raw (or lowercased, stripped, unquoted) and a transformed copy (`unicodedata.normalize`, `unquote`, `resolve`, `.lower()`) reaches `open`, a query or a URL. Read: every transform between the check and the use. Confirm: build an input that is harmless before the transform and hostile after (fullwidth dots, `%2e%2e`, a trailing dot or space).
- **A string prefix standing in for a boundary.** `path.startswith("/srv/x")`, `host.endswith("example.com")`. Read: what else begins or ends that way (`/srv/x-private`, `evilexample.com`). Confirm: run the check on that sibling.
- **An identity copied across a hop.** A `user_id`, tenant or role taken from the request body or a header into a queue message, job argument, cache key or log, then trusted by the consumer. Read: where the value first enters and whether the session value replaces it. Confirm: enqueue another user's id and see whose data returns.
- **A check that a default turns off.** An env var read as a string (`"0"`, `"false"` are truthy), an empty key that means "skip", `None == None` when both sides can be absent. Read: the setting's default and how it is parsed. Confirm: `bool("0")`, or call with the field omitted.
- **A state field with several writers.** List every assignment to `status` (`git grep -n "\.status = "`), including jobs, webhooks and admin paths, and compare each with the transition table. A writer that skips the table is the bug.
- **A cache or memo key missing a dimension.** The value depends on the user, tenant, locale or auth state and the key is only a path or an id. Confirm: two users, same key.
- **Check, call, then write.** Read a balance or status, call out (payment, queue, HTTP), then update, with no lock, transaction or idempotency key. Two concurrent requests both pass the check. Confirm: reason through two interleavings, or run two threads against a stub.
- **A limit keyed on what the client chooses.** A rate limit or lockout keyed on a header, a cookie or a self-reported id. Confirm: change the key each request.

Report the pair, not one side: where it is checked, where it is used, and the input that gets between them.
