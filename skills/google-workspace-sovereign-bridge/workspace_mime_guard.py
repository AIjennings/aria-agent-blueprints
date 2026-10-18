#!/usr/bin/env python3
"""
workspace_mime_guard.py
Google Workspace Recipient-Domain Context Guard, Draft Stager, and Calendar Conflict Detector.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import base64
import json
import sys
from typing import Any, Dict, List, Tuple


def verify_and_stage_draft(
    sender: str,
    recipients: List[str],
    subject: str,
    body_text: str,
    allowed_client_domains: List[str],
) -> Dict[str, Any]:
    """Verifies recipient domains match client context and encodes a Gmail API draft payload."""
    allowed_set = {d.lower().strip() for d in allowed_client_domains}
    mismatched: List[str] = []
    for addr in recipients:
        if "@" not in addr:
            mismatched.append(addr)
            continue
        domain = addr.split("@", 1)[1].lower().strip()
        if domain not in allowed_set:
            mismatched.append(addr)

    lines = [
        f"From: {sender}",
        f"To: {', '.join(recipients)}",
        f"Subject: {subject}",
        "MIME-Version: 1.0",
        "Content-Type: text/plain; charset=utf-8",
        "",
        body_text,
    ]
    raw_mime = "\r\n".join(lines)
    b64_url = base64.urlsafe_b64encode(raw_mime.encode("utf-8")).decode("ascii")
    return {
        "action": "users.drafts.create",
        "direct_send_blocked": True,
        "domain_check_passed": len(mismatched) == 0,
        "mismatched_recipients": mismatched,
        "draft_payload": {"message": {"raw": b64_url}} if len(mismatched) == 0 else None,
    }


def check_calendar_conflicts(
    proposed_start_min: int,
    proposed_end_min: int,
    busy_Windows: List[Tuple[int, int]],
    buffer_min: int = 15,
) -> Dict[str, Any]:
    """Checks whether a proposed meeting window conflicts with busy intervals plus buffer."""
    eff_start = proposed_start_min - buffer_min
    eff_end = proposed_end_min + buffer_min
    conflicts = []
    for b_start, b_end in busy_Windows:
        if eff_start < b_end and eff_end > b_start:
            conflicts.append({"busy_start": b_start, "busy_end": b_end})
    return {
        "slot_available": len(conflicts) == 0,
        "buffer_minutes": buffer_min,
        "conflicts": conflicts,
    }


def run_selftest() -> int:
    ok_draft = verify_and_stage_draft(
        sender="andrew@aria.net",
        recipients=["ops@m1concourse.com"],
        subject="Phase 2 Track Mesh Review",
        body_text="Attached is the 60GHz link budget review.",
        allowed_client_domains=["m1concourse.com", "aria.net"],
    )
    assert ok_draft["domain_check_passed"] is True and ok_draft["direct_send_blocked"] is True

    bad_draft = verify_and_stage_draft(
        sender="andrew@aria.net",
        recipients=["ops@m1concourse.com", "wrong@otherclient.com"],
        subject="Phase 2 Track Mesh Review",
        body_text="Attached is the 60GHz link budget review.",
        allowed_client_domains=["m1concourse.com"],
    )
    assert bad_draft["domain_check_passed"] is False and "wrong@otherclient.com" in bad_draft["mismatched_recipients"]

    cal = check_calendar_conflicts(600, 660, busy_Windows=[(540, 590), (680, 720)], buffer_min=15)
    assert cal["slot_available"] is False, "590 busy end + 15m buffer overlaps 600 start"
    print("[PASS] workspace_mime_guard.py --selftest: all assertions passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Google Workspace Outbound Draft Guard & Calendar Verifier")
    parser.add_argument("--selftest", action="store_true", help="Run deterministic self-test")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()
    print(json.dumps({"status": "ready", "tool": "workspace_mime_guard.py"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
