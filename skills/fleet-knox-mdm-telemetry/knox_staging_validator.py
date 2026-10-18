#!/usr/bin/env python3
"""
knox_staging_validator.py
Samsung Knox Kiosk Policy Validator & Samsara ELD Telemetry Alert Normalizer.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
from typing import Dict, Any, List

REQUIRED_KNOX_KEYS = {
    "kiosk_mode_enabled": True,
    "usb_debugging_enabled": False,
    "factory_reset_allowed": False,
    "location_mode": "HIGH_ACCURACY",
}


def validate_knox_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    violations: List[str] = []
    for key, expected in REQUIRED_KNOX_KEYS.items():
        actual = profile.get(key)
        if actual != expected:
            violations.append(f"{key}: expected {expected!r}, got {actual!r}")
    allowlist = profile.get("allowed_packages", [])
    if "com.samsara.driver" not in allowlist:
        violations.append("allowed_packages missing required ELD package 'com.samsara.driver'")
    return {
        "compliant": len(violations) == 0,
        "violations": violations,
        "checked_packages": len(allowlist),
    }


def evaluate_eld_telemetry(vehicle_id: str, hos_remaining_mins: int, j1939_mil_on: bool, spn_code: int) -> Dict[str, Any]:
    alerts: List[str] = []
    if hos_remaining_mins < 60:
        alerts.append("HOS_LOW_ROUTE_TO_SAFE_PARKING")
    if j1939_mil_on or spn_code > 0:
        alerts.append(f"MAINTENANCE_FAULT_SPN_{spn_code}")
    return {
        "vehicle_id": vehicle_id,
        "hos_remaining_mins": hos_remaining_mins,
        "dispatch_status": "ACTION_REQUIRED" if alerts else "NORMAL_IN_SERVICE",
        "alerts": alerts,
    }


def run_selftest() -> None:
    good_profile = {
        "profile_name": "BlueWater-TabActive-ZeroTouch-v2",
        "kiosk_mode_enabled": True,
        "usb_debugging_enabled": False,
        "factory_reset_allowed": False,
        "location_mode": "HIGH_ACCURACY",
        "allowed_packages": ["com.samsara.driver", "com.google.android.apps.maps"],
    }
    res = validate_knox_profile(good_profile)
    assert res["compliant"] is True, f"Unexpected violations: {res['violations']}"
    eld = evaluate_eld_telemetry("TRUCK-204", hos_remaining_mins=42, j1939_mil_on=True, spn_code=110)
    assert eld["dispatch_status"] == "ACTION_REQUIRED"
    print(json.dumps({"selftest": "PASS", "knox_validation": res, "eld_event": eld}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Knox MDM Profile & Samsara ELD Validator")
    parser.add_argument("--selftest", action="store_true", help="Run policy and ELD telemetry self-test")
    args = parser.parse_args()
    run_selftest()
