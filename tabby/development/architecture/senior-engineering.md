# Senior-level engineering: the habits behind well-run codebases

What separates a senior engineer's code from working code is rarely a clever trick. It is a small set of habits, applied consistently, that catch mistakes early and keep a system fast under real load. This file names the habits, with the real codebases they come from, and says how they apply to Python, Rust and C.

## Assertions as a safety net

TigerBeetle's style guide treats assertions as the main tool for catching programmer error, not an afterthought: assert a function's arguments, return values and invariants: the target is an average of two assertions per function. Pair assertions where possible, checking the same property on both sides of a boundary (validity before writing to disk, and again right after reading it back). Assert both the positive space you expect and the negative space you do not, because bugs live at that boundary. State invariants as the positive form (`if index < count`), which is easier to read than its negation. Split a compound assertion (`assert(a); assert(b);`) instead of one combined condition, so a failure says which part broke.

In Python this is `assert` only for invariants the caller cannot violate from outside ([errors.md](../code/errors.md) has the line between a bug and a caller mistake); in Rust, `debug_assert!` for invariants checked in debug builds and a real `assert!` where a release build must still catch it (ruff's bitset array-size check is exactly this); in C, `assert()` from `<assert.h>`, compiled out by `NDEBUG`, so a release build still needs the check to be a real error path if callers can trigger it.

## Design for limits before you profile

TigerBeetle's rule: put a limit on everything, because production always has one. All loops and queues get a fixed upper bound; an event loop that cannot terminate gets an assertion saying so. The best time to think about performance is the design phase, with a back-of-the-envelope sketch of network, disk, memory and CPU cost, not after profiling: a design that is wrong by 1000x is cheap to fix before it is built and expensive after. Optimise the slowest resource first, after weighing how often each one is used; a memory cache miss paid a million times can cost more than a disk fsync paid once.

This is the same move as [fit.md](fit.md): know the workload and the limits before writing the structure, then make the limit a loud, cheap-to-fix failure instead of a silent one.

## `unsafe`, confined and proven

Two different large Rust and Java codebases that lean on `unsafe` for real workloads agree on the shape of the boundary, independent of language.

Polars pairs almost every unchecked accessor with a safe, bounds-checked twin (`get` beside `get_unchecked`), documents the precondition under a `# Safety` heading ("It is the caller's responsibility that `idx < self.len()`"), and keeps the `unsafe` block itself to the one call that needs it, wrapped in a comment that restates why it is sound at that call site. The public API stays safe; `unsafe` is an internal fast path for a hot loop that has already checked its own bound.

Spark's `Platform` class concentrates every `sun.misc.Unsafe` call used across the whole engine behind one small set of static methods (`getInt`, `putLong`, byte-array offsets, `throwException`), queried for platform capability once (`unaligned()`) instead of scattered throughout the codebase. `UnsafeRow` then builds a documented binary row layout (a null-tracking bit set, one word per fixed-length field, relative offsets for variable-length ones) on top of that one safe surface, so the whole SQL engine operates on raw memory through one audited seam instead of many.

The shared rule: `unsafe` lives behind the smallest possible interface, has a written precondition, and the code that uses it does not also decide whether the precondition holds; the caller of the safe wrapper does. See [library/native/rust.md](../library/native/rust.md) and [library/native/c.md](../library/native/c.md) for the project's own `unsafe` rules; this file is why those rules exist.

## Let the program set its own pace

TigerBeetle again: do not react directly to external events; run your own loop and let it decide when to look at events, which both keeps control flow under your control and lets you batch instead of context-switching on every one. This is the same idea as DeepSeek's DualPipe: a bidirectional pipeline schedule built specifically so forward and backward passes, and their communication, overlap instead of stalling on each other, cutting the idle bubbles between stages. Both are the same move at different scales: decide the schedule up front instead of letting external timing decide it for you.

## Design around the hardware you actually have

DeepSeek's FlashMLA Ascend kernel work is a documented case of several of the habits above applied under real hardware limits, written up after the fact in their own deep-dive notes:

- **The instruction cache is small (8K to 32K depending on the core type), so code size is a hard budget.** They kept the hot kernel's code under that limit on purpose, the same "put a limit on everything" instinct as above, applied to code size instead of a queue depth.
- **The hardware issues instructions in order on each pipe, so the issue order has to be designed, not left to chance.** A scalar core and a SIMD core had to pass a signal through a shared buffer because the hardware itself enforces strict in-order issue per pipe; they traced that constraint to its source and designed the issue sequence around it instead of fighting it with retries.
- **A per-token copy request would have exceeded the hardware's request queue depth, so they batched requests instead ("gather2")**, the same batching instinct as TigerBeetle's "let the CPU be a sprinter": give the hardware large, predictable chunks of work instead of many small ones.
- **They split tensors across both halves of a banked on-chip memory, and padded a buffer, specifically to avoid a bank conflict**, which is the same "know the memory layout you depend on" reasoning as [fit.md](fit.md), one level closer to the metal.

The lesson is not the specific numbers (another NPU, another cache size, another bank layout). It is reading the hardware's actual constraints first, from its documentation or by measuring, and designing the code's shape around them, rather than writing the obvious version and hoping the compiler or runtime absorbs the mismatch.

## Know which layer you are fixing, and delete the fix when it moves

DeepGEMM's own changelog records this: an instruction-scheduling detail of the generated low-level code used to need a manual post-processing pass, until a newer compiler release did that scheduling automatically, at which point the manual pass was dropped. Two separate disciplines, both visible in that one line: first, noticing that a layer you depend on (here, the compiler's code generation) is leaving measurable performance on the table and writing a narrow, well-tested fix for exactly that gap; second, deleting the fix the moment the lower layer catches up, instead of carrying it forward as dead weight because it still technically works. A workaround that never gets revisited is the same failure as the undated `# shortcut:` comment in [code/minimalism.md](../code/minimalism.md): name what it is working around and when to check if that is still true.

DeepEP shows the companion habit at the planning level: an earlier version needed autotuning to pick how many streaming multiprocessors and queue pairs a communication kernel should use; a later version replaced that search with an analytical calculation of the same numbers. Autotuning is a reasonable first answer when you do not yet understand a system's behaviour well enough to model it. Once you do, a closed-form calculation is faster, more predictable, and has no search budget to run out. Treat a tuning loop in your own code the same way: a placeholder for a model you have not derived yet, not a permanent feature.

## Say why, every time

"Always motivate, always say why": a decision explained is a decision the next reader can evaluate, not just obey. This is one of the few rules in this file that costs nothing and always applies: every ADR ([documentation/history/adr.md](../../documentation/history/adr.md)), every `# shortcut:` comment ([code/minimalism.md](../code/minimalism.md)), every rejected alternative in [fit.md](fit.md) is this rule in practice.

## What this does not mean

TigerBeetle's "zero dynamic allocation after startup" and 70-line function limit are real constraints for the embedded, safety-critical systems they were written for. They are not general Python rules, and the examples above are taken for the reasoning, not the letter of the rule. Do not import a constraint from a different domain just because the source is well-regarded; state which workload and failure mode it is solving before applying it here.
