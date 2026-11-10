# Choosing and checking a diagram

A diagram answers one question a reader has about structure, order or state. Write that question down first. If a sentence, a table or a list answers it as well, write that instead: a list of things is a table, a before-and-after of attributes is a table, a single box is a sentence.

## Pick the type from the question

| The reader asks | Draw |
| --- | --- |
| What are the parts and who talks to whom? | architecture: boxes grouped by what they share (a process, a host, a repository, a trust boundary) |
| In what order do things happen between parts? | sequence: one lifeline per part, time downward |
| What states can one thing be in, and what moves it? | state machine: states, transitions, terminal states |
| What does the data look like? | entity-relationship: tables or types, keys, cardinality |
| What are the steps, and where does it branch? | flowchart, or swimlanes when who does each step matters |
| What changed? | two pictures with identical layout, the difference in the accent colour |

One type per picture. If you need two, draw two.

## Budget

- At most 9 nodes and 12 connections. Past that, split into an overview and a detail picture.
- One or two accented elements: the focus (see Roles in [style.md](style.md)). Accent on everything is accent on nothing.
- Remove test, before reporting done: can a node go (would the reader still understand)? Do two nodes always travel together (merge them)? Is a connection obvious from the layout (remove the line)? Does a label repeat what colour or position already says?

## Nodes and connections

- A node is a name plus, at most, one short role in lowercase (`http server`, `job table`). Names in the sans face; ports, commands and paths in mono.
- Three kinds of connection, and no more: the main request or data path (the focus colour, solid, one continuous route), secondary runtime connections (`BASE`, solid), build-time or deploy-time relations (`SLOT`, dashed).
- Connections run horizontally and vertically, with right-angle bends. No diagonals, no two lines on top of each other, no line passing behind a box it does not connect to.
- A label sits beside its line on a background patch, never on the stroke, and never rotated.
- No legend inside the drawing; if the picture needs one, the roles are not clear enough.

## Format

- SVG with real text, so it stays searchable and sharp. Start from the skeleton in [style.md](style.md): its custom properties carry the colour and font tokens (light and dark), and a design.md replaces their values.
- Accessible by default: the skeleton's `role="img"`, `<title>` (the subject, under 60 characters, first child) and `<desc>` (one sentence about the content, not the geometry), referenced by `aria-labelledby`.
- Diagrams that live in Markdown and must stay editable by hand: Mermaid, if the project already uses it. Do not convert existing diagrams between formats unasked.

## Verify by looking

Render the picture to PNG at the size it will be shown and read it; reading the SVG source proves nothing about overlaps. Check: no line crosses a label, no arrowhead lands in text, nothing is clipped at an edge or sticks out of its group, every label is readable at that size. Fix and render again. If you cannot render here, say so in the report.

Every fact in the picture comes from the code or from the user: a service, queue or arrow you cannot point to in the repository is marked as assumed or left out.
