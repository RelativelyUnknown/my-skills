# Dependency graph

**The reader asks:** What depends on what?

Use it when fan-in or a cycle makes a tree wrong. Direction is "depends on": the arrow points at the dependency.

- Builder: put the most depended-on node at the right or bottom, the entry points at the left or top, so arrows run one way. A cycle is drawn as one `optional` connector back, with the label `CYCLE`; it is the finding, so make it the focal edge's neighbour.
- Group by package with zones when there are more than 9 modules, and show one picture per package.
- A picture of every import in a project is a hairball. Draw the modules the question is about and their direct neighbours only.

Visual rules: [../style.md](../style.md). Connectors: [../connectors.md](../connectors.md). Check before reporting: `python3 assets/diagram/check.py out.svg`.
