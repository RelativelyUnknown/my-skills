# Security audit: reporting

Three buckets, in this order, each finding under one root cause:

- **Confirmed**: you traced untrusted input to a sink with no effective control and can say what an attacker gets. Only these carry a severity.
- **Needs validation**: it depends on something you cannot see (deployment, a framework version, a runtime value). State the question and who can answer it. No severity.
- **Rejected**: looked suspicious, disproved. One line each with the control that stops it, so it is not raised again.

For each confirmed finding: `file:line`, the input and how it reaches the sink, what the attacker gets, severity, the smallest fix at the last point where the data is trusted, and a **regression test** that fails before the fix and passes after.

Severity follows the damage you can state: high when an outside party defeats an explicit control with real consequences (data read or changed, code run, other tenants' data), medium when a control is weakened but the damage is limited, low for hardening. If you cannot state concrete damage, rate lower. The overall severity never exceeds the worst confirmed finding.

Do not pad: a missing header or rate limit with no victim is a note at the end, not a finding. A clean audit says what was checked and found nothing.
