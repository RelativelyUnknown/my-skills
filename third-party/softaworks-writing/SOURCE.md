# Source of this copy

- Upstream: https://github.com/softaworks/agent-toolkit
- Path: `skills/writing-clearly-and-concisely/`
- Commit: `3027f20f3181758385a1bb8c022d4041dfb4de84` (5 March 2026, as shown on the GitHub commits page)
- Licence: MIT, Copyright (c) 2026 Leonardo Flores (repository LICENSE; the skill's own files state no licence). The upstream `LICENSE` is kept next to this file; it applies to these copies, not to the rest of this repository.
- Vendored: 6 November 2026, **unmodified**. Files were downloaded as raw bytes from `raw.githubusercontent.com` at that commit.
- Not included: everything else in the toolkit.

## Review before vendoring

The bytes were scanned for invalid UTF-8, invisible and bidirectional characters, HTML comments and tags, long encoded blobs, phrases aimed at an AI agent (ignore previous instructions, run, upload and similar) and install or shell commands, and the frontmatter was checked for permission fields. Nothing was found that tells an agent to do anything outside the task.

- Attribution from the skill's README: original skill by @joshuadavidthomas (joshuadavidthomas/agent-skills, MIT); adapted from obra/the-elements-of-style; writing principles from *The Elements of Style* by William Strunk Jr. (1918); AI-pattern research from Wikipedia's field guide to AI-generated content.
- `signs-of-ai-writing.md` is about 94 KB (roughly 25k tokens): load it only when needed.
- `signs-of-ai-writing.md` contains two zero-width spaces (U+200B) at line 165, inside a quoted example of AI-written text, and `<!-- -->` comment markers inside quoted Wikipedia examples. They are upstream content and were left as they are.
- Frontmatter uses only `name` and `description`.

## Files (sha256)

| sha256 | path |
| --- | --- |
| `4b4447da5344f8b2d3a8a19ba8366d1ac7a24d9ab4690bd04576dc772ddf8321` | `LICENSE` |
| `cd8241146abf3e7514fdb07a6db2e06c8535a4f78dd1ab471901b2e7fe4db089` | `skills/writing-clearly-and-concisely/README.md` |
| `c5f4ecc8bfa7984d0df70d30cea3bfeb824f7b24d31db111d5a1a9a959880575` | `skills/writing-clearly-and-concisely/SKILL.md` |
| `248b18596fa18cf63605182688565d25d115c859f602068185f6014c26addbfe` | `skills/writing-clearly-and-concisely/elements-of-style/01-introductory.md` |
| `8cead3fc56b54ab5fc22e52c14423182fdce2d9535d4c1dda1f8319cac542027` | `skills/writing-clearly-and-concisely/elements-of-style/02-elementary-rules-of-usage.md` |
| `3867f33512ff2f0e965386dbb558579aab43ca10f070bd48d732584b9b5119e0` | `skills/writing-clearly-and-concisely/elements-of-style/03-elementary-principles-of-composition.md` |
| `150feae0c201def056a96dd25fa5d23e015f53632b21f3bcd7b7266f8197c563` | `skills/writing-clearly-and-concisely/elements-of-style/04-a-few-matters-of-form.md` |
| `60db286f5166b1b6f4d85a0cc39471b375fbd62d6057d3844533551fb09f2c2d` | `skills/writing-clearly-and-concisely/elements-of-style/05-words-and-expressions-commonly-misused.md` |
| `06d135c200e1bbfdbe90f433dfbdffeb9c4ea07f028a9a880f4026622e5c10fd` | `skills/writing-clearly-and-concisely/signs-of-ai-writing.md` |

## Updating

Download the files again at a newer commit, repeat the review, replace the files, and update the commit, date and hashes here.
