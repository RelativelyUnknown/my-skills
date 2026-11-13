---
type: regex
target:
  source: file
  path: "tests/test_gateway_contract.py"
pattern: "FakePaymentGateway[\\s\\S]*PaymentGateway|PaymentGateway[\\s\\S]*FakePaymentGateway"
weight: 1
---

The contract test file refers to both the fake and the real gateway
