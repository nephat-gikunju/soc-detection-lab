"""Data models used by the lab detector."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Alert:
    """A normalised security alert produced from synthetic event data."""

    alert_id: str
    rule_id: str
    title: str
    severity: str
    confidence: str
    first_seen: str
    last_seen: str
    summary: str
    recommended_playbook: str
    evidence_event_ids: tuple[str, ...]
    details: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        """Return an alert shape suitable for JSON output."""

        return asdict(self)
