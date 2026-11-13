---
type: regex
target:
  source: file
  path: "tests/test_gateway_contract.py"
pattern: "skipif|skip\\(|importorskip|environ|getenv"
weight: 1
---

The real-service leg is conditional on credentials from the environment, so the suite needs no secrets
