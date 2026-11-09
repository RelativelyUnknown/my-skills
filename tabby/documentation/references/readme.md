# README

The README is a landing page. A visitor decides in under a minute whether the project solves their problem and how to try it. Model READMEs: HTTPX, Polars, Ruff, uv, Rich.

Order:

1. **Name and one sentence** saying what it is and for whom: "HTTPX is a fully featured HTTP client for Python 3, with sync and async APIs." Not a tagline, not a list of adjectives.
2. **Status badges**, a few at most: version, supported Python versions, CI, license. No badge wall.
3. **Install**: one command (`pip install <pkg>` or `uv add <pkg>`), plus extras if they matter.
4. **Example**: the shortest program that does the main job, with its output. It runs as written, and a test runs it.
5. **Features or why**: optional, three to six concrete points with numbers where they exist ("Parses 1 GB of CSV in 2 s on a laptop; see benchmarks"), not superlatives.
6. **Links**: documentation, changelog, contributing guide, issue tracker.
7. **License** in one line.

Leave out: long API reference, full configuration tables, a table of contents for a short file, "Introduction" headings, emoji headings, roadmap promises.
