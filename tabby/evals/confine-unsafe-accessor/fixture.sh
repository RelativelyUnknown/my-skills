#!/usr/bin/env bash
set -euo pipefail
mkdir -p src
cat > Cargo.toml <<'__F__'
[package]
name = "rowstore"
version = "0.1.0"
edition = "2021"
__F__
cat > src/row.rs <<'__F__'
/// A fixed-width row of integers.
pub struct Row {
    values: Vec<i64>,
}

impl Row {
    pub fn new(values: Vec<i64>) -> Self {
        Self { values }
    }

    /// Returns the value at `i`, or `None` if `i` is out of bounds.
    pub fn get(&self, i: usize) -> Option<i64> {
        self.values.get(i).copied()
    }

    pub fn len(&self) -> usize {
        self.values.len()
    }
}
__F__
cat > src/lib.rs <<'__F__'
pub mod row;
__F__
cat > AGENTS.md <<'__F__'
## Tabby
reviewed: 2026-11-09 @ 0000000
purpose: an in-memory row store, hot summation loops over validated indices
users: a query engine calling Row::get millions of times per query
goals: the fast path must not weaken safety for any other caller
kind: code
modules: development, review
ask-first: new dependency, public API change
commands: cargo test
__F__
git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
