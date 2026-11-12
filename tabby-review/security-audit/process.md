# Security audit: process

Find what an outside party can reach and report only what you can show. Techniques here come from the sources in `THIRD_PARTY_NOTICES.md`, kept where they held up when run or traced.

## 1. Scope and risk

- **A diff:** report what the change adds or makes reachable; the rest is context. **A repository:** start from the entry points. Read the whole diff, and whole files when it is cut off.
- Rank by what a file touches, not its size. High: authentication, authorization, crypto, parsing outside data, anything that builds a command, query or path, money, and any *removed* check. For those: `git log -S "<removed text>"` and `git blame` (why was the check there? one added by a "fix" or "security" commit is the worst to lose), callers of a changed function (`git grep`), and whether any test would fail if the lines broke. A refactor is high risk until shown otherwise.
- Find how the project already does the thing (its validator, authorization decorator, queryset scoping, safe-fetch helper). New code that skips what its siblings do is the best lead. A framework default depends on the pinned version.

## 2. Boundaries and flows

0. **Scanners are leads.** If the project runs `bandit`, `semgrep`, `ruff --select S` or `pip-audit`, read the output as a worklist and say how each hit was judged. A file the tool skipped (semgrep documents skipping files over 1 MB without a JSON warning; not run here) is not cleared. Run semgrep with `--metrics=off`.
1. **Boundaries.** List the entry points (routes, CLI arguments, queue messages, files, environment) and sort each by who may call it: anyone, a logged-in user, a role, another service. Check the check, not its name (`admin_required` may only test a header). A callback or webhook with no caller check is public.
2. **Flows.** Follow each untrusted value from entry through parsing, validation and copies to where it is used. Include batch, retry and error paths. Compare what one function guarantees with what the next assumes.
3. **Read next.** Before you report, open the page for every row whose trigger appears in the code, and name the pages in your coverage line.

| The code shows | Open |
| --- | --- |
| request data reaching `open`, `join`, `startswith`/`endswith`, a redirect, a `unquote` or `normalize`, an id copied into a queue message, job, cache key or log, `status =` assigned in several places, a flag read from the environment, a cache or limit key, read-then-call-then-write | [../two-places-agree.md](../two-places-agree.md) |
| `execute(`, f-string SQL, `subprocess`, `eval`, `pickle`, `yaml.load`, templates, `render` | [injection-and-output.md](injection-and-output.md) |
| login, session, token, JWT, password reset, roles, `is_admin`, `setattr`/`vars(`/`update(**` on request data, ownership of a record | [identity-and-access.md](identity-and-access.md) |
| uploads, archives, `open`, URLs fetched server-side, hashing, randomness, secrets, TLS | [files-network-and-crypto.md](files-network-and-crypto.md) |
| `os.environ`, settings, feature flags, defaults, debug switches, empty or zero values | [defaults-and-config.md](defaults-and-config.md) |
| `.github/workflows`, an AI agent in CI | [ci-workflows.md](ci-workflows.md), [ci-agents.md](ci-agents.md) |
| lock files, indexes, release and publish steps, an advisory | [supply-chain.md](supply-chain.md) |
| C, C++ or Rust beside Python | [../native-boundary.md](../native-boundary.md) |

Attacker-controlled: request data, uploads, headers, cookies, messages from other parties, data lower-trust users write. Server-controlled: settings, environment, CLI flags, constants, the project's own output. For a value read from a database or file, find who writes it. Say how much control the attacker has and what is in the way (normalisation, truncation, type coercion).

## 3. Try to disprove each candidate

The default is "refuted" until the evidence says otherwise; reviewers lean toward seeing bugs and overrating them.

- **Restate the claim** in one sentence: the input, the line, the mistake, the effect. If you cannot, drop it.
- **Read the controls on the path:** allowlists, parameter binding, constant arguments, framework escaping, a check in any layer. A check anywhere counts if it holds on every path to the sink.
- **Is the sink reachable?** Earlier conditions can make a dangerous-looking line impossible to reach. Code nothing calls today is not refuted by that: report it lower and say what would make it reachable.
- **What stops it, what only slows it.** A parameterised query stops; a rate limit or hard-to-guess id raises the bar.
- **Check both directions:** are you reporting because it looks dangerous, or dismissing a real hole because the exploit looks complicated? Re-read after you conclude; did you rely on a validation you never saw?
- **What does the attacker already have?** A bug that needs the privilege it grants is not a finding.
- **Do not report:** tests, fixtures, docs, dead code; auto-escaping and parameterised queries (only their escape hatches on user data); denial of service, ReDoS and missing rate limits (a hardening note, unless a small unauthenticated input causes large amplification); missing logs or headers, open redirects outside login flows; SSRF where only the path of a fixed host is controlled; client-side checks (the server decides); memory-safety claims outside C, C++ and `unsafe`; theoretical races and timing; environment variables and CLI flags as attacker input; vulnerable third-party versions in a diff review ([supply-chain.md](supply-chain.md) covers a repository).
- **Confidence:** reached by attacker input with no effective control: confirmed, with a severity. Depends on something you cannot see: `needs validation`, with the question. Anything else is a hardening note at most.

## 4. Variants, then the fix

- State the root cause in one sentence: "[untrusted data] reaches [dangerous operation] without [required protection]", or for a logic bug the invariant broken. Then search for siblings: write a pattern that matches only the known instance, generalise one element at a time (function, argument, module, framework), read all matches after each step, and stop when more than half are noise. Look beyond the module: other routes, jobs and commands reaching the same sink.
- Widen first: other names with the same role (`is_active`, `is_admin`; `user_id`, `owner_id`), other slips of the same kind (inverted condition, `return True` on the fall-through, `or` for `and`, `None == None`), functions whose behaviour contradicts their name.
- A fix is checked with evidence, not the diff or the author. A test that states the safe outcome must fail on the old code and pass on the new, and you must read the old-code failure to be sure it is your assertion and not an `ImportError`. Add a benign control, and a variant through a different path (another entry point, streaming against buffered, error and cleanup paths, empty and maximum inputs), not the same payload with another literal. "The original proof no longer works" is not a fix until an independent variant also fails. A comment saying the caller must check is not a fix.
- A confirmed finding comes with a regression test that fails before the fix ([reporting.md](reporting.md)).

## Limits

Static reading first. Run target code only with no network, a scrubbed environment, dummy secrets and writes limited to a scratch directory; if you cannot isolate it, say so and do not run it. Never install a tool to audit. Facts outside the repository (proxy, identity provider, deployment) are not proof either way: `needs validation`, with who can answer. Write-time rules: `tabby/development/code/security-basics.md`.
