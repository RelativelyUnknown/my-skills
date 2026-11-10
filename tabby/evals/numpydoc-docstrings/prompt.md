---
tags: [documentation]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add docstrings to the public functions in stats.py. Our pyproject has `[tool.ruff.lint.pydocstyle] convention = "numpy"`.

```python
# stats.py
def zscore(values: list[float]) -> list[float]:
    m = sum(values) / len(values)
    sd = (sum((v - m) ** 2 for v in values) / len(values)) ** 0.5
    if sd == 0:
        raise ValueError('values have zero variance')
    return [(v - m) / sd for v in values]
```
