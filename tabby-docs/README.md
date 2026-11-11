# documentation

A skill of the Tabby plugin for writing and editing software documentation by what the reader needs: Diátaxis page types plus history, operations, troubleshooting and governance pages, concise style, runnable examples, and no AI filler.

**Entry point:** [`SKILL.md`](SKILL.md), about 540 tokens: the never-miss rules and a workflow that ends in an edit pass for filler. [`pages.md`](pages.md) lists the page-type leaves.

## Layout

```
SKILL.md                             rules and workflow
pages.md                              the page-type leaves, by reader need
tutorial.md  how-to.md  reference.md  explanation.md         the four reader needs
docstrings.md  readme.md  changelog.md  placing.md           where and in what form
commits.md  drift.md                                         commit messages; docs in step with code
voice.md  style.md  concision.md  ai-patterns.md  code-examples.md
history/        adr.md                                       decisions and rationale
operations/     runbook.md                                   incident and setup steps
troubleshooting/  symptom-fix-matrix.md                      fast fault isolation
governance/     contributing.md                              rules for collaborators
```

Every folder has an `index.md`. Docstring content rules (no conversation residue, no restated signatures) live in [`../tabby/development/code/comments.md`](../tabby/development/code/comments.md).

## Evals

In [`../evals/`](../evals/): `three-pages` (a tutorial, a how-to and a reference for one package), `readme-for-small-package`, `numpydoc-docstrings`, `adr-runbook-troubleshooting`, `agents-md-for-a-repo`.

## Licence

MIT.
