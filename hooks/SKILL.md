---
name: hooks
description: "Use only when the user asks for it: /tabby:hooks, 'turn Tabby hooks on or off'. Installs or removes an optional reminder hook so Claude loads the right Tabby skill on every prompt. Never enable it on your own."
disable-model-invocation: true
license: MIT
---

# Tabby hooks (optional, off by default)

Claude Code decides on its own whether to load a skill, and on short prompts it often does not (measured: the right Tabby skill loaded on 46% of unseen prompts without the reminder, 95% with it; `AUDIT.md` section 8). The reminder is a `UserPromptSubmit` hook that prints about 120 words of context before each prompt. It runs no other command, reads nothing, and writes nothing.

## `/tabby:hooks on`

1. Say what will change, and show the user both pieces before writing anything:
   - the reminder text, from [remind.txt](remind.txt) (read it with the Read tool and quote it);
   - the settings entry:

```json
{"hooks": {"UserPromptSubmit": [{"hooks": [{"type": "command", "command": "cat \"$CLAUDE_PROJECT_DIR/.claude/tabby-remind.txt\""}]}]}}
```

2. Ask: this project only (`.claude/settings.json`, shared with the team when committed; the default) or all projects (`~/.claude/settings.json`, using `$HOME/.claude/tabby-remind.txt`). Wait for a clear yes.
3. On yes: copy `remind.txt` to `.claude/tabby-remind.txt` (or `~/.claude/tabby-remind.txt`) with the Write tool, then merge the entry into the settings file. Keep every other setting and every other hook; if the file has invalid JSON, stop and say so.
4. Say that the hook starts with the next prompt in a new session, and how to remove it.

## `/tabby:hooks off`

Remove only the entry whose command mentions `tabby-remind.txt`, and delete that text file. Leave other hooks alone. Report what was removed.

## `/tabby:hooks` with no word

Say whether the entry is present in the project and user settings, and what `on` and `off` do. Change nothing.
