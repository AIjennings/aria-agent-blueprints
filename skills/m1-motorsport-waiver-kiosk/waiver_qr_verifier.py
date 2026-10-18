#!/usr/bin/env python3
"""
waiver_qr_verifier.py
Deterministic HMAC-SHA256 Track Gate Waiver QR Pass Generator and Offline Scanner Verifier.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import hashlib
import hmac
import json
import sys
from typing import Any, Dict


def issue_waiver_qr_token(
    participant_id: str,
    event_code: str,
    issued_epoch: int,
    ttl_seconds: int,
    signing_secret: str,
) -> Dict[str, Any]:
    """Generates a signed QR payload for a completed motorsport track waiver."""
    expires_epoch = issued_epoch + ttl_seconds
    canonical = f"{event_code}|{participant_id}|{issued_epoch}|{expires_epoch}"
    sig = hmac.new(signing_secret.encode("utf-8"), canonical.encode("utf-8"), hashlib.sha256).hexdigest()[:24]
    token = f"{canonical}|{sig}"
    return {
        "event_code": event_code,
        "participant_id": participant_id,
        "expires_epoch": expires_epoch,
        "qr_token": token,
        "signature": sig,
    }


def verify_waiver_qr_token(qr_token: str, current_epoch: int, expected_event: str, signing_secret: str) -> Dict[str, Any]:
    """Verifies a scanned gate pass token in constant time and checks event/time validity."""
    parts = qr_token.split("|")
    if len(parts) != 5:
        return {"valid": False, "reason": "MALFORMED_TOKEN"}
    event_code, participant_id, issued_str, expires_str, provided_sig = parts
    canonical = f"{event_code}|{participant_id}|{issued_str}|{expires_str}"
    expected_sig = hmac.new(signing_secret.encode("utf-8"), canonical.encode("utf-8"), hashlib.sha256).hexdigest()[:24]

    if not hmac.compare_digest(provided_sig, expected_sig):
        return {"valid": False, "reason": "INVALID_SIGNATURE"}
    if event_code != expected_event:
        return {"valid": False, "reason": "WRONG_EVENT_CODE"}
    if current_epoch > int(expires_str):
        return {"valid": False, "reason": "PASS_EXPIRED"}
    return {
        "valid": True,
        "gate_action": "OPEN_LANE_GREEN",
        "participant_id": participant_id,
        "event_code": event_code,
    }


def run_selftest() -> int:
    secret = "m1-track-gate-test-secret-2026"
    issued = issue_waiver_qr_token("DRV-9081", "M1-TRACKDAY-OCT", issued_epoch=1760000000, ttl_seconds=43200, signing_secret=secret)
    good = verify_waiver_qr_token(issued["qr_token"], current_epoch=1760003600, expected_event="M1-TRACKDAY-OCT", signing_secret=secret)
    assert good["valid"] is True and good["gate_action"] == "OPEN_LANE_GREEN"

    expired = verify_waiver_qr_token(issued["qr_token"], current_epoch=1760099999, expected_event="M1-TRACKDAY-OCT", signing_secret=secret)
    assert expired["valid"] is False and expired["reason"] == "PASS_EXPIRED"

    tampered = issued["qr_token"].replace("DRV-9081", "DRV-9999")
    bad_sig = verify_waiver_qr_token(tampered, current_epoch=1760003600, expected_event="M1-TRACKDAY-OCT", signing_secret=secret)
    assert bad_sig["valid"] is False and bad_sig["reason"] == "INVALID_SIGNATURE"
    print("[PASS] waiver_qr_verifier.py --selftest: all assertions passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="M1 Motorsport Waiver QR Token Generator & Gate Verifier")
    parser.add_argument("--selftest", action="store_true", help="Run deterministic self-test")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()
    print(json.dumps({"status": "ready", "tool": "waiver_qr_verifier.py"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
