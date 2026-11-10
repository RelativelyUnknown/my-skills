# Senior-level engineering: illustrations

Real code for each question in [senior-engineering.md](senior-engineering.md). Read one to settle a doubt about how a rule looks in practice; the rule in that file is the instruction, this file is evidence.

## Make invariants checkable, not implicit

TigerBeetle's style guide targets an average of two assertions per function, pairs them across a boundary (validity checked right before a write and again right after the matching read), and states the positive form of each invariant. ruff's `RuleSet` bitset carries a `debug_assert!` that fires the first time a rule id does not fit the array, naming the fix in the message ("Increase the size of the bitset array") instead of failing silently.

## Know every limit before you can measure one

TigerBeetle bounds every loop and queue and sketches network, disk, memory and CPU cost at design time, before any profiler runs. DeepSeek's FlashMLA Ascend kernels show the same question asked one level lower, against real hardware: the instruction cache is 8K to 32K depending on the core, so code size became a hard budget on purpose; the hardware issues instructions in order on each pipe, so the issue sequence had to be designed around that fact rather than discovered by a race; per-token copy requests would have exceeded the hardware's request queue depth, so requests were batched ("gather2") to stay under it; tensors were split across both halves of a banked on-chip memory, with padding added, specifically to avoid a bank conflict. None of the numbers transfer to another chip; the habit of reading the real limit first does.

## Shrink what has to be trusted without proof

polars pairs nearly every unchecked accessor with a safe, bounds-checked twin (`get` beside `get_unchecked`), states the precondition under a `# Safety` heading ("It is the caller's responsibility that `idx < self.len()`"), and keeps the `unsafe` block itself to the one call that needs it. Spark's `Platform` class concentrates every `sun.misc.Unsafe` call used by the whole engine behind one small set of static methods, queried for platform capability once; `UnsafeRow` then builds a documented binary row layout on top of that single audited seam, so the SQL engine touches raw memory through one place instead of many.

## Decide your own pace instead of reacting to someone else's

TigerBeetle's own rule: do not react directly to external events; run your own loop and decide when to look at them, which both keeps control flow under your control and lets you batch instead of context-switching on every one. DeepSeek's DualPipe schedules a bidirectional pipeline specifically so forward and backward passes, and their communication, overlap instead of stalling on each other, deciding the schedule up front rather than letting arrival order decide it. FlashMLA's "gather2" batching is the same move at the hardware-request level.

## Name the layer you are really fixing, and write its expiry date

DeepGEMM's own changelog records a manual low-level instruction-scheduling pass that used to be needed by hand; once a newer compiler release did that scheduling automatically, the manual pass was dropped. DeepEP shows the companion habit: an earlier version autotuned how many streaming multiprocessors and queue pairs a communication kernel should use; once the team understood the relationship well enough, a later version replaced that search with a direct analytical calculation of the same numbers.

## What this is not

TigerBeetle's "zero dynamic allocation after startup" and 70-line function limit are real constraints for the embedded, safety-critical systems they were written for. They are evidence that constraints taken seriously produce good design, not a Python rule to copy; see the last question in [senior-engineering.md](senior-engineering.md).
