# Lab Guide

## Before you start

This project is safe to run because it processes only local JSONL fixtures. It
does not launch containers, generate attack traffic, scan a network, or connect
to external services.

~~~text
make validate
make test
~~~

Both commands should finish successfully before you begin the walkthroughs.

## SC-001: Bulk sensitive-record access

~~~text
make lab-1
~~~

1. Read the SOC-001 alert summary.
2. Open PB-001 and create a case using the incident-case template.
3. Validate source, shift, authorization, export activity, and business-service
   impact before changing access.
4. Record the containment decision, evidence, recovery checks, and rule-tuning
   notes.

Success means the analyst can distinguish a suspicious high-volume pattern from
a confirmed privacy incident.

## SC-002: Privileged-account authentication anomaly

~~~text
make lab-2
~~~

1. Read the SOC-002 alert and evidence event identifiers.
2. Open PB-002 and validate the failure sequence, successful sign-in, MFA,
   device context, change records, emergency-access approval, and subsequent
   activity.
3. Coordinate a safe session-revocation or account-containment decision.
4. Record the scope, remediation actions, and controlled recovery.

Success means the analyst can preserve business continuity while containing a
potential identity compromise.

## SC-003: Kubernetes production control break

~~~text
make lab-3
~~~

1. Read the admission-policy and interactive-execution alerts.
2. Open PB-003 and preserve audit, runtime, deployment, image, RBAC, and
   network evidence before a disruptive action.
3. Isolate the suspected workload through an approved platform procedure.
4. Rebuild and rescan a clean image, then validate deployment and monitoring.

Success means the analyst can distinguish a prevented deployment from a
correlated runtime incident and can hand remediation back to platform and
development teams.

## Evidence standard

Use the templates under playbooks/templates. Keep the original fixture event
identifiers, timestamps, source context, decision owner, action time, and
verification result. Do not paste raw sensitive information or credentials into
a case record.
