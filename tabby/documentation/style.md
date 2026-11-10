# Style guide

Defaults distilled from the Google developer documentation style guide, the Microsoft Writing Style Guide, the Python devguide documentation style guide and Write the Docs. A project's own style guide wins over this file.

## Words to replace

| Instead of | Write |
| --- | --- |
| utilize, leverage, make use of | use |
| in order to | to |
| is able to, has the ability to | can |
| due to the fact that | because |
| prior to, subsequent to | before, after |
| in the event that | if |
| a number of | some, or the number |
| e.g., i.e., etc., via, vs. | for example, that is, and so on, through/by, versus |
| please (in instructions) | (delete) |
| simply, just, easily, obviously, of course | (delete) |
| we (meaning the product or the authors) | the name of the product, or rephrase |
| will (for behavior) | present tense |
| click on | click, or select |
| whitelist, blacklist, master/slave | allowlist, denylist, primary/replica |
| sanity check, dummy value | quick check, placeholder |

## Grammar and voice

- Second person; present tense; active voice. Passive is fine when the actor is unknown or irrelevant ("The file is deleted after 30 days").
- Imperative mood for instructions; indicative for descriptions.
- Contractions: fine in conversational docs, avoided in formal reference; one choice per docs set.
- American spelling unless the project uses another. Serial (Oxford) comma.

## Headings and titles

- Sentence case: capitalize the first word and proper nouns only.
- Task pages and sections: bare imperative verb ("Install the CLI"); conceptual pages: noun phrase ("Authentication model"); reference: the object's name.
- No punctuation at the end, no code-only headings where a phrase works, no emoji, no "Introduction" as the only first heading.
- Do not skip levels; one H1 per page.

## Lists and procedures

- Numbered list for steps that happen in order; bullets otherwise.
- One action per step. Start the step with the verb, or with the condition or location if there is one ("In `config.toml`, set ...").
- State the result after the step when the reader must check it before going on.
- Introduce a list with a complete sentence or a fragment ending in a colon; keep items parallel.
- A procedure has at most about ten steps; split longer ones into sub-procedures with their own headings.

## Punctuation and capitalization

- No exclamation marks. Em dashes sparingly; prefer commas, colons or separate sentences.
- Capitalize product and feature names exactly as their owners do (Python, PyPI, GitHub, macOS). Generic terms stay lowercase (the command line, the server).
- Write "Python", "Unicode", "POSIX" capitalized; "reST" with a lowercase r; "free-threaded" rather than "no-GIL" (Python devguide).

## Numbers, dates and units

- Numerals for 10 and up and any measurement; spell out one to nine in prose. Units with a space: `500 ms`, `16 GB`.
- Unambiguous dates: `2026-11-03` in technical text, "November 3, 2026" in prose; never `11/03/26`. Time zones explicit (UTC).

## Code, UI and file names

- Code font: code, commands, flags, parameters, return values, environment variables, file and directory names, literal values (`true`, `None`, `"utf-8"`).
- Bold: UI elements the reader clicks or reads (**Save**, **Settings**). Do not put UI names in quotes.
- Placeholders in angle brackets and uppercase or descriptive (`<PROJECT_ID>`), defined right after the example.
- No code font for emphasis or as a verb; write "push the branch with `git push`".

## Notes and warnings

- Use admonitions rarely; when everything is a note, nothing is.
- Note: helpful but skippable. Important: needed for success. Warning or caution: risk of data loss, security exposure or a crash; say what happens and how to avoid it.
- Never put essential steps only inside a note.

## Accessibility and inclusive language

- Alt text says what an image shows and why it matters; decorative images get empty alt text.
- Do not rely on color, position ("the button on the right") or direction ("above") alone.
- Avoid ableist and violent metaphors where a plain word exists; keep real API terms (`kill -9`). Use "they" for an unspecified person.
