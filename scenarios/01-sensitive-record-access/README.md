# SC-001: Suspected Bulk Sensitive-Record Access

## Scenario

A valid synthetic support-analyst identity accesses six synthetic restricted
records from
an external test address within seven minutes. The lab rule is intentionally
sensitive; an analyst must investigate before treating the signal as an
incident.

## Run

~~~text
make lab-1
~~~

## Expected result

The detector raises SOC-001 at high severity and directs the analyst to
PB-001. The high severity is based on the external network context, not an
assumption that the operations account is compromised.

## Analyst outcome

Use the playbook to verify business purpose, schedule, device, source, export
activity, and approval context. Preserve the event window and obtain incident
commander and service-operations approval before a containment action that
could disrupt a critical business service.

All identifiers and record references in this scenario are synthetic.
