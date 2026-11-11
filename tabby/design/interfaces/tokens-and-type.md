# Tokens and type

One quiet system: neutral surfaces, one accent, one type family. The values are the diagram tokens in [../diagrams/style.md](../diagrams/style.md), so a project's pictures and screens look related. A `design.md` replaces them, and a project's existing tokens win.

## Colour as custom properties

```css
:root{--surface:#FFFFFF;--zone:#F5F6F9;--ink:#14171F;--label:#5B6270;--hair:#DADEE6;--accent:#2F5BEA;--accent-tint:#E8EEFF;--on-accent:#FFFFFF}
@media (prefers-color-scheme:dark){:root{--surface:#0E1016;--zone:#151824;--ink:#F1F3F8;--label:#9BA3B4;--hair:#2A3042;--accent:#7C9BFF;--accent-tint:#1C2547;--on-accent:#0E1016}}
```

- Text is `ink` or `label` on `surface` or `zone` (7:1 and 5:1 or better). Never a mid grey for body text.
- One accent for the one action or the one thing to notice. A second saturated colour is for status only (error, warning, success) and always arrives with words or an icon, never alone.
- On a coloured surface, tint the secondary text from that hue; do not drop a grey onto it.
- Dark mode follows `prefers-color-scheme` unless the project has its own switch. Check both.

## Type

- One family. Inter, or the project's. Mono only for code, identifiers and figures that must align.
- Body 16 px at line-height 1.5 (never below 14 px for anything a reader must read; the checker fails under 12). Headings 1.2. Scale by steps of about 1.2: 14, 16, 20, 24, 28, 36.
- Measure 60 to 70 characters for running text (`max-width: 68ch`). Wider reads badly; the checker warns past about 90.
- Sentence case. Weight (400, 600, 700) and size give emphasis, not colour, gradients or capitals. Tracking no tighter than -0.02em.
- Figures in tables and dashboards use `font-variant-numeric: tabular-nums` and are right aligned.
- Balance a headline (`text-wrap: balance`); avoid a lone word on the last line of a paragraph (`text-wrap: pretty`).

## Space and shape

- 4 px grid: 4, 8, 12, 16, 24, 32, 48, 64. More space around a group than inside it, and more above a heading than below it.
- Radius 10 on controls, 14 on cards, fully round on pills and chips. One radius per kind of thing.
- Depth is one device: a hairline border or a soft shadow with a real offset and blur, not both on one card. No glow, no hard offset block shadow.
- Focus: a visible 3 px ring in `accent` with a 2 px offset on every focusable element, never removed.
- Touch targets 44 px (24 px is the floor the checker fails below).

## The parts a browser draws

Selection colour, the caret, scrollbars, `::marker`, form controls (`accent-color`) and `color-scheme` ship with browser defaults that belong to nobody. Set `accent-color: var(--accent)`, `color-scheme: light dark` and a `::selection` from the palette: it is the cheapest sign that a page was built, not assembled.
