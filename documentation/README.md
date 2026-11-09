# documentation

Part of the [skills repository](../README.md). One skill for writing and editing software documentation the way well-documented projects do: Diátaxis page types, concise style, PEP 257 with numpydoc or Google docstrings, READMEs, changelogs, tested examples, no AI filler.

`SKILL.md` holds the never-miss rules and the workflow (including a filler check as one `grep` line). `references/written/` holds the leaves, read by what the reader needs: `tutorial`, `how-to`, `reference`, `explanation`, `docstrings`, `readme`, `changelog`, `placing`, `voice`, `style`, `concision`, `ai-patterns`, `code-examples`, and `governance/contributing`. Docstring content rules (no conversation residue, no restated signatures) live in `python-engineering/references/fields/software-engineering/all/code/comments.md`.

`references/written/` also holds `history/adr`, `operations/runbook`, `troubleshooting/symptom-fix-matrix` and `governance/contributing`. `references/diagrams/style.md` is the visual language for diagrams and animations (it reads a `design.md` at the repository root when there is one) and `references/animation/` covers the pipeline (SVG scenes drawn as a function of time, headless Chromium frames, ffmpeg encodes), motion and formats; the engine is in `assets/animation/`.

The animation pipeline was moved here from an earlier skill and has not been run again since the move.

Not built, for lack of a failing baseline: release notes, migration guide, incident manual, onboarding checklist, post-mortem, SLA, security policy, code standards, `AGENTS.md` and skill-authoring leaves (the bare model already writes a sound `AGENTS.md`; the documentation skill did not fire on that prompt).

## Evals

`evals/` holds `three-pages` (a tutorial, a how-to and a reference for one package), `readme-for-small-package` and `numpydoc-docstrings`, plus `documentation.triggers.json`. Over three runs per case with `--ablation none`, the earlier flat skill scored 0.875 and the routed one 1.00 (mean of 3 cases); the routed form used more tokens (128k against 92k per run) and did not fire in the `numpydoc-docstrings` runs, where both scored well anyway. Three cases are too few to separate the two.

```bash
claude plugin eval documentation --scaffold --allow-tools Write Edit --judge-model sonnet --max-cost-usd 4
```

## License

MIT. Style rules summarize the Diátaxis framework, the Google developer documentation style guide, the Microsoft Writing Style Guide, PEP 257, numpydoc and the Wikipedia guide to signs of AI writing; sources are named in the leaves.
