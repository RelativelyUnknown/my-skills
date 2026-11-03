# Complexity tools are advice

Output from `xenon`, `radon cc` or a complexity lint rule points at code that may be hard to follow. Read it, then decide.

- Simplify when you can say what is hard to follow and a clearer shape exists (early returns, a lookup table, a function that hides real logic).
- Do not contort logic, or split a function into fragments with vague names, to reach an A. A flat run of cases or a parser table that ranks C and reads straight through stays as it is; say so in the report.
- The rank is never a reason to add `# noqa`, to raise a threshold, or to make a test pass differently. If the project's CI gates on it and the gate fails, report the failure and the readable options instead of gaming it.
