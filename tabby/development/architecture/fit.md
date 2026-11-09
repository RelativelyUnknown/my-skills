# Design fit: the structure that fits the workload and the plans

A smart design often beats clever code. The right data structure, representation or algorithm depends on facts that are not in the function you are editing: the workload, the constraints, and the project's past, present and future. Tabby holds those facts; use them. Without them, take the plain structure, say what you assumed, and ask when a wrong guess would be expensive to undo. This applies to Rust, C and C++ below the Python boundary, and to Python above it.

## What to know before choosing

- **Workload, in numbers.** How many items and how big; reads against writes; lookup, iteration or set algebra; hot or cold path; lifetime (per request or the whole program); threads. Measured is best; assumed is fine if labelled.
- **Constraints.** Memory and latency budgets, platforms, determinism, `no_std`, and the Python boundary: across it pass flat buffers and integer ids, not objects.
- **The past.** Why it is shaped this way: ADRs, `git log -S<name>`, `git blame`, comments. A structure that looks wasteful may encode a constraint you cannot see, so find the reason before replacing it ([refactoring.md](../workflow/refactoring.md)).
- **The future.** `growth:` and `constraints:` in `## Tabby`. Know what is expensive to change later (a public API, an on-disk or wire format, an FFI layout) and what is cheap (private internals).

## Method

1. State the workload in one sentence with numbers.
2. Start from the plain structure (list, dict, struct). Keep it unless the workload says it fails; decide from sizes and a measurement, not from taste.
3. Read the shape of the data against the table below: dense small ids, a fixed or bounded universe, mostly small, mostly read-only, many cross-references, repeated strings.
4. Say when the choice stops fitting, make that failure loud and cheap to fix (one constant, one module). Add both pieces: an assertion on the size, and a test that builds the structure from every variant or id and checks each one.
5. Hide it behind a small interface; use typed ids, not bare integers.
6. Record the assumed workload, the alternatives you rejected and the trigger to revisit, in one comment or ADR (`# shortcut:` for a known limit).

## Fit table

| Data shape | Structure | Stops fitting when |
| --- | --- | --- |
| A fixed, dense universe of small ids; membership and set algebra dominate | bitset: `[u64; N]`, `bitflags`, `std::bitset<N>` | the universe is large, sparse or unbounded: use a hash set or a compressed bitmap |
| Records that refer to each other | an index or typed id into a `Vec` instead of pointers: `IndexVec`, arrays plus indices | records are removed and ids reused: add generations (`slotmap`) |
| Mostly tiny, occasionally large | a packed or inline fast path with a full fallback: `smallvec`, LLVM `SmallVector`, a `u64` for the common case | the "small" case stops being the common one |
| A boolean or null flag per value, in bulk | a bit-packed mask | per-element mutation dominates: use a mutable builder |
| Many equal strings or tokens | interning: id to string table | ids must outlive the table |
| Many short-lived allocations that die together | an arena or bump allocator | objects need individual lifetimes |
| A key set known at build time | a static table: sorted array, `match`, perfect hash | the keys change at runtime |
| Hot lookups of one key type | a hash table specialised for that type | keys are heterogeneous |

## The same reasoning applies elsewhere

Algorithm (batch or stream, sort or partition), layout (struct of arrays or array of structs, columnar), caching against recomputing, error representation (an enum or an exception), API shape (a builder or an options struct). Same inputs, same record.

## Smells

- A structure chosen with no stated workload ("faster", with no numbers).
- A clever structure for a few dozen elements.
- A representation that leaks into a public or FFI signature.
- A structure with no loud failure when the data outgrows it.
- A bare integer standing in for an id of a particular table.

Worked examples from real code: [fit-examples.md](fit-examples.md).
