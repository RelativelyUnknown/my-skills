# Flowchart

**The reader asks:** What are the steps, and where does it branch?

Steps in reading order, left to right or top to bottom, with a question node wherever the path splits. Use it for logic with real branches; a linear list of steps is a numbered list.

- Builder: a step is a node with an action icon; a decision is a node named as a question (`Retries left?`) with icon `git-fork` or `help`. Its two exits are labelled `YES` and `NO`, one `main` (the common path) and one `secondary`.
- Rejoin branches so the picture ends in one place; a dead end is a terminal node that says why (`Dropped`).
- Budget: 9 nodes. Two decisions in a row usually mean a table of cases is clearer.
- When who does each step matters, use [swimlane.md](swimlane.md) instead.

Visual rules: [../style.md](../style.md). Connectors: [../connectors.md](../connectors.md). Check before reporting: `python3 assets/diagram/check.py out.svg`.
