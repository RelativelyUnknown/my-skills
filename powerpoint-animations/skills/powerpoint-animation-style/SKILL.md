---
name: powerpoint-animation-style
description: "Visual language for clean, looping explainer animations that go into PowerPoint: white 16:9 stage, one title, ink/grey/blue colour roles, no legends, pop/draw/fly motion. Use when designing or reviewing what a PowerPoint animation should look like, before writing any scene code."
---

# PowerPoint animation style

One look for every animation, so a deck of them reads as one set. Apply it before writing code; the engine in `building-animation-scenes` already implements it.

## The look

- **Stage:** white, 16:9 (960×540 design units, rendered at 1920×1080). One centred title (Inter 600, 26 px). Nothing else is permanent. No logo, legend, caption, footer or slide number.
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

## Motion vocabulary

Use only these; each does one job.

| Motion | Job |
| --- | --- |
| **pop** (scale in with slight overshoot) | a new object appears: dot, pill, tile |
| **draw** (stroke grows along a path) | a line, average or guide is being built |
| **fly** (ease in-out between two positions) | an object moves to a new place or role |
| **grow** (zone rises from the axis) | a region or bin is claimed |
| **drop** (dotted guide draws down, fades, pill pops) | a value is read off a chart into a result |
| **ring** (fade in, hold, fade out) | "look here" |
| **shake** (4 px, decaying, 0.45 s) | something failed, just before it changes |

Timing: 25 fps; whole loop 7–10 s; stagger siblings by 0.05–0.15 s; pop 0.25 s, draw 0.25–0.4 s, fly 0.5 s. Build in reading order (inputs, then method, then result). After the last event hold briefly, fade only the content (title stays) over 0.45 s, then show the title-only frame for 0.35 s so the loop restarts cleanly.

## Checklist

1. Can it be understood with no narration and no legend?
2. Do colours mean the same thing as in every other animation in the deck?
3. Is every element in the final frame necessary?
4. Does it loop without a visible jump?
