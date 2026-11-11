# Senior-level engineering: questions to ask, not stories to admire

Each section is a question to apply to a design you have not seen before; that is the point, not the stories that show it working. Illustrations are in [senior-engineering-examples.md](senior-engineering-examples.md); read one to check a doubt, not to learn the rule.

## Make invariants checkable, not implicit

Before trusting a value, ask: what must be true here for what follows to be correct? Turn the answer into a check, not a comment: a comment goes stale silently, a check fails loudly. Check it where the value enters your control, and again where its violation would do damage; the gap between the two is where a corrupted value travels unnoticed. State what must hold, not what must not ("if `index < count`" reads faster than its negation), and split a check that tests two things into two, so a failure says which one broke.

In Python this is `assert` for invariants a caller cannot violate ([errors.md](../code/errors.md) draws that line); in Rust, `debug_assert!` plus a real `assert!` where a release build must still catch it; in C, `assert()`, compiled out by `NDEBUG`, so a caller-triggerable violation needs a real error path, not just a check.

## Know every limit before you can measure one

A design touches real limits before any code exists to profile: queue depth, cache size, a connection pool, memory bandwidth. For each resource it depends on, ask: what is the actual number, and what happens at and past it? Unknown, find it (the spec, the source, a five-minute sketch) rather than learn it from an incident. Make "past the limit" a defined, observable event (a rejected request, an assertion, a degraded mode), never silent truncation or unbounded growth.

[fit.md](fit.md) applies this to one case, choosing a data structure: know the workload and its bound first, and make outgrowing it loud and cheap to fix. The same question reaches one level further down, to the hardware or runtime underneath, not only the structures built on it.

## Shrink what has to be trusted without proof

Some code cannot be checked by a compiler or type system: a raw pointer cast, manual memory access, hand-built SQL, a type-checker override. There the question is not "is this correct?" (you cannot fully know) but "how small can the part that has to be right be, and can I write down what must hold for it to be right?" Wrap it in the smallest function, state the precondition where declared and restate why it holds where used, and keep every caller on the normally-checked side of that line. Only one small, marked place should need a human to verify it by reading.

See [library/native/rust.md](../library/native/rust.md) and [library/native/c.md](../library/native/c.md) for this project's own rules for `unsafe`; this is why those rules take the shape they do.

## Decide your own pace instead of reacting to someone else's

For code that reacts to external events one at a time (requests, messages, callbacks), ask who decides when the work happens: the caller, or you? If the caller does, every event costs a context switch and your worst-case latency follows their timing. Where you can, pull events into a loop you control: batch related work, defer what can wait, give the processor large predictable chunks instead of many small interruptions. Not "add a queue everywhere": a question for whenever something external is forcing a reaction.

## Name the layer you are really fixing, and write its expiry date

Before writing a workaround for something broken or slow one layer below (a compiler, a library, the OS), name which layer owns the defect and what change would make the workaround unnecessary; write both down next to the fix as a condition to check later. No trigger means it becomes permanent, because nothing prompts a revisit; this is the general form of the `# shortcut:` convention in [code/minimalism.md](../code/minimalism.md).

The same applies to solving by search instead of understanding (autotuning, trial and error): a legitimate first answer when you cannot yet calculate the result directly, but a debt against your own incomplete model. Once you understand the system, prefer the closed-form answer: faster, more predictable, with no search budget to run out.

## Say why, every time

A decision explained is a decision the next reader can evaluate, not just obey. Costs nothing, always applies: every ADR (`history/adr.md` in the `tabby-docs` skill), every `# shortcut:` comment, every rejected alternative in [fit.md](fit.md) is this rule in practice.

## Before importing a rule from elsewhere, name its workload

A constraint from an admired codebase answers a question you have not asked yet. State in one sentence which workload and failure mode it solved there before adopting it; if you cannot, leave it out rather than carry it over because the source is well regarded.
