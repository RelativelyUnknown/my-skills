# Diagram quickstart

Everything needed for a first correct diagram. Write the file first, then look; read the other pages only when a check finding or an unusual request needs them.

1. **Is a picture needed?** If a sentence or a table answers the reader's question, write that. Otherwise note the question and the type: parts and who talks to whom (architecture), states and what moves them (state), tables and relations (entity-relationship), steps with branches (flowchart), who does each step (swimlane), where it runs (deployment). One type per picture, at most 9 nodes and 12 connections.
2. **Copy the closest spec** from `assets/diagram/examples/`: `service-request.json` (parts and flow), `order-states.json` (states), `shop-tables.json` (tables), `fan-out.json` (one part feeding several). Replace the content with what is really in the code; a part or arrow you cannot point to is left out or marked assumed.

```json
{ "id": "svc", "title": "A request through the service", "subtitle": "One sentence.",
  "zones": [{ "label": "Your service", "x": 244, "y": 156, "w": 756, "h": 348 }],
  "nodes": [{ "id": "api", "name": "API", "role": "http server", "icon": "server", "x": 288, "y": 236 },
            { "id": "queue", "name": "Queue", "role": "redis list", "icon": "stack-2", "x": 548, "y": 236, "focal": true }],
  "edges": [{ "from": "api", "to": "queue", "label": "ENQUEUE", "kind": "main" }] }
```

3. **Place on the 4 px grid.** A node is about `64 + 8.8 × len(name)` or `64 + 6.6 × len(role)` px wide (the longer), plus 16. Next node on a row: `x + width + 104` when the connector has a label (`+ 64` without). Rows 88 px apart. Zones 24 px outside their nodes. `icon` is a Tabler name: `node assets/diagram/make.mjs --icons <word>` lists matches (`server`, `database`, `stack-2`, `cpu`, `device-desktop`, `cloud`, `clock`). Exactly one `focal` node. If the repository has a `design.md`, add `"theme": { "accent": "#...", "surface": "#...", "ink": "#...", "font": "..." }` from it and say what was not applied ([style.md](style.md)).
4. **Build, then check:**

```bash
node assets/diagram/make.mjs spec.json docs/diagram.svg
python3 assets/diagram/check.py docs/diagram.svg        # exit 0 is required; fix findings in the spec, not the SVG
```

   Typical findings: a label too close to an arrowhead (widen the gap), a node off the grid (warning), too many nodes. The file now exists and is valid.
5. **Look once**, if Playwright is available: `node assets/diagram/render.mjs docs/diagram.svg --scale 2` writes light and dark PNGs; check that the focal node reads first and nothing crowds. If it is not available, do not install it: say the picture was checked but not rendered.
6. **Report:** what it shows, anything assumed, the checker result.

Need more: [style.md](style.md) (look, theme mapping), [connectors.md](connectors.md) (routes, fan-out), [icons.md](icons.md), [types/](index.md) (one page per type), [choosing.md](choosing.md).
