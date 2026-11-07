# Composition: tightening sentences

The composition principles of Strunk's *The Elements of Style* (1918, public domain), the core of softaworks' *writing-clearly-and-concisely*, applied to technical writing. Use this file for an editing pass.

## Contents

- The rules that matter most
- Paragraphs
- Sentences
- Words
- An editing pass

## The rules that matter most

| Rule | In docs |
| --- | --- |
| Use the active voice | "The scheduler retries the task", not "The task is retried by the scheduler" |
| Put statements in positive form | "Returns a copy", not "Does not modify the original" |
| Use definite, specific, concrete language | "Times out after 30 s", not "may take a while" |
| Omit needless words | "To", not "in order to"; "because", not "due to the fact that" |
| Keep related words together | Put the condition next to the action it limits |
| Place emphatic words at the end | "If the table exists, the write fails" ends on the outcome |
| Express coordinate ideas in similar form | List items and table cells share a grammatical shape |
| One paragraph per topic | A new idea starts a new paragraph |
| Begin with a topic sentence | The first sentence states the paragraph's point |
| Keep to one tense | Present tense for behavior throughout |

## Paragraphs

- Three to five sentences is plenty in docs; one-sentence paragraphs are fine for emphasis.
- The topic sentence carries the point; the rest supports or qualifies it. A reader skimming first sentences should get the page.
- Cut the closing sentence that restates the paragraph.

## Sentences

- One idea per sentence. Split at "and", "which" and semicolons when each half stands alone.
- Subject and verb early and close together; do not open with a long subordinate clause unless it is the condition for an instruction.
- Avoid a succession of loose sentences joined by "and", "but", "so". Vary structure by meaning, not for decoration.
- Do not break a sentence in two with a full stop before a dependent clause ("Because the cache is per process.").
- An opening participial phrase must refer to the subject: "Using `--force`, the command overwrites the file", not "Using `--force`, the file is overwritten".

## Words

- Prefer the short, common word: use, start, end, help, show, need, about.
<!-- lint-prose: off -->
- Cut intensifiers and qualifiers: very, really, quite, rather, somewhat, fairly, basically, actually.
- Replace phrases with words: "the question as to whether" becomes "whether"; "there is no doubt but that" becomes "doubtless", or cut it; "he is a man who" becomes "he".
<!-- lint-prose: on -->
- Turn hidden verbs back into verbs: "perform an installation of" becomes "install"; "make a decision" becomes "decide"; "provide support for" becomes "support".
- Commonly misused words in technical text:
  - "comprise": the whole comprises the parts.
  - "data": singular or plural; pick one per docs set.
  - "fewer" for countable things, "less" for amounts.
  - "that" for restrictive clauses, ", which" for the rest.
  - "affect" (verb) and "effect" (noun); "ensure" (make certain) and "insure" (against loss); "its" and "it's".

## An editing pass

1. Read only the headings and first sentences. Do they tell the story? Fix the outline before the prose.
2. For each paragraph: delete the sentence that adds least. Repeat until deleting hurts.
3. For each sentence: find the actor and the action; make the actor the subject and the action the verb.
4. For each word: replace long words with short ones, and delete the ones that carry nothing.
5. Read it aloud, or run `scripts/lint_prose.py`, and fix what trips you.
