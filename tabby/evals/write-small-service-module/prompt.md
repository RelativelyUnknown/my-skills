---
tags: [development]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Create `src/orders/service.py` with these functions, keeping it small:
- `load_orders(path)`: read a CSV file of orders (columns id, customer, amount, created) and give the rows back to the caller one at a time.
- `fetch_rates(url)`: GET a JSON object of exchange rates from a URL and return it.
- `total_in(orders, currency, rates)`: sum the order amounts converted into `currency` using `rates`.
- `stamp(order)`: return the order with a `processed_at` timestamp added.
- `describe(order, max_len)`: return a one-line description of the order, shortened to `max_len` (default 60).
Use only the standard library.
