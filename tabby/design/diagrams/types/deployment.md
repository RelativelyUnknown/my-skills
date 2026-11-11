# Deployment

**The reader asks:** Where does it run?

Zones for hosts, regions or clusters; nodes for the artifacts that run there (a container, a process, a function); connectors for the traffic between them. Ports, image names and paths are technical values and go in mono.

- Builder: one zone per boundary, nested one level at most (a region holding two hosts), `"mono": true` on nodes whose role is a port or image (`:8000`, `api:1.4`).
- Show replicas as a count in the role (`3 replicas`), not as three identical boxes.
- Mark what is public: the edge from outside the outermost zone is the `main` connector.
- Budget: 9 nodes. Show what you can point to in the repository (a Dockerfile, a compose file, a manifest); anything else is marked assumed.

Visual rules: [../style.md](../style.md). Connectors: [../connectors.md](../connectors.md). Check before reporting: `python3 assets/diagram/check.py out.svg`.
