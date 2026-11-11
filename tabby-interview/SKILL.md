---
name: tabby-interview
description: "Interview the user about a project and save the answers as a ## Tabby section in AGENTS.md. Runs only when asked: /tabby:interview, 'run the Tabby interview', 'set up Tabby'."
disable-model-invocation: true
license: MIT
---

# The Tabby interview

Read `references/start.md` in this skill's folder and follow it: research the code read-only (`references/research.md`), ask the first round (at most three questions, each with a recommended answer and the evidence behind it), and stop. Restate the answers when the user has replied, wait for a clear yes, then write the `## Tabby` section to AGENTS.md. Write no source code.

Tool defaults: `development/which-type.md` and the leaves it names are in the `tabby` skill's folder, `../tabby/` from here.
