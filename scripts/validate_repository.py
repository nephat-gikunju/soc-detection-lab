"""Verify repository conventions and synthetic scenario expectations."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from soc_lab.engine import load_events, run_detections  # noqa: E402


EMOJI_PATTERN = re.compile(
    "["
    "\U0001F000-\U0001FAFF"
    "\U0001FC00-\U0001FFFD"
    "\u2600-\u27BF"
    "]"
)
EXCLUDED_DIRECTORIES = {".git", "__pycache__", "artifacts"}
EXPECTED_RULES = {
    "01-sensitive-record-access": {"SOC-001"},
    "02-privileged-account-authentication-anomaly": {"SOC-002"},
    "03-kubernetes-production-control-break": {"SOC-003", "SOC-004"},
}
REQUIRED_PATHS = {
    "README.md",
    "detections/rules.json",
    "docs/architecture.md",
    "docs/lab-guide.md",
    "docs/soc-walkthrough.md",
    "docs/evidence-and-reporting.md",
    "docs/data-handling-and-safety.md",
    "playbooks/PB-000-incident-management-standard.md",
    "playbooks/PB-001-sensitive-record-access.md",
    "playbooks/PB-002-privileged-account-authentication-anomaly.md",
    "playbooks/PB-003-kubernetes-production-control-break.md",
}
REQUIRED_PLAYBOOK_HEADINGS = {
    "playbooks/PB-000-incident-management-standard.md": [
        "## Purpose",
        "## Roles and responsibilities",
        "## Incident lifecycle",
        "### 1. Acknowledge and register",
        "### 2. Triage and classify",
        "### 3. Preserve evidence",
        "### 4. Contain",
        "### 5. Investigate and remediate",
        "### 6. Recover and validate",
        "### 7. Privacy and notification decision gate",
        "### 8. Close and improve",
    ],
    "playbooks/PB-001-sensitive-record-access.md": [
        "## Trigger and scope",
        "## Stage 1: acknowledge and triage",
        "## Stage 2: contain",
        "## Stage 3: investigate",
        "## Stage 4: eradicate and remediate",
        "## Stage 5: recover and validate",
        "## Stage 6: privacy and communications assessment",
        "## Stage 7: close and improve",
    ],
    "playbooks/PB-002-privileged-account-authentication-anomaly.md": [
        "## Trigger and scope",
        "## Stage 1: acknowledge and triage",
        "## Stage 2: contain",
        "## Stage 3: investigate",
        "## Stage 4: eradicate and remediate",
        "## Stage 5: recover and validate",
        "## Stage 6: privacy and communications assessment",
        "## Stage 7: close and improve",
    ],
    "playbooks/PB-003-kubernetes-production-control-break.md": [
        "## Trigger and scope",
        "## Stage 1: acknowledge and triage",
        "## Stage 2: preserve evidence",
        "## Stage 3: contain",
        "## Stage 4: investigate",
        "## Stage 5: eradicate and remediate",
        "## Stage 6: recover and validate",
        "## Stage 7: privacy and communications assessment",
        "## Stage 8: close and improve",
    ],
}
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def assert_no_emojis() -> None:
    violations: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in EXCLUDED_DIRECTORIES for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if EMOJI_PATTERN.search(text):
            violations.append(str(path.relative_to(ROOT)))
    if violations:
        names = ", ".join(violations)
        raise AssertionError(f"Emoji characters are not allowed: {names}")


def assert_scenarios_match_expectations() -> None:
    for scenario, expected_rules in EXPECTED_RULES.items():
        alerts = run_detections(load_events(ROOT / "scenarios" / scenario))
        actual_rules = {alert.rule_id for alert in alerts}
        if actual_rules != expected_rules:
            message = (
                f"{scenario}: expected {sorted(expected_rules)}, "
                f"received {sorted(actual_rules)}"
            )
            raise AssertionError(message)


def assert_required_documentation() -> None:
    missing = sorted(path for path in REQUIRED_PATHS if not (ROOT / path).is_file())
    if missing:
        raise AssertionError(f"Required documentation is missing: {', '.join(missing)}")

    for relative_path, headings in REQUIRED_PLAYBOOK_HEADINGS.items():
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        missing_headings = [heading for heading in headings if heading not in text]
        if missing_headings:
            details = ", ".join(missing_headings)
            raise AssertionError(f"{relative_path} is missing headings: {details}")


def assert_local_markdown_links_resolve() -> None:
    broken: list[str] = []
    for markdown_path in ROOT.rglob("*.md"):
        if any(part in EXCLUDED_DIRECTORIES for part in markdown_path.parts):
            continue
        text = markdown_path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK_PATTERN.findall(text):
            target = target.strip()
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            local_target = target.split("#", maxsplit=1)[0]
            if not local_target:
                continue
            resolved = (markdown_path.parent / local_target).resolve()
            if not resolved.exists():
                source = markdown_path.relative_to(ROOT)
                broken.append(f"{source} -> {target}")
    if broken:
        raise AssertionError(f"Broken local Markdown links: {'; '.join(broken)}")


def main() -> None:
    assert_no_emojis()
    assert_scenarios_match_expectations()
    assert_required_documentation()
    assert_local_markdown_links_resolve()
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
