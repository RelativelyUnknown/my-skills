# Choosing and checking a diagram

A diagram answers one question a reader has about structure, order or state. Write that question down first. If a sentence, a table or a list answers it as well, write that instead: a list of things is a table, a before-and-after of attributes is a table, a single box is a sentence.

## Pick the type from the question

| The reader asks | Draw | Page |
| --- | --- | --- |
| What are the parts and who talks to whom? | architecture | [types/architecture.md](types/architecture.md) |
| In what order do things happen between parts? | sequence | [types/sequence.md](types/sequence.md) |
| What states can one thing be in, and what moves it? | state machine | [types/state.md](types/state.md) |
| What does the data look like? | entity-relationship | [types/entity-relationship.md](types/entity-relationship.md) |
| What are the steps, and where does it branch? | flowchart | [types/flowchart.md](types/flowchart.md) |
| Who does each step, and where does work change hands? | swimlane | [types/swimlane.md](types/swimlane.md) |
| Where does it run? | deployment | [types/deployment.md](types/deployment.md) |
| What depends on what? | dependency graph | [types/dependency.md](types/dependency.md) |
| When did or will things happen? | timeline | [types/timeline.md](types/timeline.md) |
| What sits on what? | layer stack | [types/layers.md](types/layers.md) |
| What changed? | two pictures with identical layout, the difference in the accent | this page |

One type per picture. If you need two, draw two. Read the type's page before drawing.

## Budget

- At most 9 nodes, 12 connections and 2 focal nodes (`check.py` fails more). Past that, split into an overview and a detail picture.
- Remove test, before reporting done: can a node go (would the reader still understand)? Do two nodes always travel together (merge them)? Is a connection obvious from the layout (remove the line)? Does a label repeat what colour or position already says?
- A node is a name plus, at most, one short lowercase role. The look, tokens and roles are in [style.md](style.md); connection kinds and label rules are in [connectors.md](connectors.md); icons in [icons.md](icons.md).

## Build

1. Write the spec: nodes with their grid positions (multiples of 4), edges with kinds, zones for groups. Start from an example in `assets/diagram/examples/`.
2. `node assets/diagram/make.mjs spec.json out.svg`. The canvas is fitted to the content; the SVG has real text, so it stays searchable and sharp, and carries `role="img"`, a `<title>` and a `<desc>`.
3. A diagram that lives in Markdown and must stay editable by hand: Mermaid, if the project already uses it. Do not convert existing diagrams between formats unasked.

## Verify

1. `python3 assets/diagram/check.py out.svg` must exit 0. It fails diagonals, labels touching nodes or arrowheads, lines behind boxes, node overlap, a picture past its budget, text under 10 px, a missing title or description, anything outside the viewBox, and any token pair below its contrast minimum. A failure is fixed in the spec, never waived without saying so.
2. `node assets/diagram/render.mjs out.svg --scale 2` writes `out.png` and `out-dark.png`. Look at both, at the size the picture will be shown: reading the SVG source proves nothing about balance. Check that the focal node is the first thing seen, that nothing crowds the edge, and that every label reads. Fix and render again.
3. If you cannot render here (no Playwright, and installing it needs a yes), say so in the report and leave the `check.py` result next to it.

Every fact in the picture comes from the code or from the user: a service, queue or arrow you cannot point to in the repository is marked as assumed or left out.
