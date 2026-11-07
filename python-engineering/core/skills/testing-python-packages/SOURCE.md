# Source

One section of `references/mocking-and-fixtures.md` ("Retries and failure sequences") is adapted from one upstream skill. The rest of this skill is original to this repository.

- Upstream: https://github.com/wshobson/agents
- Path: `plugins/python-development/skills/python-testing-patterns/`
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d
- Licence: MIT, Copyright (c) 2024 Seth Hobson. The upstream licence is kept as `LICENSE.wshobson` and applies to the adapted material.
- Adapted: 7 November 2026.

## What changed

- The upstream body (278 lines) and details (761 lines) were compared topic by topic with this skill. Fixtures with `yield`, factory fixtures, parametrization, `tmp_path` and `monkeypatch`, mocking only boundaries with autospec, controlling time (`time-machine`; the upstream uses freezegun), markers and coverage are already covered here, in stricter form, so they are not copied.
- Folded in: testing retry behaviour with a scripted `side_effect` list and three outcomes (success after transient errors, gives up after the last attempt, no retry for a permanent error). Rewritten with an injected sleep so the test is instant; the three tests pass under pytest.
