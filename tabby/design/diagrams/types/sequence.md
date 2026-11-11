# Sequence

**The reader asks:** In what order do things happen between parts?

One column per participant, time running down, a horizontal arrow per message. The builder does not draw lifelines: draw it by hand with the contract in [../style.md](../style.md), the same tokens and the same pill labels.

- Header: each participant is a node-style box in a row at the top; a dashed `line`-colour lifeline drops from it.
- Messages: a solid arrow for a call, a dashed arrow for a return. The label names the call (`POST /orders`), above the arrow, on a pill if it crosses a lifeline.
- Activation: a narrow `accent-tint` bar on the lifeline while a participant works. At most one focal message.
- Budget: 5 participants, 12 messages. Past that, split by phase (a happy path and a failure path are two pictures).
- Alternatives (`alt`, `loop`) are a labelled `zone` behind the messages they wrap; more than one nesting level means the flow belongs in a flowchart or in prose.

Visual rules: [../style.md](../style.md). Connectors: [../connectors.md](../connectors.md). Check before reporting: `python3 assets/diagram/check.py out.svg`.
