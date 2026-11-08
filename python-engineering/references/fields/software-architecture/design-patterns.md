# Design patterns

A pattern answers a problem you have today. Python already contains most of them (functions are objects, modules are singletons, generators are iterators), so the first answer is usually fewer classes, not more. Decide whether a pattern is needed, then use its Python form.

## Decide first, even when the request names a pattern

Use a pattern only if at least one of these is true today:

1. Two or more real variants exist now (not "might later") and callers choose between them.
2. A seam is needed for a test: time, network or storage you must replace.
3. Third parties must extend the code without editing it (plugins).

Otherwise write the plain function or data. If the request names a pattern that does not fit, say so in one sentence, build the simplest form that meets the underlying need, and say what you did instead. Do not refuse, and do not deviate silently.

## Python forms

| Asked for | Python form | A class is justified when |
| --- | --- | --- |
| Strategy | A dict of functions; the caller passes or looks one up | each variant carries its own state |
| Factory, abstract factory | A function, a dict of callables, or the class itself | construction needs state shared across calls |
| Singleton | A frozen dataclass built at the program edge and passed in, or a module constant that never changes | never: no `__new__`, `_instance` or metaclass |
| Builder | Keyword-only arguments with defaults; `dataclasses.replace` | never |
| Iterator | A generator function | the iteration is resumable and has several methods |
| Observer | A list of callables | subscribers have their own lifecycle |
| Command, callback | A closure or `functools.partial` | undo, queuing or serialising is required |
| Template method | Pass the varying step as an argument | never |
| Adapter, facade | One function or module that converts or hides | never |
| State | An enum plus a dict of handlers, or `match` | many states each have several methods |
| Repository | Plain functions that take a connection | swapping the storage engine is a real requirement |
| Interface | `typing.Protocol` (nothing to inherit) | an ABC only when subclasses must share implementation code |

## Two forms that are asked for most

Strategy as a dict of functions: a new variant is one function and one dict entry.

```python
def card(amount, d):   return round(amount * 0.029 + 0.30, 2), f"card-{d['last4']}"
def crypto(amount, d): return round(amount * 0.01, 2), f"btc-{d['wallet']}"

METHODS = {"card": card, "crypto": crypto}

def process_payment(kind, amount, details):
    if kind not in METHODS:
        raise ValueError(f"unknown payment kind {kind!r}; expected one of {sorted(METHODS)}")
    fee, ref = METHODS[kind](amount, details)
    return {"status": "ok", "fee": fee, "ref": ref}
```

"One settings object": a frozen dataclass, built where the program starts and passed to what needs it. Tests build `Settings(...)` directly.

```python
@dataclass(frozen=True, slots=True, kw_only=True)
class Settings:
    database_url: str
    timeout: float = 30.0

    @classmethod
    def from_env(cls, env=os.environ):
        return cls(database_url=env["DATABASE_URL"], timeout=float(env.get("TIMEOUT", "30")))
```

When existing signatures or tests must not change, call `Settings.from_env()` where it is needed. It is cheap and keeps the environment read in one module; a cached global or a singleton class would hide the dependency.

## When structure is right

- **Plugins by third parties:** a registry is justified. Discover through `importlib.metadata.entry_points(group="<pkg>.<thing>")`, keep built-ins in the same name-to-callable mapping, document the group name, and make an unknown name an error that lists the available ones.
- **Testability:** keep the rules in a function that takes values (including `now` and config); let a thin outer function read the clock, environment and network and pass them in. Passing a callable is simpler than patching.
- **Real variants with state:** a small class per variant, sharing a `Protocol`, is fine.

## Before finishing

- More classes than variants means flatten it.
- The new code should not be much longer than what it replaced. Say in one line which pattern you chose or declined, and why.

Why the table says what it says (rule of three, composition over inheritance, passing collaborators in, size by responsibility): [design-principles.md](design-principles.md).
