# Design fit: worked examples

Real code, read from the repositories. Each example gives the workload, the structure, why it fits, and what keeps it honest as the project changes.

## ruff `RuleSet` (Rust): a bitset for a fixed universe

- **Workload.** A fixed enum of rules, each with a dense small id (`Rule as u16`). Sets of rules are built from selectors with union and subtraction, and membership is asked for constantly.
- **Structure.** `RuleSet([u64; 16])`: bit `id % 64` of word `id / 64`. Union and subtract are word-wise `|` and `& !`; `len` sums `count_ones`; iteration takes the lowest set bit of each word and clears it. `contains`, `union` and `subtract` are `#[inline] const fn` (written with `while`, because `for` is not allowed in `const`).
- **Why it fits.** The universe is dense and bounded; a set is a small value (128 bytes) that is `Clone`, `Eq` and hashable for free, with no allocation and almost no branching.
- **What keeps it honest.** 16 words is 1,024 ids. A `debug_assert!` fails with "Increase the size of the bitset array" the first time an id does not fit, and a test builds a set from every rule and checks that iteration returns them all in order. The one `unsafe` (`transmute` from `u16` to `Rule`) carries a `SAFETY:` comment resting on the invariant that only valid rules are stored. The future (more rules) is a loud failure and one constant.
- **Stops fitting** when ids are sparse or unbounded, or sets hold one or two elements.

## ruff `IndexVec` (Rust): ids that cannot be mixed up

`IndexVec<I, T>` is a `#[repr(transparent)]` wrapper over `Vec<T>` indexed by a newtype `I: Idx` (the crate says it is inspired by `rustc_index`). Records refer to each other by index, not reference; an id of one table cannot index another table, because the types differ, at no runtime cost. Stops fitting when records are deleted and ids reused: add generations.

## uv `Version` (Rust): a packed fast path with a full fallback

- **Workload (the code's own comment).** Resolution compares versions constantly, and almost all versions are small: epoch 0, at most four release segments, no local part, at most one pre, dev or post component.
- **Structure.** `enum VersionInner { Small, Full }`. `VersionSmall` packs those versions into one `u64`, laid out so that `u64::cmp` equals PEP 440 ordering. Its setters return `false` when a value does not fit, and the caller switches to the `Full` form (an `Arc`). A `NonZero<u8>` niche keeps the enum at two words.
- **Why it fits.** The common case is small and hot, the rare case stays correct, and the choice hides behind `Version`.
- **What keeps it honest.** The comment records the limits and why they were chosen, and an earlier encoding that was abandoned after a bug (`1.0dev1 > 1.0a1`). That record is the project's past, written where the next maintainer will read it.

## polars `Bitmap` (Rust): one bit per value

A column of millions of values may be null in places. The validity mask is semantically `Arc<Vec<bool>>`, stored as bytes with one bit per value plus an offset and a length so slicing copies nothing: eight times smaller than a byte per flag. Building one by pushing values uses the mutable twin, `MutableBitmap`: the immutable form is for sharing, the mutable form for construction.

## pandas `khash` (C): one hash table, specialised per type

pandas vendors klib's `khash.h` and generates a typed hash table for each dtype (`Int64`, `Float64`, `String`, `UInt8` and others) from one template, `hashtable_class_helper.pxi.in`. Hot lookups on a single key type avoid boxing and indirect comparison. Stops fitting when keys are heterogeneous: pandas keeps an object table for those.

## Same choices in other languages

Names to look up, not verified here. C++: `std::bitset<N>` (size fixed at compile time), `boost::dynamic_bitset` (sized at run time), LLVM `SmallVector`. Rust: `bitflags`, `smallvec`, `slotmap`, `bumpalo`, `indexmap`. C: arrays plus indices, arena allocators, `uint64_t` arrays as bitsets. Python: an `int` as a bitmask or `enum.IntFlag`, `array`, `memoryview`, `__slots__`.
