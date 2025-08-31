# SC-003: Kubernetes Production Control Break

## Scenario

An admission policy blocks an unsigned synthetic records API image in a
production namespace. Shortly afterward, a developer identity opens an
interactive session in the workload without a break-glass record. A synthetic
runtime alert and unapproved egress event provide corroborating context.

## Run

~~~text
make lab-3
~~~

## Expected result

The detector raises:

| Rule | Severity | Reason |
| --- | --- | --- |
| SOC-003 | High | An admission control rejected an unsafe production workload. |
| SOC-004 | Critical | Unapproved production execution correlates with a runtime shell and unapproved egress. |

## Analyst outcome

Follow PB-003. Preserve audit, runtime, deployment, image, RBAC, and network
evidence before using an approved containment procedure. Rebuild and redeploy
a clean image through the future DevSecOps pipeline rather than patching a
running container in place.

All workloads, addresses, identities, and image names are synthetic.
