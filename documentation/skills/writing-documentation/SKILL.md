---
name: writing-documentation
description: "Writes and edits software documentation the way well-documented projects do: Diátaxis page types, Google and Microsoft developer style, PEP 257 and numpydoc or Google docstrings, READMEs, changelogs, tested examples, no AI filler. Use when writing or reviewing docs, a README, docstrings, a tutorial, a guide or release notes."
argument-hint: "[style=google docstrings=numpy]"
---

# Writing documentation

Documentation lets a reader do or understand something without asking the author. Every sentence either moves the reader toward that or goes. This skill keeps the core of *writing-clearly-and-concisely*: Strunk's composition rules and no AI patterns. It adds the conventions of well-documented projects: Diátaxis, the Google and Microsoft developer style guides, the Python devguide style guide, PEP 257 and numpydoc.

## Start

1. **Name the reader and their need.** One page serves one need:

| The reader wants to | Page type | It contains | It leaves out |
| --- | --- | --- | --- |
| learn by doing, as a beginner | Tutorial | One guided path to a working result, every step shown | Choices, alternatives, theory |
| reach a goal they already have | How-to guide | Steps toward that goal, starting from a stated precondition | Teaching basics, full option lists |
| look something up while working | Reference | Complete, accurate, consistently structured facts (API, CLI, config) | Instructions, opinions, narrative |
| understand why or how it works | Explanation | Context, design reasons, trade-offs, alternatives | Step-by-step instructions |

   If a page needs two types, write two pages and link them. Details and templates: [references/diataxis.md](references/diataxis.md).

2. **Follow the project's conventions over the defaults below.** Check the docs tool: `mkdocs.yml` means MkDocs, `docs/conf.py` means Sphinx. Check the docstring style (`[tool.ruff.lint.pydocstyle] convention`, or read five existing docstrings). Check for a style guide or `.vale.ini`, the changelog format and the English variety. Arguments (`style=`, `docstrings=`) override what you find. Report differences as suggestions; do not convert existing docs unasked.

3. **Read the code and run it before describing it.** Documentation that states intended behavior instead of actual behavior is a bug. If the code and the existing docs disagree, report it rather than picking one silently.

## Voice and structure

- Address the reader as "you". Present tense ("returns", not "will return"). Active voice; name who acts. Imperative for instructions ("Run", "Set").
- Lead with the point. A page's first sentence says what it is for; a section's first sentence answers its heading. No introductions that announce what follows.
- Sentence-case headings that name the task or topic: "Configure retries", not "Retries Configuration Options". Task headings start with a verb.
- Put the condition before the instruction: "To export a table, run ...". Put the goal before the location: "To change the schema, edit `config.toml`".
- Numbered lists for sequences, one action per step, with the expected result when the reader needs to check it. Bullets for unordered items. List items share a grammatical form.
- One idea per sentence; aim for under 25 words. Short paragraphs. Tables for options and comparisons with more than two attributes.
- Link text names its destination ("see [Authentication](#authentication)"); never "click here", "this" or a bare URL in prose.
- Code font for code, commands, file names, paths, parameters and literal values. Bold only for UI labels. Italics for a term at its definition, if at all.
- Use one term per concept, defined once, matching the API and UI exactly. Do not vary terms for style.

## Content rules

- **Be specific.** Numbers, versions, units, exact error messages, defaults. "Retries 3 times with exponential backoff starting at 1 s" beats "retries automatically".
- **Timeless.** No "currently", "now", "new", "recently", "soon", or promises about future features. History belongs in the changelog; plans belong in the issue tracker.
- **No minimizers, puffery or filler.** Not "simply", "just", "easy", "obviously"; not "powerful", "seamless", "robust", "blazing fast"; not "in order to", "note that", "it is important to note". A speed claim comes with a benchmark or is cut.
- **Affirmative and calm.** Say what works and how to do it. Reserve warnings for data loss, security and crashes, and state the consequence: "Deletes the table and its history; this cannot be undone." Collect security considerations in their own section and link to it.
- **Global readers.** No idioms, jokes or Latin abbreviations (write "for example", "that is"). Expand an acronym on first use unless it is better known than its expansion (HTML, URL, API).
- **Inclusive and accessible.** "allowlist/denylist", "primary/replica"; "they" for an unknown person. Alt text that states what an image shows; never rely on color alone.
- **Honest scope.** State requirements, supported versions and known limitations where readers will look for them. Do not hide a limitation in a footnote.

## Code examples

- Every example runs as written: imports, setup and realistic values included. A test runs it (doctest, an executed README block, or a docs test); an example nobody runs drifts.
- Show one concept per example, then the output when the reader needs it to confirm success.
- Shell commands are copy-pasteable: no `$` prompt mixed into the copied text, one command per line, output in a separate block. Placeholders look like `<YOUR_WORKSPACE_URL>` and are explained right after the block. Never a real token, password or internal hostname.

More in [references/code-examples.md](references/code-examples.md).

## Docstrings

What a docstring says (behavior, returns, raises; no conversation residue; no restated signature) is set by `writing-python-code` (`references/docs-and-comments.md`). How it is formatted follows the project's convention; for new code read [references/docstrings.md](references/docstrings.md). Short version: the summary line is one sentence ending in a period, imperative mood ("Return the ...") under PEP 257 and numpydoc; Google style projects may use "Returns the ..."; never mix the two in one project.

## Workflow

1. Outline with headings only; check each heading against the page type.
2. Draft. Write the example first, run it, then write the prose around it.
3. Lint: `python3 <this skill's folder>/scripts/lint_prose.py <files>` (add `--future` for reference pages). Fix each finding or keep it with a reason; a quoted word or a technical term ("trivial" in a math sense) can stay. If the project has `.vale.ini`, run `vale` with it too.
4. Edit pass. Delete sentences that restate the heading, summarize the page, announce what comes next, or praise the software. Check that every step is an action, every claim is specific, every link works.
5. Report what you changed, which examples you ran and how, and which linter findings you kept and why.

## Read when relevant

| Doing | Read |
| --- | --- |
| Planning a page or a whole docs set, or splitting a mixed page | [references/diataxis.md](references/diataxis.md) |
| Word choice, punctuation, numbers, dates, UI text, procedures | [references/style-guide.md](references/style-guide.md) |
| Writing docstrings or API reference | [references/docstrings.md](references/docstrings.md) |
| Writing a README, changelog, release notes or CONTRIBUTING | [references/readme-and-changelog.md](references/readme-and-changelog.md) |
| Writing or reviewing code samples | [references/code-examples.md](references/code-examples.md) |
| Reviewing a draft (yours or generated) for AI writing patterns | [references/ai-patterns.md](references/ai-patterns.md) |
| Tightening prose sentence by sentence | [references/composition.md](references/composition.md) |
