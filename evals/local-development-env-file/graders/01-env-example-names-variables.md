---
type: regex
target:
  source: file
  path: ".env.example"
pattern: "APP_DATABASE_URL[\\s\\S]*APP_API_KEY"
weight: 3
---

.env.example lists the variables
