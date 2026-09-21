# SOC Lab

A reproducible, defensive security operations lab.
It demonstrates application, identity, and Kubernetes detection engineering;
end-to-end SOC incident handling; privacy-aware evidence collection; and
remediation verification.

The organization is intentionally unnamed. Every event, identity, record
reference, address, image name, and finding in this repository is synthetic.
This project does not connect to, target, or represent a production system.

## Portfolio outcome

This repository demonstrates the operational loop expected of a security
analyst:

~~~text
Synthetic logs
  -> normalized detections
  -> alert triage
  -> containment and investigation
  -> remediation and recovery
  -> evidence, tuning, and closure
~~~

It is designed to be easy for a recruiter or technical reviewer to run. There
are no external Python dependencies and no SIEM deployment required to validate
the scenario logic.

## Labs

| Scenario | Detection | What it demonstrates | Playbook |
| --- | --- | --- | --- |
| SC-001: Bulk sensitive-record access | SOC-001 | Application audit monitoring, privacy-aware triage, access investigation | [PB-001](playbooks/PB-001-sensitive-record-access.md) |
| SC-002: Privileged-account anomaly | SOC-002 | Identity monitoring, account-takeover triage, safe containment | [PB-002](playbooks/PB-002-privileged-account-authentication-anomaly.md) |
| SC-003: Kubernetes control break | SOC-003 and SOC-004 | Admission-control monitoring, runtime correlation, Kubernetes response | [PB-003](playbooks/PB-003-kubernetes-production-control-break.md) |

## Architecture

~~~mermaid
flowchart LR
    A["Synthetic application, identity, and Kubernetes events"] --> B["Portable detection engine"]
    B --> C["Normalized alerts"]
    C --> D["SOC case and evidence register"]
    D --> E["Playbook-guided containment and investigation"]
    E --> F["Remediation, recovery, and verification"]
    F --> G["Detection tuning and post-incident review"]
~~~

For a detailed design, read [the architecture guide](docs/architecture.md).

## Quick start

Prerequisites:

- Python 3.11 or later
- GNU Make is optional but recommended

Clone your published repository, enter it, and run:

~~~text
make validate
make test
make demo
~~~

To run one lab at a time:

~~~text
make lab-1
make lab-2
make lab-3
~~~

The same commands can run without Make:

~~~text
PYTHONPATH=src python3 -m soc_lab scenarios/01-sensitive-record-access
PYTHONPATH=src python3 -m soc_lab scenarios/02-privileged-account-authentication-anomaly
PYTHONPATH=src python3 -m soc_lab scenarios/03-kubernetes-production-control-break
~~~

## What the reviewer can verify

| Check | Command | Expected result |
| --- | --- | --- |
| Repository conventions | make validate | Scenario fixtures match expected detection IDs and repository content contains no emoji characters. |
| Unit tests | make test | The detector produces the expected severity and evidence for every scenario. |
| Full walkthrough | make demo | Validation, tests, and all three scenario outputs complete successfully. |
| Continuous integration | GitHub Actions | The same validation and test checks run on pushes and pull requests. |

## Scenario walkthrough

Start with [the SOC walkthrough](docs/soc-walkthrough.md). It explains how an
analyst should move from the generated alert to evidence collection, decision
making, containment, recovery, and post-incident improvement.

The project deliberately distinguishes between:

- a suspicious signal and a confirmed incident;
- an alert severity and business-impact assessment;
- automated evidence collection and human-approved containment;
- remediation of a server and rebuilding a container image.

## Documentation

- [Architecture](docs/architecture.md)
- [Lab guide](docs/lab-guide.md)
- [Detection engineering guide](detections/README.md)
- [SOC walkthrough](docs/soc-walkthrough.md)
- [Evidence and reporting standard](docs/evidence-and-reporting.md)
- [Data handling and safety](docs/data-handling-and-safety.md)
- [Incident-management standard](playbooks/PB-000-incident-management-standard.md)
- [Playbook index](playbooks/README.md)

## Safety and privacy

Use the lab only with the included synthetic data and within an environment you
own or are explicitly authorized to test. Do not upload real sensitive data,
tokens, credentials, organizational logs, or production configurations.

The privacy and notification sections in the playbooks are operational
decision gates, not legal advice. A real organization must involve its
privacy/compliance owner, legal counsel, incident commander, and relevant
business leaders when assessing an event.

## Roadmap

This SOC lab is the first phase of a wider security portfolio. Logical next
phases are:

1. A vulnerability-to-remediation orchestrator that enriches scanner findings
   with SIEM context and opens approved remediation work.
2. A DevSecOps and Kubernetes pipeline that scans code, dependencies, images,
   and infrastructure; generates an SBOM; and enforces admission policies.
3. SIEM integration using Wazuh or Elastic, while retaining these portable
   fixtures as deterministic detection tests.

## Repository layout

~~~text
.
├── detections/          Portable detection catalog
├── docs/                Architecture, walkthroughs, and evidence guidance
├── playbooks/           End-to-end incident response playbooks
├── scenarios/           Safe JSONL fixtures and expected alerts
├── scripts/             Repository validation
├── src/soc_lab/         Runnable detection engine
└── tests/               Unit tests
~~~

## License

Released under the [MIT License](LICENSE).
