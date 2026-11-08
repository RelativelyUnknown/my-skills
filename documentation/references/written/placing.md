# Placing and splitting pages

Diátaxis (diataxis.fr, Daniele Procida) sorts documentation by what the reader is doing. Two questions place any page: is the reader acting or thinking, and are they learning or working?

| | Acting | Thinking |
| --- | --- | --- |
| **Learning** (study) | Tutorial | Explanation |
| **Working** (applying skill) | How-to guide | Reference |

Most bad pages mix two quadrants: a tutorial that stops to list every option, a reference page full of advice.

## Placing pages that do not fit

| Page | Treat as |
| --- | --- |
| README | A landing page: one paragraph of explanation, the install command, one how-to-sized example, links to the rest |
| Quickstart | A short tutorial |
| FAQ | Usually how-to or explanation entries; move each answer to its proper page and link from the FAQ |
| Troubleshooting | How-to guides keyed by symptom: the exact error, the cause, the fix |
| Changelog, release notes | Reference (a record), written for users |
| API docstrings | Reference |
| Architecture or design doc | Explanation |

## Splitting a mixed page

1. Mark each paragraph T, H, R or E.
2. Move R material into tables or reference sections; move E material into an explanation page.
3. Keep the page's main type; replace removed material with one-line links.
4. Check the title still matches the type (goal for how-to, topic for explanation, object name for reference).
