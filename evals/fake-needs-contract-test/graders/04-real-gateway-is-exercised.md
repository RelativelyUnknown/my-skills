---
type: regex
target:
  source: file
  path: "tests/test_gateway_contract.py"
pattern: "(?<!Fake)PaymentGateway\\("
weight: 1
---

The contract test constructs the real PaymentGateway (against a sandbox or a local server), so the fake is compared with it
