"""Command-line interface for running a lab scenario."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import load_events, run_detections, write_alerts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a synthetic SOC lab scenario."
    )
    parser.add_argument(
        "scenario",
        type=Path,
        help="Scenario directory containing events.jsonl, or an events.jsonl file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path for normalised alerts as JSON.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print normalised alerts as JSON instead of the analyst summary.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    events = load_events(args.scenario)
    alerts = run_detections(events)

    if args.output:
        write_alerts(alerts, args.output)

    if args.json:
        print(json.dumps([alert.as_dict() for alert in alerts], indent=2))
        return

    print(f"Scenario: {args.scenario}")
    print(f"Events processed: {len(events)}")
    print(f"Alerts raised: {len(alerts)}")
    for alert in alerts:
        print()
        print(f"[{alert.severity.upper()}] {alert.rule_id}: {alert.title}")
        print(f"Summary: {alert.summary}")
        print(f"Recommended playbook: {alert.recommended_playbook}")
        print(f"Evidence events: {', '.join(alert.evidence_event_ids)}")
