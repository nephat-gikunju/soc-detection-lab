# Evidence and Reporting Standard

## Objective

Evidence must let another analyst understand what happened, when decisions
were made, who approved them, and how recovery was verified. It should be
sufficient for operational learning without exposing unnecessary sensitive or
employee data.

## Minimum evidence fields

| Field | What to record |
| --- | --- |
| Case ID | Stable incident or investigation identifier. |
| Detection | Rule ID, alert ID, severity, confidence, and scenario. |
| Timeline | Alert time, acknowledgement, key actions, recovery, and closure. |
| Scope | Affected synthetic assets, identities, data category, and services. |
| Evidence references | Event IDs, queries, exported logs, hashes, and screenshots. |
| Decisions | Owner, approver, rationale, and business-service impact assessment. |
| Remediation | Change record, owner, implementation status, and verification result. |
| Follow-up | Detection tuning, risk acceptance, training, audit, or engineering work. |

## Evidence preservation

Preserve the original source event identifiers and export a bounded time window
before making a disruptive change. Where the operating environment supports
it, use approved immutable storage, record timestamps in UTC, and calculate
integrity hashes according to organizational policy.

Do not collect extra sensitive or employee content merely because an alert fires.
Escalate access requests through the appropriate privacy and business-governance
process.

## Privacy and notification decision gate

The privacy/compliance owner and legal counsel determine whether an event
involves unauthorized access, the level of risk, contractual obligations, and
any regulator or data-subject notification requirement. The SOC records the
facts, preserves evidence, and supports that assessment; it does not make a
legal determination by itself.

## Templates

- [Incident case template](../playbooks/templates/incident-case-template.md)
- [Post-incident review template](../playbooks/templates/post-incident-review-template.md)
- [Evidence log template](../playbooks/templates/evidence-log-template.csv)
