# Layer stack

**The reader asks:** What sits on what?

Stacked abstraction levels, each a band that depends only on the one below it (application over library over runtime over operating system).

- Builder: one `zone` per layer, stacked, labelled; two or three nodes inside each; `v` connectors only where a layer calls the next. A connector that skips a layer is the finding.
- Order: the layer users touch on top.
- Budget: 5 layers, 9 nodes. If everything calls everything, it is not layered, and a dependency graph is the honest picture.

Visual rules: [../style.md](../style.md). Connectors: [../connectors.md](../connectors.md). Check before reporting: `python3 assets/diagram/check.py out.svg`.
