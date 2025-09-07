# Architecture

## Design goal

The lab represents a compact SOC workflow without requiring a heavy SIEM
deployment. It separates event generation, detection, playbook execution, and
evidence handling so each part can be inspected and tested independently.

~~~mermaid
flowchart TB
    A["Scenario JSONL fixtures"] --> B["Event validation"]
    B --> C["Detection engine"]
    C --> D["Alert output"]
    D --> E["SOC analyst"]
    E --> F["Playbook"]
    F --> G["Evidence register and case report"]
    F --> H["Containment and remediation decision"]
    H --> I["Recovery validation"]
    I --> J["Detection tuning"]
    J --> C
~~~

## Components

| Component | Responsibility | Repository location |
| --- | --- | --- |
| Scenario fixtures | Represent safe, synthetic application, identity, and Kubernetes events. | scenarios/ |
| Detection engine | Applies transparent correlation logic to normalized events. | src/soc_lab/engine.py |
| Detection catalog | Documents logic, scope, false positives, and playbook links. | detections/rules.json |
| Playbooks | Define end-to-end analyst actions and decision gates. | playbooks/ |
| Evidence templates | Standardize what an analyst records. | playbooks/templates/ |
| Tests | Confirm that fixtures produce the expected alert rules and severity. | tests/ |

## Normalized event fields

Every event fixture contains the fields below:

| Field | Purpose |
| --- | --- |
| event_id | Stable evidence reference. |
| timestamp | UTC ISO 8601 event time. |
| event_type | Normalized activity type used by the detector. |
| actor | Synthetic identity and role. |
| source | Synthetic IP address and network context. |
| asset | Asset identifier, classification, and environment. |

Additional fields are event-specific. The project favors counts, record
references, and behavior context instead of sensitive content.

## Trust boundaries

The detector processes only the supplied local fixtures. It makes no network
calls and has no access to a SIEM, endpoint agent, Kubernetes cluster, cloud
account, or production system.

When adapted to an organization, the same logical boundaries should exist:

1. Collect application, identity, endpoint, cloud, and Kubernetes telemetry.
2. Normalize and protect event data before it reaches detection logic.
3. Limit analyst access to the minimum data necessary for investigation.
4. Require incident-command and business-operations approval for actions that
   may affect a critical business service.
5. Record evidence, decisions, and validation results in the incident case.

## Production integration boundary

Wazuh or Elastic can ingest and correlate the equivalent event sources. This
repository deliberately keeps the core logic independent of either platform so
that the project remains runnable and testable on a basic local machine.

Do not treat a container as a patchable server. Container findings should
normally be remediated by updating dependencies or a base image, rebuilding,
scanning, and redeploying an immutable image. Node and VM patching is a
separate approved remediation workflow.
