# Deprecation and migration

Every public behaviour has a user, and removing it is a migration you owe them. Ask before removing anything: who depends on this, what do they move to, and when? "Delete it" is a request to deprecate unless the code has no callers you can find and nothing outside the repository imports it.

Removing or changing a public name needs approval (`ask-first: public API change`). The rules for the warning and the release are in [api-design.md](../library/shared/api-design.md) and [release.md](../library/shared/release.md); this page is the order of work.

## Before deprecating

1. Does it still do something nothing else does? If yes, keep it.
2. Who calls it? Search the repository, then ask about code outside it. Count them.
3. Does the replacement exist and work? If not, build it first; never deprecate without one.
4. What does moving cost each caller? If a mechanical edit can do it, do it for them.
5. What does keeping it cost: security exposure, maintenance, confusion?

Default to **advisory** (warn, document, leave it working). **Compulsory** (a removal date) only for a security problem, a blocker or an unsustainable cost, and then with the migration tooling and notes in place first.

## In Python

- `warnings.warn("use new_name; removal in 3.0", DeprecationWarning, stacklevel=2)`, or `@warnings.deprecated("...")` from Python 3.13 (type checkers flag uses). `stacklevel=2` points at the caller. Name the replacement and the removal version.
- `DeprecationWarning` is shown by default only for code running as `__main__`, and by pytest. For warnings that end users of an application must see, use `FutureWarning`.
- Run your own tests with `-W error::DeprecationWarning` so nothing inside the project still calls the old name. Add a test that the warning is raised (`pytest.deprecated_call()`).
- The old name stays in `__all__` and keeps working until the removal release.

## Moving callers

- Put the new path beside the old one, move callers over in steps, and keep the tests green after each. Behind a flag or an adapter if the old and new must run together (strangler).
- Schema changes: add, backfill, switch reads, then drop later ([persistence.md](../application/shared/persistence.md)).
- Replacing a dependency: put it behind one module first, migrate callers to that module, change the implementation, remove the dependency from `pyproject.toml` last and check what else it pulled in.
- Dropping a Python version: raise `requires-python` in a minor release, update the CI matrix, delete the compatibility code, and say so in the changelog.

## Removing

Only when callers are gone, the deprecation has lasted the stated releases, and the changelog has a "Removed" entry with the migration. A breaking removal follows the version rules in [versioning.md](../library/shared/versioning.md).

## Code nobody owns

Code with users but no owner and no recent change gets an owner or a deprecation with a plan; it does not stay in between.
