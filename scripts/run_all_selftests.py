#!/usr/bin/env python3
"""
run_all_selftests.py
Runs the deterministic --selftest verification suite across all 20 Aria production reference blueprints.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

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
    "skills/twenty-crm-muse-connector/twenty_crm_shim.py",
    "skills/elevenlabs-voice-telephony-bridge/elevenlabs_tool_verifier.py",
    "skills/m1-motorsport-waiver-kiosk/waiver_qr_verifier.py",
    "skills/google-workspace-sovereign-bridge/workspace_mime_guard.py",
    "skills/live-motorsport-timing-extractor/motorsport_timing_analyzer.py",
    "skills/govcon-sam-rfp-compliance/sam_rfp_matrix.py",
    "skills/mcp-security-governance-scanner/mcp_schema_auditor.py",
    "skills/gcp-wif-keyless-auth-guard/wif_token_auditor.py",
    "skills/aviation-weather-go-nogo/metar_risk_scorer.py",
    "skills/invoice-qbo-time-reconciler/billing_reconciler.py",
    "skills/satellite-change-detection-gis/geospatial_tile_calc.py",
    "skills/php2shell-vulnerability-scanner/php2shell_scanner.py",
    "skills/compliance-stack-hardening/compliance_compose_auditor.py",
    "skills/metacognition-engine/metacognition_auditor.py",
]


def main() -> int:
    failed = 0
    for rel in SCRIPTS:
        script_path = ROOT / rel
        proc = subprocess.run([sys.executable, str(script_path), "--selftest"], capture_output=True, text=True)
        if proc.returncode == 0:
            print(f"[PASS] {rel}")
        else:
            print(f"[FAIL] {rel}: {proc.stderr or proc.stdout}")
            failed += 1
    print(f"\nSummary: {len(SCRIPTS) - failed}/{len(SCRIPTS)} reference tools passed self-test.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
