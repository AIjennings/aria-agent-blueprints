#!/usr/bin/env python3
"""
run_all_selftests.py
Runs the deterministic --selftest verification suite across all 8 Aria production reference blueprints.
"""
from __future__ import annotations
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCRIPTS = [
    "skills/mmwave-vision-mesh-planner/mmwave_network_planner.py",
    "skills/siklu-multihaultg-mesh-ops/siklu_ipv6_bridge.py",
    "skills/hid-access-control-provisioning/wiegand_badge_analyzer.py",
    "skills/ecom-tax-exemption-bridge/shopify_tax_bridge.py",
    "skills/telecom-bill-audit-engine/telecom_audit_parser.py",
    "skills/fleet-knox-mdm-telemetry/knox_staging_validator.py",
    "skills/multi-agent-gateway-watchdog/gateway_health_watchdog.py",
    "skills/voice-to-crm-copilot/voice2crm_dispatcher.py",
    "skills/cre-sovereign-underwriter/cre_underwriter_calc.py",
]


def main() -> int:
    passed = 0
    for rel in SCRIPTS:
        full = os.path.join(ROOT, rel)
        proc = subprocess.run([sys.executable, full, "--selftest"], capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"[FAIL] {rel}:\n{proc.stderr}\n{proc.stdout}", file=sys.stderr)
            return 1
        print(f"[PASS] {rel}")
        passed += 1
    print(f"\nAll {passed}/{len(SCRIPTS)} reference blueprint self-tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
