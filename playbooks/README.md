# Playbook Index

The documents in this directory are end-to-end incident-response playbooks.
They are written for a fictional organization and apply only to the synthetic
scenarios in this repository.

| Playbook | Trigger | Primary owner | Related scenario |
| --- | --- | --- | --- |
| [PB-000](PB-000-incident-management-standard.md) | Any SOC investigation | Incident commander | All scenarios |
| [PB-001](PB-001-sensitive-record-access.md) | SOC-001 | SOC L2 / incident commander | SC-001 |
| [PB-002](PB-002-privileged-account-authentication-anomaly.md) | SOC-002 | SOC L2 / incident commander | SC-002 |
| [PB-003](PB-003-kubernetes-production-control-break.md) | SOC-003 or SOC-004 | SOC L2 with platform owner | SC-003 |

Each scenario-specific playbook uses the shared standard in PB-000. The
playbooks require human approval for actions that could affect critical business service,
availability, or a person’s access to business systems.

## How to use a playbook

1. Create a case using the incident-case template.
2. Record the alert, evidence references, and assigned owner.
3. Perform each stage in order unless the incident commander documents a reason
   to deviate.
4. Preserve evidence before taking a disruptive containment action.
5. Record the decision owner, approval, action, outcome, and validation result.
6. Complete the post-incident review and detection-tuning section before case
   closure.

## Templates

- [Incident case template](templates/incident-case-template.md)
- [Post-incident review template](templates/post-incident-review-template.md)
- [Evidence log template](templates/evidence-log-template.csv)
