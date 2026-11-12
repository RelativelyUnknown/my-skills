# Motion

Motion explains a change in order. If the picture explains itself still, leave it still. Write the thesis before you animate: what changes, in what causal order, and what the reader should notice. A motion with no purpose is cut.

## The thesis (three lines, before any story)

1. **Order:** what happens first, second, third (a request moves left to right; a state changes along its transitions).
2. **Focus:** the one moment to remember (the packet reaching the queue and the count rising; the queue appearing where the direct call was).
3. **Why each motion:** one short purpose per step, in its `"why"` field ("the packet shows the path a request takes"). A step you cannot justify in a few words goes; `check-motion.mjs` fails a step without a `why`.

## Vocabulary

Use these step kinds in `assets/animation/animate.mjs`; each does one job.

| Step | Job | Time |
| --- | --- | --- |
| `reveal` (fade in, rise 8 px) | a part appears, in the order the reader should meet it | 0.45 s |
| `draw` (line draws itself, then its label fades in) | a connection is made | 0.55 s |
| `packet` (a dot travels along connectors) | something moves through the system | set by `dur`, 1.5 to 2.5 s |
| `pulse` (one ring expands from a node) | "look here" | 0.7 s |
| `badge` (a count appears and updates) | a state change you can see (the queue fills) | 0.25 s |
| `active` (a node takes the focal look) | the one thing currently true (the order's state) | 0.2 s |
| `hide` (fades out) | the old way, replaced (before and after) | 0.3 s |

`reveal`, `draw` and `hide` take a list and a `stagger`, so one step can bring in a row of parts in turn.

## Rules

- **Budget:** at most 8 steps, at most 2 running at once, one focal moment. `check-motion.mjs` fails more.
- **Static first:** the picture without script is complete and correct; the player only hides parts at the start and shows them in order. Under `prefers-reduced-motion` the page shows the end state and offers "Play once".
- **Ease out, never bounce:** entrances decelerate (exponential ease-out); lines draw with an ease in-out; nothing overshoots, shakes or loops forever on its own.
- **Durations:** 150 to 300 ms for feedback, 300 to 500 ms for a change of layout, 500 to 800 ms for the one authored moment. A packet crossing the picture takes 1.5 to 2.5 s so it can be followed.
- **Order of reading:** inputs, then the method, then the result. Parts that explain nothing (a retry path, a legend of context) appear with their neighbours or stay still.
- **Loop without a jump:** hold on the finished picture for 2 s, fade the story out over 0.5 s, then restart from the empty or "before" state. `check-motion.mjs` fails a loop whose boundary is not empty.
- **One mover at a time on the eye:** while a packet moves, nothing else draws.
- Never animate for decoration: no idle pulsing, no ambient drift, no looping shimmer.

## Before and after

Show the old way first (`"ghost": true` elements are visible only in the before state), hold for 2 s, `hide` what goes, `reveal` and `draw` what replaces it, and `pulse` the new part. The end state is the new picture, which is also the static one.

## Anything the vocabulary does not cover

A sequence diagram or a chart comparison is hand-authored: still a pure function of time (no wall clock, no random, no CSS animation), still budgeted, still ending on the complete static picture. Add the new step kind to the player rather than bolting on a second mechanism, and add a seeded defect for it to `selftest-motion.mjs`.
