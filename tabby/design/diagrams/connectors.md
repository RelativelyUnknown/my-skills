# Connectors and labels

A connector says one thing: this part hands something to that part. Draw it so the eye follows it without effort. `assets/diagram/make.mjs` routes and labels connectors by these rules; `check.py` fails a diagonal (rule 1), a label touching a node or closer than 16 px to its arrowhead (rule 3) and a line behind a box (rule 4); rules 2, 5 and 6 are kept by the builder and checked by looking.

## Rules

1. **Right angles only.** A straight horizontal or vertical run, or a run with a rounded elbow (radius 12). No diagonals, no curves that wander.
2. **A node is its box, not its tile.** Connect box edge to box edge, 4 px off the border, never through the text. The arrowhead tip is the path's end; it is 12 px long, so a label keeps 16 px clear of it.
3. **A label sits on its line, in a pill that masks the line.** The pill is wide enough for its text (`text length × 6.6 + 16`), centred on the connector's longest run, with the same fill as the canvas. Never rotated, never touching a node.
4. **No line behind a box it does not connect.** Route around, or move the node. Crossing another line is acceptable; crossing a box is not.
5. **Nothing overlaps.** Two connectors never share a stroke. Where several leave one box edge, each gets its own attach point at least 12 px apart.
6. **Draw lines before boxes** so a box always sits on top of a line it hides a few pixels of.

## Three kinds of connection, and no more

| Kind | Meaning | Look |
| --- | --- | --- |
| `main` | the request or data path the reader should follow, one continuous route | accent, 2.5 px, solid |
| `secondary` | other runtime connections | line colour, 1.75 px, solid |
| `optional` | retry, return, build-time or deploy-time relation | line colour, 1.5 px, dashed |

If two connectors need different meanings, a legend is not the answer: label them, or split the picture.

## Routes in the builder

`h` (same row) and `v` (overlapping columns) are chosen automatically. `hv` and `vh` make one elbow. `below` and `above` draw a U that leaves and returns through the bottom or top edge, for a retry or a return path:

```json
{ "from": "worker", "to": "queue", "label": "RETRY", "kind": "optional", "route": "below" }
```

A connector that needs two elbows and a detour means the layout is wrong: move a node.

## Labels

One or two short words in capitals, naming the action (`POST`, `ENQUEUE`, `RETRY`), not repeating what the endpoints already say. A connector the reader can understand from position alone gets no label. Leave at least the pill width plus 40 px between two nodes on a row that carry a label.
