# Animation quickstart

Everything needed for a first correct animation: one self-contained HTML file. Write it first, then look; read [motion.md](motion.md) and [pipeline.md](pipeline.md) only when a check finding or an unusual request needs them.

1. **Thesis in three lines** (in your head or the reply): the order things happen, the one moment to remember, why each step exists. If the picture explains itself still, make the diagram instead ([../diagrams/quickstart.md](../diagrams/quickstart.md)).
2. **Copy a template** from `assets/animation/templates/`: `flow.json` (a request through parts), `state-change.json` (one thing moving through states), `before-after.json` (a design change). They are diagram specs plus a `story`; place nodes as in the diagram quickstart.
3. **Write the story**: at most 8 steps, at most 2 running at once, every step with a `why`.

```json
"story": [
  { "t": 0.0, "reveal": ["client", "api", "queue"], "stagger": 0.5, "why": "the parts appear in the order a request meets them" },
  { "t": 0.3, "draw": ["client>api", "api>queue"], "stagger": 0.5, "why": "each connection is made as the request uses it" },
  { "t": 2.8, "packet": ["client>api", "api>queue"], "dur": 1.6, "why": "the dot shows the path one request takes" },
  { "t": 4.4, "pulse": "queue", "why": "this is where work waits" } ]
```

   Other steps: `badge` (a count), `active` (a node takes the focal look), `hide` (the old part, with `"ghost": true` elements in before/after).
4. **Build, then check:**

```bash
node assets/animation/animate.mjs spec.json docs/flow.html
node assets/animation/check-motion.mjs docs/flow.html     # exit 0 required; needs Playwright
```

   `check-motion.mjs` writes a contact sheet; open it. If Playwright is not available, do not install it: run `python3 assets/diagram/check.py` on `node assets/diagram/make.mjs spec.json out.svg` and say the motion was not checked.
5. **Report:** the thesis in a line, the file, the checker results. Video only if asked: [formats.md](formats.md).
