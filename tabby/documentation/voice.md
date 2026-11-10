# Voice and structure

The reader is mid-task and reads in order, looking for the next thing to do. Ask of each sentence: what does this let them do or understand, and is it the first thing they need? Put the point first, keep sentences single-purpose, and cut anything that announces instead of informing.

- Address the reader as "you". Present tense ("returns", not "will return"). Active voice; name who acts. Imperative for instructions ("Run", "Set").
- Lead with the point. A page's first sentence says what it is for; a section's first sentence answers its heading. No introductions that announce what follows.
- Sentence-case headings that name the task or topic: "Configure retries", not "Retries Configuration Options". Task headings start with a verb.
- Put the condition before the instruction: "To export a table, run ...". Put the goal before the location: "To change the schema, edit `config.toml`".
- Numbered lists for sequences, one action per step, with the expected result when the reader needs to check it. Bullets for unordered items. List items share a grammatical form.
- One idea per sentence; aim for under 25 words. Short paragraphs. Tables for options and comparisons with more than two attributes.
- Link text names its destination ("see [Authentication](#authentication)"); never "click here", "this" or a bare URL in prose.
- Code font for code, commands, file names, paths, parameters and literal values. Bold only for UI labels. Italics for a term at its definition, if at all.
- Use one term per concept, defined once, matching the API and UI exactly. Do not vary terms for style.

## Content rules

- **Be specific.** Numbers, versions, units, exact error messages, defaults. "Retries 3 times with exponential backoff starting at 1 s" beats "retries automatically".
- **Timeless.** No "currently", "now", "new", "recently", "soon", or promises about future features. History belongs in the changelog; plans belong in the issue tracker.
- **No minimizers, puffery or filler** ("simply", "just", "easy", "powerful", "seamless", "blazing fast", "in order to", "note that"). A speed claim comes with a benchmark or is cut.
- **Affirmative and calm.** Say what works and how to do it. Reserve warnings for data loss, security and crashes, and state the consequence: "Deletes the table and its history; this cannot be undone." Collect security considerations in their own section and link to it.
- **Global readers.** No idioms, jokes or Latin abbreviations (write "for example", "that is"). Expand an acronym on first use unless it is better known than its expansion (HTML, URL, API).
- **Inclusive and accessible.** "allowlist/denylist", "primary/replica"; "they" for an unknown person. Alt text that states what an image shows; never rely on color alone.
- **Honest scope.** State requirements, supported versions and known limitations where readers will look for them. Do not hide a limitation in a footnote.
