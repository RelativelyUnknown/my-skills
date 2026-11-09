# Architecture decision record

One record per decision, numbered, kept in `docs/adr/NNNN-short-title.md`. It lets a stranger understand in a year why the code is shaped this way.

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
