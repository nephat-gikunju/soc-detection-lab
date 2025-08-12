# Detection Engineering

This directory contains the portable detection catalog used by the runnable
lab. The Python engine in src/soc_lab/engine.py is deliberately small and
readable so that a reviewer can inspect every condition without deploying a
SIEM.

The rules represent detection logic, not production-ready thresholds. A real
deployment needs a documented log source, field mapping, baseline, tuning
history, change owner, test fixture, and review date.

## Rule traceability

| Scenario | Detection | Playbook |
| --- | --- | --- |
| SC-001 | SOC-001 | PB-001 |
| SC-002 | SOC-002 | PB-002 |
| SC-003 | SOC-003 and SOC-004 | PB-003 |

## Production adaptation

Map the normalized event fields to your SIEM, retain raw evidence according to
your organization’s approved retention policy, and test each rule with benign
and alert-producing fixtures before enabling an automated response.

The rules intentionally avoid raw sensitive content. Events use synthetic
record references and counts so that the SOC can investigate access behaviour
without placing customer or business content in the detection pipeline.
