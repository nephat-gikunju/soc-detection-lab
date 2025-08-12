"""Small, transparent detection engine for the portfolio lab.

The rules are intentionally readable. They illustrate analyst reasoning and are
not intended to replace a production SIEM correlation engine.
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable

from .models import Alert

Event = dict[str, Any]

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def parse_timestamp(value: str) -> datetime:
    """Parse an ISO 8601 timestamp and normalise it to UTC."""

    timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        return timestamp.replace(tzinfo=UTC)
    return timestamp.astimezone(UTC)


def nested_value(event: Event, path: str, default: Any = None) -> Any:
    """Return a dotted field from a nested event without raising KeyError."""

    value: Any = event
    for part in path.split("."):
        if not isinstance(value, dict):
            return default
        value = value.get(part, default)
    return value


def load_events(path: str | Path) -> list[Event]:
    """Load and validate JSON Lines events from a scenario directory or file."""

    source = Path(path)
    event_file = source / "events.jsonl" if source.is_dir() else source
    events: list[Event] = []

    with event_file.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as error:
                message = f"{event_file}:{line_number} is not valid JSON: {error.msg}"
                raise ValueError(message) from error

            required_fields = {"event_id", "timestamp", "event_type", "actor", "asset"}
            missing = sorted(required_fields - set(event))
            if missing:
                message = f"{event_file}:{line_number} is missing {', '.join(missing)}"
                raise ValueError(message)

            parse_timestamp(event["timestamp"])
            events.append(event)

    if not events:
        raise ValueError(f"{event_file} does not contain any events")

    return sorted(events, key=lambda event: parse_timestamp(event["timestamp"]))


def _alert(
    *,
    rule_id: str,
    title: str,
    severity: str,
    confidence: str,
    events: Iterable[Event],
    summary: str,
    playbook: str,
    details: dict[str, Any],
) -> Alert:
    evidence = tuple(events)
    timestamps = [event["timestamp"] for event in evidence]
    actor = nested_value(evidence[0], "actor.id", "unknown")
    first_seen = min(timestamps)
    last_seen = max(timestamps)
    return Alert(
        alert_id=f"{rule_id}-{actor}-{first_seen.replace(':', '').replace('-', '')}",
        rule_id=rule_id,
        title=title,
        severity=severity,
        confidence=confidence,
        first_seen=first_seen,
        last_seen=last_seen,
        summary=summary,
        recommended_playbook=playbook,
        evidence_event_ids=tuple(event["event_id"] for event in evidence),
        details=details,
    )


def detect_bulk_sensitive_record_access(events: list[Event]) -> list[Alert]:
    """Detect five or more successful sensitive-data reads in ten minutes.

    The threshold is deliberately low for a lab exercise. In production it
    should be baselined by role, workflow, business schedule, and data-access
    pattern.
    """

    candidates = [
        event
        for event in events
        if event["event_type"] == "sensitive_record_access"
        and event.get("outcome") == "success"
        and nested_value(event, "asset.classification") == "sensitive-data"
    ]
    by_actor: dict[str, list[Event]] = defaultdict(list)
    for event in candidates:
        by_actor[str(nested_value(event, "actor.id", "unknown"))].append(event)

    alerts: list[Alert] = []
    for actor, actor_events in by_actor.items():
        for start_index, start_event in enumerate(actor_events):
            start = parse_timestamp(start_event["timestamp"])
            window = [
                event
                for event in actor_events[start_index:]
                if parse_timestamp(event["timestamp"]) <= start + timedelta(minutes=10)
            ]
            if len(window) < 5:
                continue

            source_networks = sorted(
                {
                    str(nested_value(event, "source.network", "unknown"))
                    for event in window
                }
            )
            source_ips = sorted(
                {
                    str(nested_value(event, "source.ip", "unknown"))
                    for event in window
                }
            )
            record_ids = sorted(
                {str(event.get("record_id", "unknown")) for event in window}
            )
            severity = "high" if "external" in source_networks else "medium"
            summary = (
                f"{actor} accessed {len(window)} synthetic sensitive records in "
                f"ten minutes from {', '.join(source_ips)}."
            )
            alerts.append(
                _alert(
                    rule_id="SOC-001",
                    title="Suspicious bulk sensitive-record access",
                    severity=severity,
                    confidence="medium",
                    events=window,
                    summary=summary,
                    playbook="playbooks/PB-001-sensitive-record-access.md",
                    details={
                        "actor": actor,
                        "access_count": len(window),
                        "source_ips": source_ips,
                        "source_networks": source_networks,
                        "synthetic_record_ids": record_ids,
                        "window_minutes": 10,
                    },
                )
            )
            break
    return alerts


def detect_privileged_authentication_anomaly(events: list[Event]) -> list[Alert]:
    """Detect repeated privileged-account failures followed by new-IP success."""

    failures = [
        event
        for event in events
        if event["event_type"] == "authentication_failure"
        and nested_value(event, "actor.role") in {"administrator", "platform_admin"}
    ]
    successes = [
        event
        for event in events
        if event["event_type"] == "authentication_success"
        and nested_value(event, "actor.role") in {"administrator", "platform_admin"}
    ]
    by_actor: dict[str, list[Event]] = defaultdict(list)
    for event in failures:
        by_actor[str(nested_value(event, "actor.id", "unknown"))].append(event)

    alerts: list[Alert] = []
    for actor, actor_failures in by_actor.items():
        for start_index, start_event in enumerate(actor_failures):
            start = parse_timestamp(start_event["timestamp"])
            failure_window = [
                event
                for event in actor_failures[start_index:]
                if parse_timestamp(event["timestamp"]) <= start + timedelta(minutes=5)
            ]
            if len(failure_window) < 5:
                continue

            failure_ips = {
                str(nested_value(event, "source.ip", "unknown")) for event in failure_window
            }
            final_failure = parse_timestamp(failure_window[-1]["timestamp"])
            matching_successes = [
                event
                for event in successes
                if nested_value(event, "actor.id") == actor
                and final_failure
                <= parse_timestamp(event["timestamp"])
                <= final_failure + timedelta(minutes=15)
                and str(nested_value(event, "source.ip", "unknown")) not in failure_ips
            ]
            if not matching_successes:
                continue

            success = matching_successes[0]
            evidence = [*failure_window, success]
            success_ip = str(nested_value(success, "source.ip", "unknown"))
            alerts.append(
                _alert(
                    rule_id="SOC-002",
                    title="Privileged-account authentication anomaly",
                    severity="critical",
                    confidence="high",
                    events=evidence,
                    summary=(
                        f"{actor} had {len(failure_window)} failed privileged "
                        f"authentication attempts followed by a success from new "
                        f"source IP {success_ip}."
                    ),
                    playbook=(
                        "playbooks/PB-002-privileged-account-authentication-anomaly.md"
                    ),
                    details={
                        "actor": actor,
                        "failed_attempts": len(failure_window),
                        "failure_source_ips": sorted(failure_ips),
                        "successful_source_ip": success_ip,
                        "success_event_id": success["event_id"],
                        "window_minutes": 15,
                    },
                )
            )
            break
    return alerts


def detect_kubernetes_admission_policy_denial(events: list[Event]) -> list[Alert]:
    """Detect policy controls denying an unsafe workload in production."""

    alerts: list[Alert] = []
    for event in events:
        if event["event_type"] != "kubernetes_admission_denied":
            continue
        if nested_value(event, "asset.environment") != "production":
            continue

        policy = str(event.get("policy", "unknown"))
        reason = str(event.get("reason", "unknown"))
        alerts.append(
            _alert(
                rule_id="SOC-003",
                title="Kubernetes admission policy denied unsafe workload",
                severity="high",
                confidence="high",
                events=[event],
                summary=(
                    f"Policy {policy} denied workload "
                    f"{event.get('workload', 'unknown')} in production: {reason}."
                ),
                playbook="playbooks/PB-003-kubernetes-production-control-break.md",
                details={
                    "policy": policy,
                    "reason": reason,
                    "workload": event.get("workload", "unknown"),
                    "image": event.get("image", "unknown"),
                    "namespace": event.get("namespace", "unknown"),
                },
            )
        )
    return alerts


def detect_unapproved_production_kubernetes_exec(events: list[Event]) -> list[Alert]:
    """Detect interactive execution in a production workload without break-glass.

    A runtime shell alert or unapproved egress occurring within five minutes of
    the execution event raises this laboratory signal to critical severity.
    """

    alerts: list[Alert] = []
    for event in events:
        if event["event_type"] != "kubernetes_exec":
            continue
        if nested_value(event, "asset.environment") != "production":
            continue
        if event.get("break_glass") is True:
            continue

        event_time = parse_timestamp(event["timestamp"])
        workload = str(event.get("workload", "unknown"))
        related_events = [
            candidate
            for candidate in events
            if candidate["event_id"] != event["event_id"]
            and candidate.get("workload") == workload
            and event_time
            <= parse_timestamp(candidate["timestamp"])
            <= event_time + timedelta(minutes=5)
            and candidate["event_type"]
            in {"container_runtime_alert", "network_connection"}
        ]
        runtime_signals = [
            candidate
            for candidate in related_events
            if candidate["event_type"] == "container_runtime_alert"
            and candidate.get("signal") == "shell_spawned_in_container"
        ]
        egress_signals = [
            candidate
            for candidate in related_events
            if candidate["event_type"] == "network_connection"
            and candidate.get("destination_approved") is False
        ]
        correlated_events = [*runtime_signals, *egress_signals]
        severity = "critical" if correlated_events else "high"
        confidence = "high" if correlated_events else "medium"
        actor = str(nested_value(event, "actor.id", "unknown"))
        alerts.append(
            _alert(
                rule_id="SOC-004",
                title="Unapproved interactive Kubernetes execution",
                severity=severity,
                confidence=confidence,
                events=[event, *correlated_events],
                summary=(
                    f"{actor} opened an interactive session in "
                    f"{workload} without a break-glass record. "
                    f"Correlated runtime or egress signals: {len(correlated_events)}."
                ),
                playbook="playbooks/PB-003-kubernetes-production-control-break.md",
                details={
                    "actor": actor,
                    "workload": workload,
                    "namespace": event.get("namespace", "unknown"),
                    "command": event.get("command", []),
                    "break_glass": False,
                    "correlated_event_ids": [
                        candidate["event_id"] for candidate in correlated_events
                    ],
                },
            )
        )
    return alerts


def run_detections(events: list[Event]) -> list[Alert]:
    """Run every lab detector and return alerts in triage order."""

    alerts = [
        *detect_bulk_sensitive_record_access(events),
        *detect_privileged_authentication_anomaly(events),
        *detect_kubernetes_admission_policy_denial(events),
        *detect_unapproved_production_kubernetes_exec(events),
    ]
    return sorted(
        alerts,
        key=lambda alert: (SEVERITY_ORDER[alert.severity], alert.first_seen, alert.rule_id),
    )


def write_alerts(alerts: list[Alert], output_path: str | Path) -> None:
    """Write alert output to a JSON file."""

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = [alert.as_dict() for alert in alerts]
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
