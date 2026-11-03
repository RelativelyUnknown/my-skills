# Docstrings and comments

The one home for these rules; `reviewing-python-changes` checks against them.

Write for a reader a year from now who never saw this conversation.

- Say what a function does, returns and raises, in positive terms ("Returns a new list", not "Doesn't modify the input"). Do not restate the signature or types. Private and self-explanatory functions get no docstring. A module docstring is one line of purpose, or none.
- No conversation residue: "as discussed", "per requirements", "we decided", "intentionally", "now uses", "no longer", "previously", "changed from", "fixed". History and rationale go in the commit message.
- Comments explain a non-obvious why; they never narrate the next line. A rule the code must keep is enforced by structure or a test, not a docstring. No references to internal docs, tickets or sections.
