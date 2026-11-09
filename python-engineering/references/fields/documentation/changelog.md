# Changelog and release notes

Follow Keep a Changelog (keepachangelog.com) unless the project uses another format or a generator (towncrier, git-cliff, release-please).

```markdown
# Changelog

All notable changes to this project are documented in this file. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.0] - 2026-11-03

### Added
- `Client.stream()` yields response chunks without loading the body into memory.

### Deprecated
- `Client.download(path)`; use `Client.stream()` and write the chunks. Removal planned for 2.0.

### Fixed
- Retries no longer double the timeout on each attempt (#412).

[Unreleased]: https://github.com/<owner>/<repo>/compare/v1.4.0...HEAD
[1.4.0]: https://github.com/<owner>/<repo>/compare/v1.3.2...v1.4.0
```

- Sections, in this order, only when non-empty: Added, Changed, Deprecated, Removed, Fixed, Security.
- Newest version first; ISO 8601 dates; one entry per user-visible change.
- Written for users: what changed for them and what they must do. Name the public API, link the issue. Not commit messages, not internal refactors.
- Breaking changes say what breaks and the migration in the entry itself.
- Changes land under `[Unreleased]` with the code; the release moves them under the version.

## Release notes

Release notes are a curated, readable summary of a release, for announcements or a GitHub release:

- Lead with what most users care about (headline features, breaking changes) in two or three sentences.
- Then a migration section for breaking changes with before/after code.
- Then link to the full changelog. Do not paste it.

## Deprecation notices

In reference docs, mark deprecated APIs where readers look them up:

```rst
.. deprecated:: 1.4
   Use :meth:`Client.stream` instead. Removal is planned for 2.0.
```

MkDocs/mkdocstrings projects use an admonition or the docstring's `Deprecated` text. Always name the replacement and, when known, the removal version.
