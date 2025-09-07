# SOC Walkthrough

This walkthrough shows the expected analyst workflow. It is intentionally
written as an investigation process rather than an automatic-response script.

## 1. Receive and acknowledge an alert

Run one scenario and record the alert ID, rule ID, severity, confidence, event
window, affected asset, and assigned analyst in a case record.

~~~text
make lab-1
~~~

An alert is an investigative lead. Do not describe an alert as a confirmed
breach until the evidence supports that conclusion.

## 2. Preserve the initial evidence

Record the alert output and all referenced event IDs. Preserve a bounded
pre-alert and post-alert time window. Record where the evidence came from and
the time it was collected.

## 3. Triage against the linked playbook

Use the detection rule and the scenario-specific playbook together:

| Scenario | Triage focus | Escalation point |
| --- | --- | --- |
| SC-001 | Role, schedule, source, approval, exports, and service impact | Suspected unauthorized sensitive-data access or export |
| SC-002 | Authentication pattern, MFA, device, session, privileges, and later activity | Reasonable evidence of account compromise |
| SC-003 | Audit event, runtime evidence, image, RBAC, egress, and service impact | Correlated production workload compromise |

## 4. Decide containment

Containment needs a named owner and rationale. Do not disable a business-user
account or business-critical service without considering safe service
continuity. The incident commander and business operations decide how to reduce
risk while maintaining an approved operating path.

## 5. Investigate, remediate, and recover

Scope related identities, services, credentials, changes, and data exposure.
Hand technical remediation to the responsible identity, application, or
platform owner. Confirm recovery using appropriate health checks, rescan or
retest results, and heightened monitoring.

For the Kubernetes lab, use immutable remediation: update the source or base
image, rebuild, scan, approve, and redeploy. Do not patch a running container
in place.

## 6. Assess privacy and notifications

Route a concise factual package to the privacy/compliance owner and legal
counsel. They assess whether a notification is needed. Record the decision,
approver, timing, and required follow-up in the case.

## 7. Close and improve

Close only after evidence, containment, remediation, recovery, ownership, and
follow-up actions are documented. Hold a blameless retrospective and tune the
detection if the scenario exposed an avoidable false positive, blind spot, or
slow escalation path.
