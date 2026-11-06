# Source of this copy

- Upstream: https://github.com/blader/humanizer
- Path: `SKILL.md` at the repository root
- Commit: `0ef9fe5bc3572734fd3ae6c448fe00a30cd5dcf0` (28 October 2026, as shown on the GitHub commits page)
- Licence: MIT, Copyright (c) 2025 Siqi Chen (the frontmatter also declares `license: MIT`, `metadata.version: 3.1.0`). The upstream `LICENSE` is kept next to this file; it applies to these copies, not to the rest of this repository.
- Vendored: 6 November 2026, **unmodified**. Files were downloaded as raw bytes from `raw.githubusercontent.com` at that commit.
- Not included: `scripts/`, `agents/`, the plugin manifests, `README.md`, `CHANGELOG.md`.

## Review before vendoring

The bytes were scanned for invalid UTF-8, invisible and bidirectional characters, HTML comments and tags, long encoded blobs, phrases aimed at an AI agent (ignore previous instructions, run, upload and similar) and install or shell commands, and the frontmatter was checked for permission fields. Nothing was found that tells an agent to do anything outside the task.

- About 32 KB (roughly 8k tokens) when loaded: keep it out of a project that does not edit prose often.
- Frontmatter uses `name`, `description`, `license` and `metadata`; no permission fields.
- Covers prose only; code blocks, commands and paths are left unchanged. Docstrings and code comments are not mentioned.

## Files (sha256)

| sha256 | path |
| --- | --- |
| `4ac4810254ab36d45419141aeb8e69bf50652cfafe5b2dab947d06d44e5cbf96` | `LICENSE` |
| `0612f1dfb1672b0ea9b97e139bf1f06cabe98d8b27424fe8ff01e1fb4cc99cad` | `skills/humanizer/SKILL.md` |

## Updating

Download the files again at a newer commit, repeat the review, replace the files, and update the commit, date and hashes here.
