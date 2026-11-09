# Typing

- Structured data is a dataclass, `TypedDict` or the model class the project already uses, not a `dict[str, Any]` passed around. No `Any`: write the precise type, or `object` for a truly opaque value. `Optional` return only if the function can return `None`. No tuples of three or more values as a return type. No `x = x or 30` (`or` also replaces `0` and `""`).
- Run the checker after every change and fix the types instead of silencing it; never add a second checker.

- Annotate every public function and method (parameters and return) and public attributes. Private helpers only where the checker cannot infer the type.
- Syntax by target: `X | None` and `list[int]` (3.10+); `Self`, `Required`/`NotRequired`, `assert_never` (3.11); `type Alias = ...`, `def f[T](x: T)`, `class Box[T]`, `@override` (3.12); `TypeIs`, `ReadOnly` (3.13). Below the target, import from `typing_extensions` or leave it out. Never `Optional[...]`, `Union` or `typing.List` in new code.
- Parameters take the widest type that works (`Sequence`, `Mapping`, `Iterable`); returns are concrete (`list[str]`). `list[Dog]` is not a `list[Animal]` because lists are invariant, but a `Sequence[Animal]` parameter accepts it.
- Narrow, do not cast: `if x is None: raise ...`, `isinstance`, `match`. A `cast` or `# type: ignore[code]` needs a comment saying why the checker is wrong, and always the error code, with `warn_unused_ignores` on.
- `Any` only at an untyped boundary, narrowed straight away; `object` for an opaque value. A `dict[str, Any]` with known keys is a `TypedDict` (`NotRequired` for optional keys) or a dataclass. Distinct ids are `NewType`.
- A closed set is `Literal[...]` or an `Enum`. Handle it with `match` and end with `case _: assert_never(x)`: adding a member then fails the check.
- `TypeIs[T]` narrows both branches; its `T` must be a subtype of the parameter type, so take `Sequence[object]` to narrow to `Sequence[str]` (`list[str]` is rejected for `list[object]`). `TypeGuard[T]` narrows only the true branch. Plain `isinstance` is simpler when it is enough.
- A decorator uses `ParamSpec` and `functools.wraps` so the wrapped signature survives. A callable with keyword names or defaults is a `Protocol` with `__call__`; otherwise `Callable[[int], str]`.
- `@override` marks an override and fails on a typo in the name; mypy's `explicit-override` error code makes it mandatory. A `Protocol` is for two or more implementations or a test fake; `@runtime_checkable` checks that methods exist, not their signatures.
- Generics only where the type flows from input to output (`def first[T](xs: Sequence[T]) -> T`); bind with `bound=` when you call methods on it. No generic class or repository for one use.
- `from __future__ import annotations` stores annotations as strings. Code that reads them at run time (pydantic, `typing.get_type_hints`) fails on names imported only under `TYPE_CHECKING`. Python 3.14 evaluates annotations lazily by default (PEP 649, 749), so the import is not needed there.
- Adopting strict mode in an existing codebase: `strict = true` for the whole project plus a shrinking `[[tool.mypy.overrides]]` list (`module = "pkg.legacy.*"`, `ignore_errors = true`); new modules never join the list. Pyright: `typeCheckingMode = "strict"` in `[tool.pyright]` with `ignore = [...]`.
- A library ships `py.typed` and annotates everything it exports; see [api-design.md](../library/shared/api-design.md).

Examples checked with `mypy --strict`: [typing-patterns.md](typing-patterns.md).
