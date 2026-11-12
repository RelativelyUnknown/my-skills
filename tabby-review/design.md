# Design review

Reviewing a diagram, an animation, an interface or a README picture, whether it is a diff or an existing page. Two independent assessments, one of judgment and one of measurement, then one report. Say nothing about what is fine beyond a short list of strengths; a clean picture gets a short "no findings".

## Two assessments, kept apart

**A. Judgment (before any checker output).** Look at the thing itself: render it (`../tabby-diagrams/assets/diagram/render.mjs` for a diagram, the contact sheet from `check-motion.mjs` for an animation, the page at 390 px and 1280 px in light and dark for an interface) and read the source. Answer:

- **Specific or generic?** Could an unrelated project use this unchanged? A picture or screen that fits any product is a finding.
- **Hierarchy and focus.** Is there one thing to see first, and is it the right one? Squint test: does it survive?
- **Truth.** Every part, arrow, figure, logo and quote exists in the code or the user's material. Anything invented or unmarked as assumed is a finding.
- **Fit to the reader's job.** The question a diagram answers (is it the one the reader has?), the mode of an interface (persuade, operate, read; one page, one mode).
- **Content and copy.** Labels that say something, controls named for their action, errors with a way out, no filler.
- **States and edges.** Empty, error, loading, long text, many items; the first frame of an animation; both themes.
- **Known defaults.** Anything in `../tabby-frontend/interfaces/refuse.md` that the brief did not earn.

**B. Measurement.** Run the checkers and record exit codes and findings exactly as printed:

| Subject | Command |
| --- | --- |
| a diagram | `python3 ../tabby-diagrams/assets/diagram/check.py file.svg` |
| an animation | `node ../tabby-diagrams/assets/animation/check-motion.mjs file.html` |
| an interface | `node ../tabby-frontend/assets/interfaces/ui-check.mjs <url or file>` |

A checker that cannot run (no Playwright) is reported as not run, never as passed. A waived finding is listed with its reason; judge the reason.

**Keep A and B apart.** A subagent for each, when the harness has one, with no sight of the other's output: the checker's findings anchor judgment. Finish and write down A before reading B. If subagents are not available, do A, write it down, then B, and start the report with the line `DEGRADED: single-context review (no subagent available)`.

## Report

1. **Verdict** in one line: ship, ship after the listed fixes, or rework, and why.
2. **Findings**, most serious first, at most seven. Each: where (element, file and line, or time in the animation), what is wrong, and the change that fixes it. A finding the checker made is marked `measured`; one from judgment is marked `judged` and says what you looked at.
3. **Strengths**, at most three, only ones that should survive the fixes.
4. **Not checked:** what you could not render or run, in one line each.

Do not edit the work under review. Do not repeat the checker's output as a list of your own findings. A finding with no concrete fix ("improve the hierarchy") is not a finding.
