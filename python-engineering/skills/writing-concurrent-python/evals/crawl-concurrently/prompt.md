---
tags: [writing-concurrent-python, prototype]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

`crawl(urls)` in `src/fetcher/crawl.py` fetches about 200 URLs one after another and takes minutes. Make it concurrent: at most 10 requests at once, each limited to 5 seconds, and one failing URL must not lose the results of the others. `fetch` is a blocking function you may not change.
