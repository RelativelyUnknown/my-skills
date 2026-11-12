---
type: llm
focus:
  source: file
  path: "src/grid.cpp"
weight: 3
---

PASS if the binding of `Grid::cell` no longer lets Python take ownership of a pointer into the vector, and keeps the Grid alive while a returned Cell is in use: it states `nb::rv_policy::reference_internal`, or `reference` together with `nb::keep_alive<0, 1>()`, or it returns a `Cell` by value or with `rv_policy::copy` and the change is consistent. FAIL if the binding still uses the default policy with a raw pointer, uses `take_ownership`, or uses a plain `rv_policy::reference` with nothing keeping the Grid alive.
