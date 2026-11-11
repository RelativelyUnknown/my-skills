# State machine

**The reader asks:** What states can one thing be in, and what moves it?

A node per state, a connector per transition, labelled with the event that causes it. The start is where the reader looks first; terminal states say so in their role (`closed`).

- Builder: states in one row along the happy path (`main` connectors), exits and error states below it (`optional`, routes `vh`, `below`). Example: `assets/diagram/examples/order-states.json`.
- Focal: the state where the interesting work happens, not the first one.
- A guard goes in the label (`PAID`, `NO STOCK`), never in a second line of small text.
- Budget: 9 states, 12 transitions. A state with transitions to every other state is a flag in disguise; merge or split it.
- Every state and event comes from the code or the user; one you cannot point to is marked as assumed.

Visual rules: [../style.md](../style.md). Connectors: [../connectors.md](../connectors.md). Check before reporting: `python3 assets/diagram/check.py out.svg`.
