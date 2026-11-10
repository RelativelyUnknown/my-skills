# Docstrings and comments

The one home for these rules; the self-review in the `review` module checks against them.

Write for a reader a year from now who never saw this conversation.

Ask what the reader cannot get from the code: the reason a choice was made, a constraint that is invisible, what a caller may rely on. Write that, and nothing the code already says. Anything that only makes sense with this conversation or this week's state belongs in the commit message, where it stays true.

- Say what a function does, returns and raises, in positive terms ("Return a new list", not "Don't modify the input"). The summary line follows the project's docstring convention: imperative under PEP 257 and numpydoc ("Return ..."), descriptive is allowed under Google style ("Returns ..."); never mix them. Do not restate the signature or types. Private and self-explanatory functions get no docstring. A module docstring is one line of purpose, or none.
- No conversation residue: "as discussed", "per requirements", "we decided", "intentionally", "now uses", "no longer", "previously", "changed from", "fixed". History and rationale go in the commit message.
- Comments explain a non-obvious why; they never narrate the next line. A rule the code must keep is enforced by structure or a test, not a docstring. No references to internal docs, tickets or sections.
