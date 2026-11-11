# Known defaults to refuse

These are what an interface drifts into when nobody decides. Each is a default, not a ban: the brief's own words can earn one, and reaching for one without a reason means a decision was skipped. Items the checker detects are marked (c). Fix the element, do not soften it.

## Scaffolds

- Same-size cards of icon, heading and text as the whole page structure. Cards inside cards. (Use a table for tabular data, a list for a list.)
- The hero-metric block: one huge number, a small label, supporting stats, an accent.
- A small label above a heading (an eyebrow), or section numbers (01, 02, 03) when order carries no meaning. The heading carries its own weight.
- A modal for something that needs no interruption.
- A page with a card and a gradient for every idea; one idea per screen needs one treatment.

## Surfaces

- Gradient text (c). Emphasis is weight or size.
- Glass and blur as decoration; backdrop blur on many elements (c, warning).
- A coloured side stripe on a card, callout or list item: a border of 3 px or more on one side only (c).
- A hard offset block shadow (`6px 6px 0`) in a design that is not deliberately that style (c).
- A coloured glow: a zero-offset shadow with a wide blur (c).
- A hairline border under a wide soft shadow (the "ghost card"). Pick one device.
- Over-rounded corners (a 40 px radius on a card) and pills used for everything.
- Decorative backgrounds: grid lines, stripes, noise, radial halos, with nothing real under them.
- Sparklines, progress rings and soft-shadowed rectangles standing in for content.
- Unicode glyphs or emoji as icons. One icon set, one stroke weight.

## Type and colour

- A system display face as a headline voice when the page has its own world; the nearest installed font is a failure, not a fallback.
- Mono type as a costume for "technical". It is for code, identifiers and aligned figures.
- A flat hierarchy: every level the same weight and size. Crushed tracking, all-capital body text, justified text, a single word alone on the last line.
- Grey text on a coloured background. Low-contrast text (c).
- Purple-to-blue gradients, glowing accents on near-black, a cream palette chosen because it is fashionable. Pick the theme from where and when the page is used.
- Tiny text under 12 px (c).

## Motion

- The same fade-and-rise on every section as it scrolls into view.
- Pulsing status dots, blinking cursors, marquees, bounce or elastic easing.
- Infinite animations that ignore `prefers-reduced-motion` (c).

## Copy

- Generic claims ("a seamless, powerful platform"), forced contrast ("Not a tool. A platform."), and puffery. Say what it does.
- The same sentence repeated inside one block; filler in a button; an error with no way out.
- Figures, quotes, logos or testimonials the project does not have. Mark a placeholder as one.
- Em dashes used as a tic. (See `documentation/ai-patterns.md` for the wider list.)

## Never the whole page

A page that avoids every item above is not thereby good. These are floors. Spend the page on a clear brief, real content and one committed choice of look.
