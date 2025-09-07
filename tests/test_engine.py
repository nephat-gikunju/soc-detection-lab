from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from soc_lab.engine import load_events, run_detections, write_alerts


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = REPOSITORY_ROOT / "scenarios"


class DetectionEngineTests(unittest.TestCase):
    def alerts_for(self, scenario: str):
        events = load_events(SCENARIOS / scenario)
        return run_detections(events)

    def test_bulk_sensitive_record_access(self):
        alerts = self.alerts_for("01-sensitive-record-access")
        self.assertEqual([alert.rule_id for alert in alerts], ["SOC-001"])
        self.assertEqual(alerts[0].severity, "high")
        self.assertEqual(alerts[0].details["access_count"], 6)

    def test_privileged_account_anomaly(self):
        alerts = self.alerts_for("02-privileged-account-authentication-anomaly")
        self.assertEqual([alert.rule_id for alert in alerts], ["SOC-002"])
        self.assertEqual(alerts[0].severity, "critical")
        self.assertEqual(alerts[0].details["failed_attempts"], 5)

    def test_kubernetes_production_control_break(self):
        alerts = self.alerts_for("03-kubernetes-production-control-break")
        self.assertEqual(
            [alert.rule_id for alert in alerts],
            ["SOC-004", "SOC-003"],
        )
        self.assertEqual(alerts[0].severity, "critical")
        self.assertEqual(alerts[1].severity, "high")

    def test_alert_output_is_valid_json(self):
        alerts = self.alerts_for("01-sensitive-record-access")
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "alerts.json"
            write_alerts(alerts, output_path)
            payload = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(payload[0]["rule_id"], "SOC-001")


if __name__ == "__main__":
    unittest.main()
