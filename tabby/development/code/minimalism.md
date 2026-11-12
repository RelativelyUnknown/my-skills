# Minimalism and names

Aim for the fewest concepts a reader must learn, not the fewest characters. Write like a senior engineer who golfs, never at the cost of clarity.

Every function, class, constant and exception is something a reader must look up. Each must earn its place.

The question for every piece you add: what does the reader lose if this is gone? If nothing, it is cost without value. Indirection (a wrapper, a hook, a constant, a base class) is worth it only when it hides a real decision or protects a rule that must stay consistent; "flexibility" nobody asked for is a guess about the future, paid for now. The lines below are that question applied to common cases.

- First ask whether it needs to exist. Then climb the ladder: what the project already has, the standard library, the community's standard library, and only then niche libraries or new code ([reuse.md](reuse.md)). Skip options and flexibility nobody asked for, and name what you skipped in one line.
- Keep values in the form they arrive in. Do not convert a type, wrap a value or add a model class unless a rule needs enforcing there ([validation.md](validation.md)).
- A function must hide real logic or enforce a rule that has to stay consistent. Deletion test: if inlining it leaves every call site as short and clear, delete it. No one-line wrappers around expressions, stdlib calls or library methods (`def quote(s): return f'"{s}"'`).
- A method that never reads `self` is a function; a class with `__init__` and one method is a function. No wrapper classes that only forward; no ABCs, Protocols, factories or registries with one implementation; no parameters, options or hooks "for flexibility"; no `**kwargs` unless forwarding.
- Defaults are literals in the signature or the dataclass field (`timeout: float = 30`), so hovering over a function in an editor shows the value. No `DEFAULT_*` constant and no `DEFAULTS` dict standing in for a default, and "easy to change later" is no reason: a caller can pass the value and a developer edits one line. A constant is for a value the body uses; a value used once stays inline. Mutable defaults are never allowed: use `None` and build the object in the body.
- No `utils.py` or `helpers.py`; put code where it is used. No variable assigned only to be returned on the next line. No single-use type alias, base class or Enum "for consistency".
- Shorter only when also clearer: no nested comprehensions beyond one level, no walrus chains, no single-letter names outside tight loops.

- Names say what a thing is, in the codebase's vocabulary: `users`, not `user_list`. No vague names (`data`, `result`, `info`, `temp`, `obj`, `helper`, `manager`, `handler`), no `new_`/`old_`/`v2`/`final`/`fixed`/`robust`. Booleans read as predicates (`is_expired`). One word per concept: not `fetch`, `get` and `load` for the same thing.
- Core logic takes values and returns values; I/O and state stay at the edges. No module-level mutable state, singletons or global clients; pass dependencies in. Early returns over nesting. `with` for resources. Sets for membership checks in loops; batch queries and HTTP calls. Async code never calls blocking I/O, and a function that never awaits is not `async`.
- A shortcut with a known limit gets one comment: `# shortcut: <the limit>, <when to upgrade>` (for example `# shortcut: linear scan, move to an index past 10k rows`). A shortcut without a named trigger is a smell. The review lists them with `git grep -nE "# ?shortcut:"`.

## Write it right the first time

Slop is easier to avoid than to remove. While you write, not after:

- Before a helper, a constant or a class: `git grep` for the thing that already does it, and use that.
- A comment only for why; never for what the next line does. No "Step 1" or "now we...".
- Check inputs where untrusted data enters (a request, a file, a queue message). Code that only receives the project's own values does not re-check them; no `try`/`except` around a call that cannot fail in a way you can handle.
- If the type checker complains, fix the type. A cast, `Any` or `# type: ignore` to get past it is a smell of its own ([smells.md](smells.md)).
- Match the file you are in: its naming, its error style, its test layout. No reformatting of lines you did not change.
- Leave no scratch files, prints, commented-out code or half-finished branches behind.

Minimal applies to the solution, never to the job. Never cut: validation where untrusted data enters, error handling that prevents data loss, security checks, a test for new logic that can fail, anything the user asked for.
