# Making an animation

The default deliverable is one self-contained HTML file: the diagram as inline SVG plus a small player. No network, no dependencies, and it opens from a file. The picture is a pure function of time, so any moment can be reproduced (`window.__seek(t)`).

## Steps

1. **Thesis.** Write the three lines in [motion.md](motion.md): order, focus, why each motion.
2. **Spec.** Copy a template from `assets/animation/templates/` (`flow.json` a request through parts, `state-change.json` one thing moving through states, `before-after.json` a design change) and replace the nodes, edges and zones with the real ones, as in [diagrams/choosing.md](../diagrams/choosing.md). The look is the diagram look: [diagrams/style.md](../diagrams/style.md), with a `design.md` mapped through the spec's `theme`.
3. **Story.** Add the `story` list (the steps in [motion.md](motion.md)). Without one a default is generated: parts and main connectors appear in order, then one packet runs the main path.
4. **Build.** `node assets/animation/animate.mjs spec.json out.html`.
5. **Check the picture and the motion.** `python3 assets/diagram/check.py` on the static SVG (`node assets/diagram/make.mjs spec.json out.svg`), then `node assets/animation/check-motion.mjs out.html`. It fails a step budget, too many steps at once, a jump at the loop boundary, a page that moves under reduced motion, a request to the network, a script error and missing controls, and writes `contact-sheet.png`.
6. **Look.** Open the contact sheet: stills at the start, a quarter, half and three quarters of the story, its end and the last frame of the loop. Check that each still reads, the focus lands where intended, nothing overlaps mid-motion, and the first frame is not confusing.
7. **Deliver** the HTML. Video only when asked: [formats.md](formats.md).

## Needs

Playwright with Chromium for steps 5 and 6 (and for `assets/diagram/render.mjs`). Node 22 for every `.mjs` script. Ask before installing anything; if Playwright is not available, say that the motion was not checked and deliver the HTML with the `check.py` result.

## Proving the checkers

`python3 assets/diagram/selftest.py` and `node assets/animation/selftest-motion.mjs` run each checker against a clean example and against seeded defects. Run them after changing a checker, the builder, the player or the tokens.
