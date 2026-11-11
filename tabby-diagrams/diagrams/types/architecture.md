# Architecture

**The reader asks:** What are the parts, and who talks to whom?

Boxes grouped by what they share: a process, a host, a repository, a trust boundary. Each group is a `zone`; a part outside every zone is external (a client, a third-party API).

- Builder: nodes in one or two rows, one zone per group, `main` connectors for the request path, `secondary` for the rest, `optional` for retry and build-time links. Example: `assets/diagram/examples/service-request.json`.
- One part feeding several (a router, a queue to its consumers): put the targets in a column and use the `z` route with `slot` ([../connectors.md](../connectors.md)); example `assets/diagram/examples/fan-out.json`.
- Budget: 9 nodes, 12 connections, one or two focal nodes (the part the reader came to understand).
- Name the node by what it is (`Queue`) and its role by what it runs (`redis list`). Ports and paths go in mono (`"mono": true`).
- Every part and arrow must be real: one you cannot point to in the code is marked as assumed or left out.
- Past 9 nodes: an overview with one zone per subsystem, then one picture per subsystem.

Visual rules: [../style.md](../style.md). Connectors: [../connectors.md](../connectors.md). Check before reporting: `python3 assets/diagram/check.py out.svg`.
