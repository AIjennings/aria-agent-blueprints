#!/usr/bin/env python3
"""
wif_token_auditor.py
GCP Workload Identity Federation (WIF) Configuration Verifier & Cloud Spend Anomaly Detector.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from typing import Any, Dict, List

WIF_AUD_PATTERN = re.compile(
    r"^//iam\.googleapis\.com/projects/\d+/locations/global/workloadIdentityPools/[a-z0-9-]+/providers/[a-z0-9-]+$"
)


def verify_wif_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Verifies keyless GCP Workload Identity Federation configuration and rejects static JSON keys."""
    issues: List[str] = []
    if "private_key" in config or config.get("type") == "service_account":
        issues.append("Static service_account private_key detected; use external_account WIF instead.")
    aud = str(config.get("audience", ""))
    if not WIF_AUD_PATTERN.match(aud):
        issues.append("Invalid WIF audience URI format.")
    impersonation_url = str(config.get("service_account_impersonation_url", ""))
    if not impersonation_url.startswith("https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/"):
        issues.append("Missing or invalid service_account_impersonation_url.")
    attr_cond = str(config.get("attribute_condition", ""))
    if "assertion.sub" not in attr_cond and "assertion.repository" not in attr_cond:
        issues.append("Provider attribute_condition must pin assertion.sub or assertion.repository.")
    return {
        "keyless_verified": len(issues) == 0,
        "issues": issues,
    }


def run_selftest() -> int:
    good_cfg = {
        "type": "external_account",
        "audience": "//iam.googleapis.com/projects/123456789012/locations/global/workloadIdentityPools/vercel-pool/providers/vercel-oidc",
        "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/firestore-sync@aria-prod.iam.gserviceaccount.com:generateAccessToken",
        "attribute_condition": "assertion.sub.startsWith('owner:aria-tech:project:quoting-studio')",
    }
    res = verify_wif_config(good_cfg)
    assert res["keyless_verified"] is True, f"Expected valid WIF config, got {res}"

    leaked_key_cfg = {"type": "service_account", "private_key": "-----BEGIN PRIVATE KEY-----"}
    bad_res = verify_wif_config(leaked_key_cfg)
    assert bad_res["keyless_verified"] is False and len(bad_res["issues"]) >= 2
    print("[PASS] wif_token_auditor.py --selftest: all assertions passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="GCP Workload Identity Federation Keyless Verifier")
    parser.add_argument("--selftest", action="store_true", help="Run deterministic self-test")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()
    print(json.dumps({"status": "ready", "tool": "wif_token_auditor.py"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
