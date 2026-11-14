---
tags: [development]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

The order tests use a bare Mock for the payment gateway and say nothing true about it. Add an in-memory `FakePaymentGateway` in `tests/fakes.py`, use it in `tests/test_orders.py`, and put whatever checks the fake needs in `tests/test_gateway_contract.py`. Run the tests.
