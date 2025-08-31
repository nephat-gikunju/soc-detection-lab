# PB-003: Kubernetes Production Control Break

| Field | Value |
| --- | --- |
| Version | 1.0 |
| Owner role | SOC manager and platform-security owner |
| Review cycle | Every six months and after a production platform incident |
| Linked detections | SOC-003 and SOC-004 |
| Linked scenario | SC-003 |
| Default severity | High; critical when correlated runtime or egress evidence exists |
| Last exercise | Record after first completed lab exercise |

## Purpose

Investigate a blocked unsafe Kubernetes deployment, unapproved production
execution, or correlated workload compromise while preserving evidence,
limiting exposure, and restoring a clean workload through an approved delivery
process.

Use [PB-000](PB-000-incident-management-standard.md) for shared incident
requirements.

## Trigger and scope

Start this playbook for:

- a production admission-policy denial involving an unsafe workload;
- interactive execution in a production workload without a documented
  break-glass approval;
- a correlated runtime shell, unexpected egress, RBAC change, secret access,
  or related platform-security signal.

Raise severity to critical when unapproved execution correlates with a runtime
alert, unapproved egress, suspicious credential access, or evidence of sensitive
data exposure.

## Required initial evidence

Collect:

- alert IDs, rule IDs, timestamps, and source event IDs;
- cluster, namespace, workload, pod, node, service account, and image digest;
- Kubernetes audit event, admission decision, deployment manifest, and rollout
  history;
- runtime-security events and associated process context;
- relevant network telemetry, destination context, and egress policy;
- RBAC bindings, service-account permissions, secret-access events, and
  break-glass or change records;
- CI/CD run, source revision, scan result, SBOM, and image provenance where
  available;
- service health, business-service impact, and dependency context.

Do not copy secret values, tokens, kubeconfig content, or customer data into
the case record.

## Stage 1: acknowledge and triage

1. Create a case and preserve the alerting event window.
2. Validate cluster, namespace, workload, actor, timestamp, and log source.
3. Determine whether the event is a prevented deployment, an authorized
   maintenance action, a suspicious control bypass attempt, or a confirmed
   production compromise.
4. Check for a valid change record and time-limited break-glass approval.
5. Correlate the audit event with runtime, network, image, RBAC, and identity
   evidence.
6. Assess workload criticality, service health, data classification, and
   potential business-service impact.
7. Escalate to the incident commander and platform owner when execution or
   compromise is plausible.

| Decision point | Action |
| --- | --- |
| Admission denial only, with valid change context | Document the control working; route correction to the deployment owner. |
| Unapproved production execution without corroboration | Treat as high severity; preserve evidence and validate authorization urgently. |
| Execution plus runtime shell, unapproved egress, or sensitive access | Treat as critical; initiate approved containment. |
| Business-critical service may be affected | Involve business operations before disruptive isolation or shutdown. |

Exit criterion: the incident commander has a documented risk classification,
service-impact assessment, and containment plan.

## Stage 2: preserve evidence

Before changing the workload when feasible:

1. Export the relevant Kubernetes audit events and admission decisions.
2. Record pod name, namespace, workload, image digest, container IDs, service
   account, node, and rollout history.
3. Preserve runtime alerts, relevant logs, network telemetry, RBAC bindings,
   service-account permissions, and deployment manifests.
4. Capture CI/CD provenance, SBOM, image scan results, and source revision.
5. Use an approved snapshot or forensic process if your organization provides
   one.
6. Record every evidence location in the evidence log.

Exit criterion: the team can reconstruct the execution and deployment timeline
without relying on an altered workload.

## Stage 3: contain

Choose containment jointly with the incident commander, platform owner, and
business operations when a critical business workflow could be affected.
Possible approved actions include:

1. Pause unsafe deployment changes or revoke the deployment credential.
2. Isolate workload egress with an approved network policy or service-mesh
   control.
3. Scale down or quarantine only the affected workload when a safe alternative
   service path exists.
4. Revoke and rotate a compromised service account, token, or kubeconfig.
5. Restrict unapproved interactive execution through RBAC and break-glass
   controls.
6. Preserve safe service continuity using a known-good deployment when
   possible.

Record approval, owner, expected impact, health outcome, and residual risk.

Exit criterion: the suspected execution, egress, or deployment path is
interrupted without unsafe disruption to a critical service.

## Stage 4: investigate

1. Build a timeline that includes source code change, CI/CD run, image build,
   scan, admission policy result, deployment action, audit event, runtime
   event, and network activity.
2. Review image provenance, base image, dependency inventory, SBOM, and
   repository access.
3. Review RBAC bindings, service accounts, secrets access, and recent role
   changes.
4. Scope nearby workloads, namespaces, shared secrets, and dependent services.
5. Determine whether the root cause is a policy violation, a compromised
   identity, an unsafe image, excessive RBAC, a runtime defect, or a process
   gap.
6. Document confirmed evidence separately from hypotheses.

Exit criterion: the investigation identifies the likely root cause, scope, and
the correct remediation path.

## Stage 5: eradicate and remediate

Do not patch a running container in place. Coordinate a clean, immutable
remediation:

1. Update the source, dependency, configuration, or base image that caused the
   risk.
2. Rebuild the image from a trusted pipeline.
3. Run code, dependency, image, and infrastructure checks.
4. Generate or update an SBOM and record the image digest.
5. Correct RBAC, network policy, admission controls, secret handling, or
   provenance gaps exposed by the investigation.
6. Obtain change approval and deploy the clean image through the controlled
   pipeline.

For an affected node or VM, use a separate approved patch-management workflow
after assessing availability and rollback. Do not conflate node patching with
container remediation.

Exit criterion: a clean and verified deployment artifact is ready for recovery.

## Stage 6: recover and validate

1. Deploy the approved clean workload using a controlled rollout.
2. Run application health checks and synthetic functional tests.
3. Confirm the admission policy, RBAC, runtime monitoring, network controls,
   and audit logging are active.
4. Verify that the suspicious alert conditions no longer occur.
5. Monitor the workload, related service accounts, and egress behavior for the
   period chosen by the incident commander.
6. Obtain platform-owner and service-owner approval before case recovery is
   complete.

Exit criterion: the workload operates normally with verified controls and no
recurrence during the monitoring period.

## Stage 7: privacy and communications assessment

If evidence shows or reasonably suggests access to sensitive-data systems,
exposure of credentials, or unauthorized external transmission, provide the
factual incident package to the privacy/compliance owner and legal counsel.
They determine notification and communications obligations.

Record the assessment request, decision owner, decision, and follow-up actions.

## Stage 8: close and improve

Before closure:

1. Complete the incident case, evidence log, and recovery verification.
2. Track every remediation, policy, code, access-review, or training action.
3. Complete a post-incident review for a confirmed compromise or material
   control-break attempt.
4. Tune SOC-003 and SOC-004 based on approved-maintenance patterns,
   break-glass usage, image provenance, and correlation quality.
5. Test the improved detections using a safe fixture before deployment.
6. Obtain closure approval from the incident commander and platform owner.

## Exercise outcome for SC-003

The expected lab outcome is two related alerts:

- SOC-003 shows that admission control blocked an unsafe production
  deployment.
- SOC-004 becomes critical because unapproved production execution
  correlates with a runtime shell and unapproved egress.

The analyst should preserve the five scenario event IDs, distinguish prevention
from compromise, propose approved workload isolation, and describe a clean
image rebuild and redeployment path.
