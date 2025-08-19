# PB-001: Bulk Sensitive-Record Access

| Field | Value |
| --- | --- |
| Version | 1.0 |
| Owner role | SOC manager and application-security owner |
| Review cycle | Every six months and after an access-control incident |
| Linked detection | SOC-001 |
| Linked scenario | SC-001 |
| Default severity | High |
| Last exercise | Record after first completed lab exercise |

## Purpose

Investigate unusually high-volume or suspicious access to sensitive-record
references while preserving evidence, minimizing privacy exposure, and
protecting service continuity.

Use [PB-000](PB-000-incident-management-standard.md) for common incident
requirements. This playbook adds access-specific triage and containment steps.

## Trigger and scope

Start this playbook when SOC-001 fires or when a trusted source reports
possible inappropriate sensitive-record access or export.

Raise priority to critical when evidence indicates an unauthorized export,
confirmed external transfer, active misuse of a privileged account, or material
ongoing access to sensitive data.

## Required initial evidence

Collect only the minimum data needed for investigation:

- alert ID, rule ID, timestamps, and evidence event IDs;
- actor ID, role, session or device reference, and source context;
- affected application, environment, and data classification;
- access count, synthetic record references, and time window;
- approval, operating schedule, authorized-record scope, reporting, migration,
  or support context;
- export activity, destination context, and related authentication events;
- relevant role, entitlement, and emergency-access history.

Do not include business notes, raw sensitive content, credentials, or unrelated
employee information in the incident case.

## Stage 1: acknowledge and triage

1. Create a case using the [incident-case template](templates/incident-case-template.md).
2. Preserve the alert and a bounded window before and after the alert.
3. Validate the source application, actor, asset, timestamp, and event quality.
4. Check whether the actor had an approved business, operational, migration,
   reporting, emergency-access, or support reason.
5. Compare the access pattern with the actor’s role, shift, source, device, and
   expected workflow.
6. Check for sensitive-record export, external egress, privilege changes, new
   session, or anomalous identity events.
7. Classify the event as benign, suspicious, or confirmed incident and record
   the rationale.

| Decision point | Action |
| --- | --- |
| Approved activity with adequate evidence | Document rationale, tune the rule if needed, and close through normal review. |
| Context unavailable or pattern unexplained | Keep the case high severity, escalate to SOC L2, and begin scoped investigation. |
| Unauthorized access or export is plausible | Escalate to the incident commander and begin approved containment. |
| Ongoing unauthorized access is confirmed | Treat as critical and apply the fastest safe containment approved by incident command. |

Exit criterion: the incident commander has a documented scope hypothesis and
containment decision.

## Stage 2: contain

Choose the least disruptive option that stops the suspected unauthorized path.
Potential actions, subject to approval, include:

1. Revoke an active application session or token.
2. Block a confirmed unauthorized source through the approved network process.
3. Restrict export capability while preserving an approved business-service route.
4. Apply a temporary least-privilege access change.
5. Disable the account only after the incident commander and business
   operations confirm a safe alternative workflow, except where emergency
   policy authorizes immediate action.

Record the action, owner, approver, time, expected impact, actual outcome, and
residual risk.

Exit criterion: the suspected access path is interrupted or a documented
compensating control is active.

## Stage 3: investigate

1. Build a timeline of authentication, access, export, API, and network events.
2. Determine which synthetic records, functions, or integrations were in scope.
3. Review role assignments, privileged access, emergency-access approvals, and
   recent identity changes.
4. Review source IP, device, session, and location context according to the
   organization’s authorized data sources.
5. Identify whether the activity resulted from user error, an access-control
   design flaw, account compromise, a process gap, or a system defect.
6. Record confirmed facts separately from assumptions.

Exit criterion: the case documents affected scope, likely root cause, and
whether unauthorized acquisition or disclosure is evidenced.

## Stage 4: eradicate and remediate

Assign owned remediation actions. Depending on the root cause, these can
include:

- reset credentials and re-establish MFA;
- remove stale roles or privileged access;
- correct authorization checks or export controls;
- require stronger approval for high-volume exports;
- update monitoring and retention controls;
- improve training or workflow documentation;
- create a risk-treatment item for a control gap that cannot be fixed promptly.

Link each action to a change or work-item reference and define a verification
method.

Exit criterion: the cause is removed or formally accepted with a compensating
control and due date.

## Stage 5: recover and validate

1. Restore only the access needed for the approved business or operational
   workflow.
2. Confirm normal service, audit logging, and least-privilege authorization.
3. Monitor the identity, source, and export signals for a period set by the
   incident commander.
4. Confirm that the alert condition no longer occurs without approved context.
5. Obtain service-owner and business-operations sign-off where a critical
   business workflow was affected.

Exit criterion: normal use is restored safely and recurrence monitoring is
complete.

## Stage 6: privacy and communications assessment

Send the incident facts and preserved evidence to the privacy/compliance owner
and legal counsel. They determine whether the event requires any internal,
contractual, regulatory, or data-subject communication.

Record the decision owner, assessment time, facts supplied, decision, and any
follow-up package. The SOC does not make a legal notification decision from
the detection alone.

## Stage 7: close and improve

Before closure:

1. Complete the case template and evidence log.
2. Verify all remediation and recovery actions.
3. Record any unresolved risk with an owner and due date.
4. Complete the post-incident review for confirmed incidents or material
   near-misses.
5. Review SOC-001 for threshold, role-baseline, allowlist-expiry, and
   false-positive improvements.
6. Obtain closure approval from the incident commander.

## Exercise outcome for SC-001

The expected lab outcome is a high-severity investigation, not an automatic
claim of breach. The analyst should show that the event is external-context
bulk access, preserve the six alerting event IDs, propose a safe containment
decision, and identify the evidence needed for a privacy assessment.
