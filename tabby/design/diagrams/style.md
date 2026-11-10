# Visual style

One look for every diagram and animation, so a set of them reads as one. The tokens below are the single source: the animation engine's defaults (`assets/animation/common.js`) and static diagrams use the same values, in a light and a dark set. Apply before writing code. Motion is in [motion.md](../animation/motion.md); choosing and checking a diagram is in [choosing.md](choosing.md).

## design.md

If `design.md` (or `DESIGN.md`) exists at the repository root, read it first and map it as below. Say in the report what was applied and what was not.

| design.md says | Token | What happens |
| --- | --- | --- |
| Primary or brand colour | `ACCENT` | The three tints are derived over the surface (zone 12%, light 52%, mid 77% of the accent; the mid line is raised until it keeps 3:1 against the surface). |
| Background or surface | `SURFACE` | The stage, or the SVG's background. |
| Text colour | `INK` | Label, muted, grid, axis and empty-slot colours are derived from ink over the surface (71, 49, 7, 23 and 28%). |
| Secondary or neutral grey | `BASE` | Its zone is derived (12%). |
| Fonts (headings, body, code) | `FONT.sans`, `FONT.mono` | The design.md family goes first in the stack, the default stack after it. The font must be installed or loaded, or the fallback shows. |
| Corner radius, spacing | the layout constants | Set by hand: tiles radius 8 to 9, pills fully round, 4 px grid. |
| Stage size or aspect, motion curves and durations | not applied | The stage is 960×540 and the motion vocabulary is fixed. Say so; do not promise them. |

Ask once only if the file does not say which colour is the accent. For a static diagram, write the mapped values into the SVG's custom properties (skeleton below). For an animation, set `window.THEME` in `specs.js` (keys `ACCENT`, `BASE`, `SURFACE`, `INK`, `LABEL`, `MUTED`, `GRID`, `AXIS`, `SLOT`, `FONT`). Give both the same values. With no design.md use the defaults below, and offer once to write a short one (accent, surface, fonts); never create it unasked.

## Tokens

| Token | Light | Dark |
| --- | --- | --- |
| `SURFACE` | `#FFFFFF` | `#0F1115` |
| `INK` (given data, names) | `#111111` | `#F2F2F2` |
| `LABEL` | `#555555` | `#B0B1B2` |
| `MUTED` (axis numbers) | `#8A8A8A` | `#7E7F81` |
| `GRID` / `AXIS` | `#EEEEEE` / `#C9C9C9` | `#1F2124` / `#434548` |
| `BASE` (baseline, secondary) | `#808080` | `#9AA0AA` |
| `BASE_ZONE` | `#F0F0F0` | `#202227` |
| `ACCENT` (focus) | `#004A96` | `#6FB0FF` |
| `ACCENT_MID` / `ACCENT_LIGHT` / `ACCENT_ZONE` | `#4472AA` / `#7CA0C6` / `#E0E9F2` | `#598BC9` / `#41648F` / `#1B2431` |
| `SLOT` (empty, dashed) | `#BDBDBD` | `#4F5053` |

Light values are the engine's defaults. Dark values are what the engine derives from `SURFACE #0F1115`, `INK #F2F2F2`, `ACCENT #6FB0FF` and `BASE #9AA0AA`, so a dark theme needs only those four keys. Known weak spot: light `MUTED` is 3.5:1 on white, below 4.5:1 for small text; use `LABEL` for anything a reader must read.

**Type:** sans for titles, labels and names, mono for values, times, ports and axis ticks. Stacks: sans `Inter, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`; mono `"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`. Sizes: title 26, panel label 20, body 14, ticks 12, pill 13. The engine bundles Inter and JetBrains Mono from npm; a static SVG relies on the stack, so its fallbacks must look acceptable.

**Fills are flat.** No gradients, shadows or 3D. Rounded corners (pills fully round, tiles radius 8 to 9).

## Roles

One meaning for each colour, in every diagram type:

| Role | Token | Use |
| --- | --- | --- |
| Given | `INK` | Input data, names, the things every side starts from |
| Baseline, secondary | `BASE`, `BASE_ZONE` | The old or reference method; secondary connections |
| Focus | `ACCENT` family | The one thing to look at: the result in a comparison, the main flow in an architecture picture |
| Empty | `SLOT`, dashed | A null, a gap, a build-time or deploy-time relation |
| Selection | `INK` ring, 1.6 px | The one value to compare |

One accent only. If something needs a fourth colour, the picture is doing too much.

## Static diagram skeleton

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 540" role="img" aria-labelledby="d-title d-desc">
  <title id="d-title">Short name of the subject</title>
  <desc id="d-desc">One sentence about the content, not the geometry.</desc>
  <style>
    :root { --surface:#FFFFFF; --ink:#111111; --label:#555555; --base:#808080; --accent:#004A96; --accent-zone:#E0E9F2; --slot:#BDBDBD;
            --sans:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; --mono:"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }
    @media (prefers-color-scheme: dark) { :root { --surface:#0F1115; --ink:#F2F2F2; --label:#B0B1B2; --base:#9AA0AA; --accent:#6FB0FF; --accent-zone:#1B2431; --slot:#4F5053; } }
    text { font-family: var(--sans); fill: var(--ink); } .mono { font-family: var(--mono); }
  </style>
  <rect width="960" height="540" fill="var(--surface)"/>
  <!-- nodes and connections use only these variables -->
</svg>
```

With a design.md, replace the values (and the font stacks) in the two blocks and keep the rest.

## Layouts (animation stage)

- **Stage:** surface colour, 16:9 (960×540 units, rendered at 1920×1080). One centred title (sans 600, 26 px). Nothing else is permanent: no logo, legend, caption or footer. This is the animation stage; a static architecture diagram may carry group labels and a legend if it needs them.
- **Split screen** for comparisons: left grey, right accent, a hairline divider, the two labels at the top. Both halves start from identical input and play in parallel.
- **Full width** for a process: stages left to right, headers as small sans labels in the top row.
- Result values drop into a row of **pills** at the bottom (grey with ink text on the left, accent with `ON_ACCENT` text on the right).

## Checklist

1. Can it be understood with no narration and no legend?
2. Do colours mean the same thing as in every other picture in the set?
3. Is every element in the final frame necessary?
4. Does it loop without a visible jump (animation)?
5. Light and dark both readable, if the picture will be shown on either.
