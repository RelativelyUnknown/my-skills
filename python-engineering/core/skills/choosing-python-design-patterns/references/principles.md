# Principles behind the table

Four rules that decide most refactors. Each block runs as written (Python 3.13, 7 November 2026).

## Contents

- Rule of three
- Composition over inheritance
- Pass collaborators in
- Size by responsibility

## Rule of three

Two similar pieces of code are not yet a pattern. Copy, adapt, and wait for the third; then compare the three and abstract only what they share. A wrong abstraction costs more than duplication: every caller bends to it, and removing it later means untangling all of them. Before extracting, ask whether the pieces change for the same reason. Validation that happens to look alike in orders and in returns will diverge when the business rules do.

## Composition over inheritance

Inherit for "is a" with shared behaviour you want to override. Hold the part you reuse for "has a". A subclass that reuses a parent method which calls other overridable methods silently changes behaviour when either side changes.

```python
class Counter:
    def __init__(self) -> None:
        self.count = 0

    def add(self, item: str) -> None:
        self.count += 1

    def add_all(self, items: list[str]) -> None:
        for item in items:
            self.add(item)


class Doubling(Counter):  # overrides add(), and add_all() calls it
    def add(self, item: str) -> None:
        super().add(item)
        super().add(item)


assert Doubling().count == 0
d = Doubling()
d.add_all(["a", "b"])
assert d.count == 4  # the parent's add_all now counts twice per item: a hidden coupling


class Tally:
    def __init__(self, counter: Counter) -> None:
        self._counter = counter  # composition: the dependency is explicit

    def add_twice(self, item: str) -> None:
        self._counter.add(item)
        self._counter.add(item)


t = Tally(Counter())
t.add_twice("a")
assert t._counter.count == 2
```

## Pass collaborators in

A function that needs a clock, a connection or a sender takes it as a parameter, with the real one supplied at the program's edge. No container or framework; tests pass a fake.

```python
from collections.abc import Callable
from datetime import datetime, timedelta, UTC


def is_expired(created: datetime, ttl: timedelta, now: Callable[[], datetime] = lambda: datetime.now(UTC)) -> bool:
    return now() - created > ttl


start = datetime(2026, 1, 1, tzinfo=UTC)
assert is_expired(start, timedelta(days=1), now=lambda: start + timedelta(days=2))
assert not is_expired(start, timedelta(days=1), now=lambda: start + timedelta(hours=1))
```

## Size by responsibility

Split a function when you can name a piece without "and", when two parts change for different reasons, or when you need to test one part without the other. Line counts are a smell, not a rule: a long function that reads top to bottom as one story can stay.

## What the upstream also recommends and this skill does not

Layered "repository, service, controller" structure and wrapper classes around every collaborator are not a default here: plain functions that take a connection are the form until swapping the storage engine is a real requirement (see the table in `SKILL.md`).
