# python-docs

Part of the [skills repository](../README.md). One skill, `writing-documentation`, for writing and editing software documentation the way well-documented projects do: Diátaxis page types, Google and Microsoft developer style, PEP 257 with numpydoc or Google docstrings, READMEs, changelogs, tested examples, no AI filler.

It is being folded into the routed `documentation` skill (written docs, diagrams, animation, writing for agents); see the repository README.

## What the skill covers

- Name the reader and their need first; one page serves one need (tutorial, how-to, reference, explanation).
- Follow the project's conventions (docs tool, docstring style, style guide) before the defaults. The defaults come from `AGENTS.md` (`## Python defaults`); the skill asks once if they are missing.
- Read the code and run the example before describing it.
- Voice and structure rules, content rules (specific, timeless, no filler), code-example rules, docstring formats.
- A filler check with one `grep` line, no script.

Docstring content rules (no conversation residue, no restated signatures) stay in `writing-python-code` in [python-engineering](../python-engineering/).

## Install

Copy `skills/writing-documentation` into your tool's skills folder (see the repository README).

## Evals

`skills/writing-documentation/evals/` holds `three-pages` (a tutorial, a how-to and a reference for one package; with the skill 0.91, without 0.76 over three runs per arm), `readme-for-small-package` and `numpydoc-docstrings`. `evals/writing-documentation.triggers.json` lists prompts that should and should not load the skill.

## License

MIT. Style rules summarize the Diátaxis framework, the Google developer documentation style guide, the Microsoft Writing Style Guide, PEP 257, numpydoc and the Wikipedia guide to signs of AI writing; sources are named in the reference files.
