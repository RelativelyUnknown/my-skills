# Visual style

One look for every diagram and animation, so a set of them reads as one. Apply it before writing code; the engine in `assets/animation/` already implements it. Motion is in [motion.md](../animation/motion.md).

## design.md

If `design.md` (or `DESIGN.md`) exists at the repository root, read it before choosing anything. Its colours, typography, stage size and motion override the defaults below: map its primary colour to `ACCENT`, its neutral text and surface colours to `INK`, `LABEL`, `BASE` and the stage, and set them through `window.THEME` in `specs.js` (keys: `INK`, `LABEL`, `MUTED`, `GRID`, `AXIS`, `BASE`, `BASE_ZONE`, `ACCENT`, `ACCENT_MID`, `ACCENT_LIGHT`, `ACCENT_ZONE`, `SLOT`). Ask once only if the file does not say which colour is the accent. With no `design.md`, use the defaults and offer once to write a short one (accent, font, stage size); never create it unasked.

## The look

- **Stage:** white, 16:9 (960×540 design units, rendered at 1920×1080). One centred title (Inter 600, 26 px). Nothing else is permanent. No logo, legend, caption or footer.
- **Type:** Inter for titles, labels and names; JetBrains Mono for values, times and axis ticks. Sizes: title 26, panel label 20, body 14, ticks 12, pill 13.
- **Fills are flat.** No gradients, shadows, 3D or outlines on everything. Rounded corners (pills fully round, tiles r 8–9).

## Colour roles (meaning, not decoration)

| Role | Colour | Use |
| --- | --- | --- |
| Input, given data | ink `#111111` | the dots or items every side starts from |
| Baseline / "before" | grey `#808080`, zone `#F0F0F0` | everything the old or reference method produces |
| Result / "after" | accent `#004A96`; line `#4472AA`, guides `#7CA0C6`, zone `#E0E9F2` | everything the new method produces |
| No value | dashed outline `#BDBDBD` | an empty slot, a null, a gap |
| Selection | ink ring, 1.6 px | the one value the viewer should compare |

Rules: one accent only (swap it via `window.THEME` to match a brand); grey text `#555` for labels, `#8A8A8A` for axis numbers. If something needs a fourth colour, the design is doing too much.

## Layouts

- **Split screen** for comparisons: left grey, right accent, a hairline divider, the two labels at the top of each half. Both halves start from identical input and play in parallel so the eye compares timing as well as shape.
- **Full width** for a process (stages left to right, or a grid feeding lanes). Headers are small sans labels in the top row.
- Result values drop into a row of **pills** at the bottom (grey pills with ink text on the left, accent pills with white text on the right).

## Checklist

1. Can it be understood with no narration and no legend?
2. Do colours mean the same thing as in every other animation in the set?
3. Is every element in the final frame necessary?
4. Does it loop without a visible jump?
