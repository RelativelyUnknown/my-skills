---
type: regex
target:
  source: file
  path: "pyproject.toml"
pattern: "dependencies\\s*=\\s*\\[[^\\]]*(?:dateparser|dateutil|parsedatetime|pendulum|arrow)"
flags: i
weight: 3
---

The library is declared as a dependency
