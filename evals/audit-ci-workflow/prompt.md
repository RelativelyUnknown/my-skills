---
tags: [review, security, supply-chain]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill]
---

Audit our GitHub Actions workflows for security problems and report what you find. The repository is public and takes pull requests from forks. The workflow files are `.github/workflows/ci.yml`, `.github/workflows/labeler.yml` and `.github/workflows/release.yml`. Do not change any files.
