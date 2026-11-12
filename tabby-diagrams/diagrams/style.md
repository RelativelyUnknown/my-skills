# Visual style

One quiet look for every picture, so a set of them reads as one. White ground, soft zones, tonal role fills, one accent. Depth comes from tone, not from outlines or shadows. Tokens below are the single source; `assets/diagram/make.mjs` and the animation templates read the same values. Choosing and checking a diagram: [choosing.md](choosing.md). Connector geometry: [connectors.md](connectors.md). Motion: [../animation/motion.md](../animation/motion.md).

## Build it, do not hand-place it

Write a small JSON spec (nodes, edges, optional zones) and run `node assets/diagram/make.mjs spec.json out.svg`. The builder applies the tokens, the 4 px grid, icons, connector routing and label pills, and writes light and dark into one SVG. Hand-drawn SVG is for a type the builder does not cover (a sequence diagram); it follows the same tokens and the contract at the end of this page.

## design.md

If `design.md` (or `DESIGN.md`) exists at the repository root, read it first and map it. Say in the report what was applied and what was not.

| design.md says | Spec `theme` key | What happens |
| --- | --- | --- |
| Primary or brand colour | `accent` | The focal tint is 12% of it over the surface. A readable `accent-text` is derived, mixed toward the ink until it reaches 4.5:1. |
| Background or surface | `surface` | Zone, node, hairline and tile fills are derived from the ink over it. One brand set gives one theme: there is no automatic dark variant. |
| Text colour | `ink` | Label (71%), line (52%), icon ink (78%) and hairline (14%) are derived from it. |
| Fonts | `font` | The design.md sans family goes first in the stack. It must be installed or loaded, or the fallback shows. |
| Corner radius, spacing, stage size, motion curves | not applied | Say so; do not promise them. |

Ask once only if the file does not say which colour is the accent. Always run `check.py` after mapping: a brand colour that fails a contrast pair is reported there, and the answer is to say so, not to hide it.

## Tokens

| Token | Light | Dark | Used for |
| --- | --- | --- | --- |
| `surface` | `#FFFFFF` | `#0E1016` | the canvas |
| `zone` | `#F5F6F9` | `#151824` | a container that groups nodes |
| `node` | `#FFFFFF` | `#171B28` | an ordinary node |
| `hair` | `#DADEE6` | `#2A3042` | node outline, secondary label outline |
| `ink` | `#14171F` | `#F1F3F8` | title, names |
| `label` | `#5B6270` | `#9BA3B4` | subtitle, role text, secondary labels |
| `accent` | `#2F5BEA` | `#7C9BFF` | the focal node, the main flow |
| `accent-text` | `#2F5BEA` | `#7C9BFF` | accent used as text (4.5:1 on the surface) |
| `accent-tint` | `#E8EEFF` | `#1C2547` | the focal node's fill |
| `tile`, `tile-ink` | `#EEF0F5`, `#3A4152` | `#20263A`, `#C7CEDF` | the icon tile and its icon |
| `line` | `#7A8294` | `#6A748C` | secondary and optional connectors (3:1 on the zone) |
| `on-accent` | `#FFFFFF` | `#0E1016` | an icon on the accent tile |

`check.py` tests the pairs that matter, in both themes. Light `label` on `zone` is 5.7:1 and `line` on `zone` 3.6:1; the limits are 4.5:1 and 3:1.

## Roles

One meaning for each treatment, in every diagram type:

| Role | Treatment |
| --- | --- |
| Focal (one, at most two) | `accent-tint` fill, `accent` outline, solid accent icon tile. The thing the reader must see first. |
| Ordinary node | `node` fill, `hair` outline, `tile` icon tile |
| Main flow | `accent`, 2.5 px, solid, one continuous route |
| Secondary connection | `line`, 1.75 px, solid |
| Optional, retry, build-time | `line`, 1.5 px, dashed |
| Group | a `zone` container with an uppercase label at its top left; no outline |

One accent only. A second saturated colour means the picture is doing too much. Never use the accent on more than two nodes.

## Type

- **Inter** for the title (28 px, 650, tracking -0.4), node names (15 px, 650), subtitle (15 px) and role text (11.5 px). Sentence case; the title is left aligned with one subtitle line under it.
- **JetBrains Mono** only for technical values: ports, paths, commands, column names and types. Not for ordinary role text.
- Connector labels are uppercase, 10.5 px, 600, tracking 0.5, in a pill that sits on the line. Nothing is below 10 px.

## Shape and space

- 4 px grid for every node origin, width, height and gap. Radius 24 on a zone, 14 on a node, 10 on a tile, fully round on a pill.
- A node is an icon tile (40 px) plus a name and, at most, one short lowercase role (`http server`, `job table`). A table node (entity, schema) is a header and mono rows.
- Gap between nodes on a row: at least the label pill's width plus 40 px (104 px for `ENQUEUE`), so the pill clears both boxes and the arrowhead. `check.py` fails a label closer than 16 px to its arrowhead.
- The canvas is fitted to the content with a 40 px margin unless width and height are given. Content that leaves a third of the canvas empty is on the wrong canvas.
- No gradients, no shadows, no glow, no decorative background pattern.

## Contract for a hand-drawn SVG

So that `check.py` can read it: `role="img"` and `aria-labelledby` pointing at a `<title>` (first child, the subject, under 60 characters) and a `<desc>` (one sentence about the content, not the geometry); a `<g data-node="id">` with a `<rect data-box>` per node; `<path data-edge="a>b">` per connector, right angles only; `<g data-pill="a>b">` per label. Colours and fonts come from the custom properties in `make.mjs`; set a text colour with a class, because the CSS rule beats a `fill` attribute.

## Checklist

1. Can it be understood with no narration and no legend?
2. Is there one focal node, and is it the one the reader must see first?
3. Do colours mean the same thing as in every other picture in the set?
4. `python3 assets/diagram/check.py out.svg` exits 0.
5. Rendered in light and dark and looked at, at the size it will be shown (`assets/diagram/render.mjs`).
