# Diátaxis: choosing and shaping a page

Diátaxis (diataxis.fr, Daniele Procida) sorts documentation by what the reader is doing. Two questions place any page: is the reader acting or thinking, and are they learning or working?

- **Learning** (study): acting: Tutorial; thinking: Explanation
- **Working** (applying skill): acting: How-to guide; thinking: Reference

NumPy, Gunicorn and Canonical's documentation are organized this way, and Django's docs use the same split. Most bad pages mix two quadrants: a tutorial that stops to list every option, a reference page full of advice.

## Contents

- Tutorial
- How-to guide
- Reference
- Explanation
- Placing pages that do not fit
- Splitting a mixed page

## Tutorial

A lesson. The author is responsible for the reader's success.

- One path, no choices. Pick the options for the reader; mention alternatives only by linking elsewhere.
- Every step produces a visible result early and often ("You should now see ...").
- Concrete, not abstract: a small real project, real data, real commands.
- Minimal explanation; link to explanation pages instead.
- It must work for a beginner on a clean machine. Test it end to end on each release.

Template:

```markdown
# Build your first <thing>

In this tutorial you build <result>. It takes about <N> minutes.

## Before you start
- <exact requirement, with version>

## Create the project
1. Run ...
   You should see ...

## <Next step>
...

## Next steps
- [How to <common next goal>](#next-goal)
```

## How-to guide

A recipe for a reader who already knows what they want.

- Title states the goal: "How to rotate credentials", "Deploy to production".
- Start from a stated precondition, not from zero. Skip teaching.
- Steps in order; branch only where real situations differ ("If you use serverless, ...").
- Leave out everything not needed for the goal, including full option lists; link to reference.
- End when the goal is reached.

## Reference

A map of the machinery, consulted, not read.

- Structure mirrors the code: one page or section per module, class, command or config file, in a consistent order.
- Each entry: signature or syntax, one-line description, parameters with types and defaults, return value, errors, a short example.
- Complete and accurate beats readable. Generate from the source where possible (autodoc, mkdocstrings, `--help` output) so it cannot drift.
- Neutral tone: describe, do not instruct or persuade.

## Explanation

Discussion that builds understanding.

- Answers "why" and "how does it work": design decisions, architecture, trade-offs, history where it explains the present, comparisons with alternatives.
- Can hold opinions and context; is read away from the keyboard.
- Titles are topics: "Consistency model", "Why the scheduler is single-threaded".

## Placing pages that do not fit

- README: A landing page: one paragraph of explanation, the install command, one how-to-sized example, links to the rest
- Quickstart: A short tutorial
- FAQ: Usually how-to or explanation entries; move each answer to its proper page and link from the FAQ
- Troubleshooting: How-to guides keyed by symptom: the exact error, the cause, the fix
- Changelog, release notes: Reference (a record), written for users
- API docstrings: Reference
- Architecture or design doc: Explanation

## Splitting a mixed page

1. Mark each paragraph T, H, R or E.
2. Move R material into tables or reference sections; move E material into an explanation page.
3. Keep the page's main type; replace removed material with one-line links.
4. Check the title still matches the type (goal for how-to, topic for explanation, object name for reference).
