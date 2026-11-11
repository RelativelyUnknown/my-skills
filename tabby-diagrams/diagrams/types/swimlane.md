# Swimlane

**The reader asks:** Who does each step, and where does work change hands?

One horizontal band per actor (a person, a team, a service), steps inside their owner's band, connectors crossing bands where work is handed over.

- Builder: one `zone` per lane, full width and stacked, labelled with the actor; nodes inside; connectors between lanes use `vh` or `v`. A handoff is the connector worth labelling.
- Lane order follows the flow: the actor who starts is on top.
- Budget: 4 lanes, 9 steps. More lanes usually mean two processes.

Visual rules: [../style.md](../style.md). Connectors: [../connectors.md](../connectors.md). Check before reporting: `python3 assets/diagram/check.py out.svg`.
