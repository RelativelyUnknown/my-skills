#!/usr/bin/env bash
# A small Rust crate whose per-request feature-flag set is a HashSet of an enum.
set -euo pipefail
mkdir -p src
cat > Cargo.toml <<'__F__'
[package]
name = "flagset"
version = "0.1.0"
edition = "2021"

[dependencies]
__F__
{
  echo '/// Feature flags. One variant per flag; new flags are added over time.'
  echo '#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]'
  echo 'pub enum Feature {'
  for i in $(seq 1 200); do echo "    F$i,"; done
  echo '}'
} > src/feature.rs
cat > src/flags.rs <<'__F__'
use std::collections::HashSet;

use crate::feature::Feature;

/// The features enabled for one request.
#[derive(Clone, Default)]
pub struct Flags {
    enabled: HashSet<Feature>,
}

impl Flags {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn from_features(features: &[Feature]) -> Self {
        Self { enabled: features.iter().copied().collect() }
    }

    pub fn contains(&self, feature: Feature) -> bool {
        self.enabled.contains(&feature)
    }

    pub fn union(&self, other: &Flags) -> Flags {
        Flags { enabled: self.enabled.union(&other.enabled).copied().collect() }
    }

    pub fn difference(&self, other: &Flags) -> Flags {
        Flags { enabled: self.enabled.difference(&other.enabled).copied().collect() }
    }
}
__F__
cat > src/lib.rs <<'__F__'
pub mod feature;
pub mod flags;
__F__
cat > AGENTS.md <<'__F__'
## Tabby
reviewed: 2026-11-09 @ 0000000
purpose: request-time feature flags for an API gateway
users: the gateway's request handlers, thousands of requests per second
goals: lowest per-request overhead; no heap allocation on the request path where possible
growth: new flags are added every release; expect several hundred within a year
out-of-scope: persistence, remote flag services
constraints: Rust stable, no new dependencies without asking
ask-first: new dependency, public API change
kind: code
modules: development, review
commands: cargo test
__F__
git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
