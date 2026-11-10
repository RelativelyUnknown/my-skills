# Architecture decision record

One record per decision, numbered, kept in `docs/adr/NNNN-short-title.md`. It lets a stranger understand in a year why the code is shaped this way.

Write one when a decision would be expensive to reverse: a framework or major dependency, a data model or schema, an authentication scheme, a public API shape, a storage or wire format, going native. A choice that one commit can undo needs a commit message, not a record.

The project's convention comes first. If records exist, match their directory, file format, numbering, name pattern and headings, and continue the sequence. Use the template below only when there is none; if two conventions exist, say so instead of adding a third.

```markdown
# ADR NNNN: <decision as a short phrase>

- Status: proposed | accepted | superseded by ADR NNNN
- Date: YYYY-MM-DD
- Decided by: <people or meeting>

## Context
The forces: what we need, the constraints, what changed.

## Decision
What we do, in one or two sentences, in the active voice ("We keep jobs in a Postgres table").

## Alternatives considered
- <option>: why not (say "not evaluated" if that is the truth).

## Consequences
What gets easier, what gets harder, what we now have to maintain.
```

- An accepted record is not edited. A new decision gets a new record and the old one is marked superseded.
- State the cost of the decision as plainly as the benefit.
- Record the date and the deciders as given; do not invent reasons the deciders did not give.
