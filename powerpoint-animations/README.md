# powerpoint-animations

Three agent skills for making clean, looping explainer animations and putting them into PowerPoint. They follow the open [Agent Skills](https://agentskills.io/specification) format: copy the folders from `skills/` into `.claude/skills/` (Claude Code, Copilot) or `~/.claude/skills/`.

| Skill | Loads when you... |
| --- | --- |
| `powerpoint-animation-style` | decide what an animation should look like: colour roles, layout, motion vocabulary, timing |
| `building-animation-scenes` | write a scene and render it to frames and MP4/WebM/GIF (includes the engine and a worked example) |
| `exporting-animations-to-powerpoint` | encode, check and embed the result in a `.pptx` |

Pipeline: `specs.js` data → `scenes/<name>.js` (pure function of time) → `render.js` (Chromium, 2× PNG frames) → `encode.sh` (MP4, WebM, GIF) → `embed_in_pptx.py` (slides).

Requirements: Node 20+, Playwright with Chromium, ffmpeg, Python 3.10+ with `python-pptx` and Pillow (for the contact sheet and embedding).

Try it: copy `skills/building-animation-scenes/assets` to a work folder and run `bash skills/building-animation-scenes/scripts/build.sh <work>/assets <work>/out example`.
