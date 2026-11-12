# Layout, modes and states

## Mode follows the visitor's job

| Mode | Visitor | Layout | Motion |
| --- | --- | --- | --- |
| **Persuade** (landing page, project site) | decides in seconds | one message per screen, one primary action, strong hierarchy, real content over decoration | one authored entrance at most |
| **Operate** (dashboard, admin, internal tool) | does the same task all day | consistent placement, density that scans, tables for tabular data, keyboard for everything, nothing that makes them wait | feedback only: 150 to 300 ms, no page-load choreography |
| **Read** (docs, reference) | looks something up | a 60 to 70 character column, a sidebar that shows where they are, search, anchors, code blocks that copy | none |

A page has one mode. A project site that is both a pitch and a reference is two pages.

## Layout

- Design at 390 px and at 1280 px; the page never scrolls sideways (the checker fails it). Let content decide breakpoints.
- Equal left and right edges. One column of text, one grid for cards, no third.
- Tabular data is a table: sticky header, right-aligned numbers, row hover, sortable only if sorting is real. A grid of identical cards is for items that are really peers (and never cards inside cards).
- Hierarchy by size and weight first, then space, then colour. Squint: the one thing that matters should still show.
- Real content. A screen with `Lorem ipsum`, round-number metrics or made-up customer logos is not finished; use the project's own data or say it is a placeholder.

## States: every interactive thing, designed

default, hover, focus (keyboard), active (pressed), disabled, loading, empty, error, success. If one is missing the screen is unfinished.

- **Empty:** says what belongs here and what to do next, with the action.
- **Error:** names the problem and the way out (`The file is over 5 MB. Choose a smaller one.`), next to the thing that failed, never only in colour.
- **Loading:** show the shape of what is coming; keep the control's size; a spinner that runs forever is an error state in disguise.
- **Forms:** a visible label above every field (a placeholder is not a label), help text before the mistake, validation after the field is left, keep what the user typed when something fails.
- **Controls name their action** (`Place order`, not `Submit`). A modal only for what needs interruption or protected focus.

## Motion

Motion shows state, relationship or continuity; it does not decorate. 150 to 300 ms for feedback, ease-out. Under `prefers-reduced-motion` nothing loops (the checker fails an infinite animation that still runs).
