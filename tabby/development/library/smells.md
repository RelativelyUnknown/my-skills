# Library smells

For code others import and install. These are the mistakes that break the rules in [api-design.md](shared/api-design.md), so read both. Same format as [code/smells.md](../code/smells.md): the smell, `→`, the fix. Report one only when you can name the caller it breaks.

- A positional boolean in a public signature (`save(report, True)`) → a keyword-only flag, or two functions
- Optional parameters before required ones, or optional ones not keyword-only → required first; optional after `*`
- A public module with no `__all__`, deep import paths, or internal state handed out as the live list → `__all__`, flat imports, return a copy or a tuple
- `__init__.py` with logic in it → imports and `__all__` only
- A changed return type, a removed name or a different exception type in a minor release → additive change; keep the old name as a deprecated alias with `DeprecationWarning` for a minor release
- A heavy dependency (pandas, pyarrow) in `dependencies` that one function needs → an extra in `[project.optional-dependencies]`, imported inside the function, an `ImportError` that names the extra
- Handlers configured, `basicConfig` called or `print` in library code → `logging.getLogger(__name__)`; a `NullHandler` in the top-level `__init__`
- Bare `Exception` raised, or an error hierarchy deeper than one root → built-ins for misuse; one root `PkgError`
- No `py.typed`, or public functions only partly annotated → ship `py.typed`; annotate every public function
- A version bump that does not match the change, or a changelog that does not say what users must change → one place for the version; a changelog line per breaking change
