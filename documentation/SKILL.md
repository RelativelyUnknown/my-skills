---
name: documentation
description: "Use when writing, updating or reviewing a README, docstrings, API reference, tutorial, how-to, changelog, runbook, ADR or CONTRIBUTING file, or making a minimalist explainer animation or diagram. Applies Diátaxis page types, concise style, runnable examples; avoids AI filler."
license: MIT
---

# Documentation

Documentation lets a reader do or understand something without asking the author. Every sentence either moves the reader toward that or goes.

Defaults: read the `## Python defaults` section of AGENTS.md (`docstrings`); infer what is missing from the repo; ask only what is still unknown, once; save the answers there.

## Never miss

- Name the reader and their need first. One page serves one need; if a page needs two, write two and link them.
- Follow the project's conventions over these defaults: the docs tool (`mkdocs.yml` means MkDocs, `docs/conf.py` means Sphinx), the docstring style (`[tool.ruff.lint.pydocstyle] convention`, or read five existing docstrings), a style guide or `.vale.ini`, the changelog format, the English variety. Report differences as suggestions; do not convert existing docs unasked.
- Read the code and run it before describing it. Documentation that states intended behavior instead of actual behavior is a bug. If the code and the existing docs disagree, report it rather than picking one silently.
- Be specific (numbers, versions, exact messages) and timeless (no "currently", "now", "new").
- Every example runs as written, and a test runs it.

## Route

Written docs: read `references/written/index.md`, then the leaf for the page type. An explainer animation or diagram: read `references/diagrams/style.md` and `references/animation/index.md`.

## Workflow

1. Outline with headings only; check each heading against the page type.
2. Draft. Write the example first, run it, then write the prose around it.
3. Grep for filler: `grep -rniwE "seamless(ly)?|robust|powerful|comprehensive|delve|leverag(e|es|ed|ing)|utili[sz]e|holistic|simply|just|easily|obviously|basically|actually|in order to|note that|currently|recently|soon|as discussed|feel free to" <files>`. Fix each hit or keep it with a reason; a quoted word or a technical term ("trivial" in a math sense) can stay. In reference pages also grep `will` for future tense. If the project has `.vale.ini`, run `vale` with it too.
4. Edit pass. Delete sentences that restate the heading, summarize the page, announce what comes next, or praise the software. Check that every step is an action, every claim is specific, every link works.
5. Report what you changed, which examples you ran and how, and which grep hits you kept and why.
