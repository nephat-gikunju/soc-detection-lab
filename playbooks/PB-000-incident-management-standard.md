# PB-000: Incident Management Standard

| Field | Value |
| --- | --- |
| Version | 1.0 |
| Owner role | SOC manager |
| Review cycle | Every six months and after a material incident |
| Applies to | All scenarios and related investigations |
| Classification | Internal security operations procedure |
| Last exercise | Not applicable; use the scenario playbooks |

## Purpose

Provide a repeatable, privacy-aware, and service-continuity-conscious process for
handling a security alert from acknowledgement through closure. This standard
defines the shared actions; scenario playbooks add technical evidence and
containment details.

## Core principles

1. An alert is not automatically a confirmed incident.
2. Preserve relevant evidence before making disruptive changes.
3. Contain malicious activity promptly while protecting service continuity and
   business operations.
4. Use the minimum data necessary for investigation.
5. Record the owner, rationale, approval, and result of every material action.
6. Escalate privacy, legal, and service-continuity decisions to the appropriate
   accountable roles.

## Roles and responsibilities

| Role | Responsibilities |
| --- | --- |
| SOC L1 analyst | Acknowledge alert, validate basic context, create case, preserve initial evidence, and escalate. |
| SOC L2 / incident commander | Classify incident, approve or coordinate containment, direct investigation, and own communication cadence. |
| Application, identity, or platform owner | Supply system context, implement remediation, and verify recovery. |
| Business operations representative | Assess business-service impact and approve alternatives when access or availability may change. |
| Privacy/compliance owner and legal counsel | Assess privacy, contractual, regulatory, and notification obligations. |
| Communications lead | Coordinates approved internal or external communications when required. |

Use roles rather than named individuals in this portfolio lab.

## Required case fields

Create a case before progressing beyond initial triage. At minimum record:

- case ID and linked alert ID;
- scenario, detection rule, severity, and confidence;
- acknowledgement time and assigned analyst;
- affected assets, identities, data category, and environment;
- evidence references and collection times;
- incident classification and business-impact assessment;
- containment decision, owner, approval, and outcome;
- remediation owner, change reference, and validation result;
- privacy-notification decision owner and status;
- closure approver, lessons learned, and follow-up actions.

Use the [incident-case template](templates/incident-case-template.md) and
[evidence log](templates/evidence-log-template.csv).

## Incident lifecycle

### 1. Acknowledge and register

1. Create the case and assign an initial owner.
2. Record alert severity, confidence, and associated playbook.
3. Check for duplicate cases, maintenance windows, or linked change records.
4. Establish the initial event window and preserve the alert output.

Exit criterion: the case has an owner, scope hypothesis, timestamps, and
evidence references.

### 2. Triage and classify

1. Validate event source, asset, actor, and timestamp quality.
2. Compare the activity with known business, operational, and maintenance
   context.
3. Determine whether the alert is benign, suspicious, or a confirmed incident.
4. Update severity using technical scope, likelihood, business impact, and
   service-continuity considerations.
5. Escalate a confirmed or likely material incident to the incident commander.

Exit criterion: the team has a documented classification and response priority.

### 3. Preserve evidence

1. Preserve the alert and relevant bounded pre-event and post-event logs.
2. Record event IDs, queries, timestamps, source systems, and collectors.
3. Obtain an approved snapshot or export before modifying a potentially
   compromised asset when feasible.
4. Store evidence in an approved location and record integrity information when
   the environment supports it.

Exit criterion: evidence needed to reproduce the timeline is retained.

### 4. Contain

1. Define the exact unauthorized path or suspected harmful activity.
2. Choose the least disruptive action that reduces risk.
3. Obtain incident-command approval for material containment.
4. Involve business operations before disabling a business user account or
   interrupting a business-critical service, unless an emergency process directs
   otherwise.
5. Record the action, owner, approval, start time, result, and residual risk.

Exit criterion: the suspected unauthorized path is interrupted or a documented
risk acceptance and compensating control exists.

### 5. Investigate and remediate

1. Scope affected identities, assets, data, integrations, and time period.
2. Establish a root-cause hypothesis and test it with evidence.
3. Assign remediation to the responsible owner with a change record.
4. Remove the cause, not only the observed symptom.
5. Retain a record of remediation implementation and any accepted risk.

Exit criterion: root cause, scope, and remediation status are documented.

### 6. Recover and validate

1. Restore approved access or service through a controlled process.
2. Run appropriate health, functional, security, and monitoring checks.
3. Confirm that no recurrence appears during the monitoring period chosen by
   the incident commander.
4. Verify that logging and detection coverage remain active.

Exit criterion: the affected service owner confirms stable recovery.

### 7. Privacy and notification decision gate

The SOC provides facts and evidence. The privacy/compliance owner and legal
counsel determine whether the event involves unauthorized access, the relevant
risk level, contractual requirements, and notification obligations. Record:

- the decision owner and time;
- the facts supplied for assessment;
- the decision and rationale;
- any reporting, communications, or follow-up requirement.

Do not make a legal notification decision from a detection rule alone.

### 8. Close and improve

1. Confirm all containment, remediation, recovery, and notification actions are
   complete or have a tracked owner and deadline.
2. Complete the incident report and post-incident review.
3. Capture detection tuning, control gaps, and audit evidence requirements.
4. Obtain the named closure approval.

Exit criterion: the case has a complete audit trail and all remaining work is
tracked to an owner.

## Escalation triggers

Escalate immediately to the incident commander when there is credible evidence
of ongoing unauthorized access, high-impact service degradation, compromise of
a privileged identity, production workload compromise, unauthorized sensitive
data export, or a potential privacy event needing rapid assessment.

## Communications

Use approved internal channels and communicate facts, uncertainty, actions,
decisions, and next update time. Do not speculate, assign blame, or disclose
sensitive or employee information beyond the need-to-know group.

## Review and exercise

Review this standard after a material incident or at the documented review
cycle. Exercise every scenario-specific playbook at least annually and update
the last-exercise date, owner, lessons learned, and follow-up actions.
