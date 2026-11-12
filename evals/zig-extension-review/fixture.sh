#!/usr/bin/env bash
set -euo pipefail
mkdir -p src
cat > build.zig.zon <<'__F__'
.{
    .name = "fastmath",
    .version = "0.1.0",
}
__F__
cat > src/root.zig <<'__F__'
const py = @import("pydust");

pub fn fibonacci(args: struct { n: u64 }) u64 {
    if (args.n < 2) return args.n;
    var sum: u64 = 0;
    var last: u64 = 0;
    var curr: u64 = 1;
    for (1..args.n) {
        sum = last + curr;
        last = curr;
        curr = sum;
    }
    return sum;
}

comptime {
    py.rootmodule(@This());
}
__F__
cat > AGENTS.md <<'__F__'
## Tabby
reviewed: 2026-11-09 @ 0000000
purpose: a Zig-backed Python math extension built with Ziggy Pydust
kind: library/native
modules: development, review
commands: zig build test
__F__
git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
