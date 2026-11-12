# Security audit: reporting

Three buckets, in this order, each finding under one root cause:

- **Confirmed**: you traced untrusted input to a sink with no effective control and can say what an attacker gets. Only these carry a severity.
- **Needs validation**: it depends on something you cannot see (deployment, a framework version, a runtime value). State the question and who can answer it. No severity.
- **Rejected**: looked suspicious, disproved. One line each with the control that stops it, so it is not raised again.

For each confirmed finding: `file:line`, the **entry point** (who sends what), the **payload**, how it **executes** or reaches the sink, **what the attacker gets**, severity, the smallest fix at the last point where the data is trusted, and a **regression test** that fails before the fix, passes after it, and fails again when you revert the fix (a quick way to know the test tests the fix). Run the failing test against the old code and read its output: it must fail on your assertion, not on an import error. Do not adjust the reproduction until it agrees with the claim. If you cannot write all four of entry point, payload, mechanism and effect, it is `needs validation`. The fix has to enforce in code (a scoped query, a check that raises); a comment saying the caller must check is not a fix.

Rate **severity** (the damage if it is real) and **likelihood** (how easily it triggers in supported use: low for an unusual configuration, high for routine operation) separately, each with a reason; neither makes a finding valid. Severity follows the damage you can state: high when an outside party defeats an explicit control with real consequences (data read or changed, code run, other tenants' data), medium when a control is weakened but the damage is limited, low for hardening. If you cannot state concrete damage, rate lower. The overall severity never exceeds the worst confirmed finding.

**Rating a severity.** List the facts first (what is vulnerable, how the attacker reaches it, which privileges they need, what they get, whether a user must act), then judge each impact on its own: code execution gives control of code and data, not automatically a leak of every record or an outage. Take the reasonable worst case, not the absolute one; where a fact is missing, choose the most defensible value and mark it assumed. A dependency or database that exists only to serve the application is part of the same system, so do not count its data twice as "downstream" harm; harm to a separate system (a visitor's browser, other tenants) is a separate line. Do not compute a numeric score by hand: CVSS 4.0 uses lookup tables, so give the vector and let the calculator produce the number, and only when the reader asks for it. A weakness with no exploitable effect (style, design preference) gets no vector.

**Coverage.** End with what you checked and what you did not (a result that only read the code says so; it is not the same as one that ran the behaviour), so a clean result can be trusted: the files read in full, the classes walked (each clean, not applicable, finding or unverified), the endpoints or flows not reviewed, and anything that needed a deployment fact you could not see. For an access-control review add one line on how this project enforces authorization.

Do not pad: a missing header or rate limit with no victim is a note at the end, not a finding. A clean audit says what was checked and found nothing.

## An independent check before you report

Disproving your own candidate in the context that produced it is weak. When you can run a subagent, give each confirmed candidate to a fresh one with only the candidate (trace, files, claimed effect) and this prompt, then keep what survives:

> You did not write this finding. Try to refute it from the source. Check every file and line in the trace, find the strongest control on the path (validation, authorization, framework behaviour, a constant argument) and say whether it stops the claimed effect. Reply `holds` with the reason, `refuted` with the control that stops it, or `needs validation` with the one fact you cannot see.

The verifier reads and runs nothing that touches the network or writes outside a scratch directory. Without subagents, do the same pass yourself starting from the sink and walking back, and say that you did.
