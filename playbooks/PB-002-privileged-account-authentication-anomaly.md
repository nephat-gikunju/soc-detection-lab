# PB-002: Privileged-Account Authentication Anomaly

| Field | Value |
| --- | --- |
| Version | 1.0 |
| Owner role | SOC manager and identity-security owner |
| Review cycle | Every six months and after an identity incident |
| Linked detection | SOC-002 |
| Linked scenario | SC-002 |
| Default severity | Critical |
| Last exercise | Record after first completed lab exercise |

## Purpose

Investigate a suspected privileged-account takeover without confusing a
repeated authentication failure with a confirmed compromise. Contain active
identity risk while retaining a safe route for legitimate business or
operational work.

Use [PB-000](PB-000-incident-management-standard.md) for shared evidence,
communications, privacy, and closure requirements.

## Trigger and scope

Start this playbook when SOC-002 fires or when the identity provider, an
administrator, or another trusted control reports suspicious privileged-account
activity.

Treat the case as critical when repeated failures are followed by successful
authentication from an unfamiliar source, especially where there is evidence
of privileged actions, access to sensitive-data systems, security-control
changes, or persistence.

## Required initial evidence

Collect:

- alert ID, rule ID, timestamps, and source event IDs;
- actor, role, entitlement set, and privileged-access status;
- failed and successful authentication sequence;
- source IP, network, device, session, conditional-access, and MFA context;
- password-reset, MFA-enrollment, recovery-method, and session-revocation
  events;
- administrative, API, sensitive-data, and role-change activity after sign-in;
- approved travel, maintenance, support, emergency-access, or change context.

Do not record passwords, MFA secrets, tokens, recovery codes, or unrelated
personnel data.

## Stage 1: acknowledge and triage

1. Create a case and preserve the alert window.
2. Validate that the identity-provider events belong to the expected actor and
   that timestamps and source fields are reliable.
3. Compare the successful sign-in with the failure source, known-device
   history, MFA result, conditional-access policy, and approved work context.
4. Review activity after the sign-in, prioritizing privilege changes, session
   creation, sensitive-data access, partner integration activity, and secret
   access.
5. Contact the account owner through an independently verified communication
   route if organizational process permits.
6. Escalate to the incident commander when compromise is plausible or active
   privileged activity is observed.

| Decision point | Action |
| --- | --- |
| Evidence supports an approved activity | Document evidence and close through normal review. |
| Authentication anomaly remains unexplained | Keep critical priority and contain sessions while investigation continues. |
| Account compromise is likely or confirmed | Initiate approved identity containment and scope all potentially affected systems. |
| Business-service workflow relies on the account | Involve business operations before disabling access; provide a safe alternate workflow. |

Exit criterion: the team has an evidence-backed assessment of whether the
privileged identity is at risk and whether active sessions must be contained.

## Stage 2: contain

Use the least disruptive approved control that terminates unauthorized access:

1. Revoke active sessions, refresh tokens, and API tokens associated with the
   suspected compromise.
2. Block a confirmed unauthorized source using the approved identity or network
   process.
3. Temporarily suspend privileged roles or the account after confirming a safe
   alternate workflow with the business and service owner.
4. Remove unauthorized devices, recovery methods, or federation sessions.
5. Preserve required logs before altering identity configuration.

Record the containment owner, approver, scope, result, service impact, and
remaining risk.

Exit criterion: unauthorized identity access is no longer active or a
documented compensating control is in place.

## Stage 3: investigate

1. Create a detailed authentication timeline from the first failure through
   containment.
2. Review MFA outcomes, device records, source history, session creation,
   password resets, recovery changes, and conditional-access decisions.
3. Review all privileged actions and access to high-value services after the
   successful sign-in.
4. Search for related activity from the same source, device, session, or
   technique across other accounts.
5. Review email, endpoint, and help-desk evidence when authorized and
   relevant.
6. Determine the most plausible initial-access path and the affected scope.

Exit criterion: the case contains a defensible scope statement and root-cause
hypothesis.

## Stage 4: eradicate and remediate

Coordinate with the identity owner to:

- reset credentials through an approved process;
- require MFA re-enrollment where justified;
- revoke remaining tokens, sessions, devices, or recovery methods;
- correct conditional-access, monitoring, privilege-review, or emergency-access
  control gaps;
- remove unauthorized role grants or integration credentials;
- create engineering and awareness follow-up actions where the investigation
  identifies a preventable control failure.

Validate every change and record the implementation owner and reference.

Exit criterion: identity controls are restored to a known-good, least-privilege
state.

## Stage 5: recover and validate

1. Restore approved access using verified identity proofing and least privilege.
2. Confirm the user can perform necessary authorized work.
3. Verify MFA, conditional access, session controls, audit logging, and alert
   coverage.
4. Monitor for repeat authentication anomalies and related account activity.
5. Obtain business-owner and, where relevant, business-operations sign-off.

Exit criterion: the account is recovered safely and no recurrence is observed
during the agreed monitoring period.

## Stage 6: privacy and communications assessment

If the account accessed sensitive-data systems, privileged integrations, or other
sensitive services, send the factual scope to the privacy/compliance owner and
legal counsel. Record their decision on privacy assessment and any required
communication.

Only the appropriate accountable roles determine notification obligations.

## Stage 7: close and improve

Before closure:

1. Complete the incident case and evidence log.
2. Confirm remediation, recovery, and monitoring results.
3. Complete a post-incident review for a confirmed compromise or significant
   near-miss.
4. Tune SOC-002 using identity risk, MFA, device, source, and role context.
5. Review privileged-access and emergency-access controls.
6. Obtain closure approval from the incident commander.

## Exercise outcome for SC-002

The expected lab outcome is a critical identity investigation. The analyst
should preserve the five failed attempts and the new-source successful sign-in,
document a safe session-containment decision, scope post-authentication
activity, and identify identity-control remediation.
