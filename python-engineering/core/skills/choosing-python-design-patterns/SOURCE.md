# Source

`references/principles.md` is adapted from one upstream skill. The rest of this skill is original to this repository.

- Upstream: https://github.com/wshobson/agents
- Path: `plugins/python-development/skills/python-design-patterns/`
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d
- Licence: MIT, Copyright (c) 2024 Seth Hobson. The upstream licence is kept as `LICENSE.wshobson` and applies to the adapted material.
- Adapted: 7 November 2026.

## What changed

- The upstream body (85 lines) and details (353 lines) are condensed to one reference of four short sections: the rule of three, composition over inheritance, passing collaborators in, and size by responsibility.
- Not folded in: KISS and single responsibility as slogans (the table and the "decide first" section already apply them), the separation-of-concerns layering and the repository and service examples. They push layers and wrapper classes that this skill's table declines until swapping the storage engine is a real requirement; the reference says so.
- New and run on Python 3.13: an inheritance example in which overriding `add()` silently changes the parent's `add_all()`, its composition rewrite, and an injected clock. Both example blocks run as written.
