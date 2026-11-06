# Redesign exception

Only when the task explicitly asks for a redesign: change the design first, run the tests, then classify each failure. Asserts the old internal shape: rewrite it. Asserts behavior the spec requires: fix the code. Asserts something the spec never required: ask, or remove it and say why. No skips may remain; the end state is green; report every test changed or removed.
