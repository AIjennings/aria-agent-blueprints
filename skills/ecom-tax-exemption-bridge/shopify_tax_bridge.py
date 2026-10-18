#!/usr/bin/env python3
"""
shopify_tax_bridge.py
Shopify Webhook HMAC-SHA256 Verifier, Tax-Exemption Discrepancy Detector, and Draft QBO Payload Builder.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import hmac
import json
import re
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

STATE_EIN_PATTERNS = {
    "MI": re.compile(r"^(?:\d{2}-?\d{7}|ME-\d{6,9})$"),
    "OH": re.compile(r"^(?:\d{2}-?\d{7}|OH-EX-\d{6,9})$"),
    "IN": re.compile(r"^(?:\d{2}-?\d{7}|0\d{9})$"),
    "IL": re.compile(r"^(?:E99\d{2}-?\d{4}-?\d{2}|\d{2}-?\d{7})$"),
}


@dataclass
class TaxAuditDecision:
    order_id: str
    customer_Exempt_flag: bool
    certificate_id: str
    state_code: str
    certificate_format_valid: bool
    tax_charged_usd: float
    subtotal_usd: float
    discrepancy_detected: bool
    action: str
    qbo_draft_payload: Dict[str, Any]


def compute_shopify_hmac(raw_body: bytes, secret: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).digest()
    return base64.b64encode(digest).decode("ascii")


def verify_shopify_hmac(raw_body: bytes, header_hmac: str, secret: str) -> bool:
    expected = compute_shopify_hmac(raw_body, secret)
    return hmac.compare_digest(expected, header_hmac.strip())


def evaluate_order_tax(
    order_id: str,
    subtotal_usd: float,
    tax_charged_usd: float,
    customer_exempt: bool,
    state_code: str,
    certificate_id: Optional[str],
) -> TaxAuditDecision:
    cert = (certificate_id or "").strip()
    pattern = STATE_EIN_PATTERNS.get(state_code.upper())
    cert_valid = bool(cert and (pattern.match(cert) if pattern else len(cert) >= 7))

    if customer_exempt and cert_valid and tax_charged_usd > 0.0:
        discrepancy = True
        action = "STAGE_TAX_REFUND_DRAFT_AND_ALERT_OPERATOR"
    elif customer_exempt and not cert_valid:
        discrepancy = True
        action = "HOLD_EXEMPTION_REQUEST_CERTIFICATE_REVIEW"
    else:
        discrepancy = False
        action = "SYNC_CLEAN_DRAFT_INVOICE"

    qbo_draft = {
        "DocNumber": f"SHPFY-{order_id}",
        "EmailStatus": "NotSet",
        "DraftOnly": True,
        "RequiresHumanApproval": True,
        "SubtotalUSD": round(subtotal_usd, 2),
        "TaxChargedUSD": round(tax_charged_usd, 2),
        "RecommendedTaxAdjustmentUSD": round(-tax_charged_usd, 2) if action.startswith("STAGE_TAX_REFUND") else 0.0,
        "ExemptionCertificate": cert or "NONE",
    }

    return TaxAuditDecision(
        order_id=order_id,
        customer_Exempt_flag=customer_exempt,
        certificate_id=cert,
        state_code=state_code.upper(),
        certificate_format_valid=cert_valid,
        tax_charged_usd=round(tax_charged_usd, 2),
        subtotal_usd=round(subtotal_usd, 2),
        discrepancy_detected=discrepancy,
        action=action,
        qbo_draft_payload=qbo_draft,
    )


def run_selftest() -> None:
    body = b'{"id":589102,"subtotal_price":"1450.00","total_tax":"87.00"}'
    secret = "test_webhook_secret_only"
    sig = compute_shopify_hmac(body, secret)
    assert verify_shopify_hmac(body, sig, secret) is True
    assert verify_shopify_hmac(body, "invalid_sig", secret) is False

    decision = evaluate_order_tax(
        order_id="589102",
        subtotal_usd=1450.00,
        tax_charged_usd=87.00,
        customer_exempt=True,
        state_code="MI",
        certificate_id="38-2910482",
    )
    assert decision.discrepancy_detected is True
    assert decision.qbo_draft_payload["DraftOnly"] is True
    print(json.dumps({
        "selftest": "PASS",
        "hmac_verified": True,
        "sample_audit": asdict(decision),
    }, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shopify Tax Exemption Bridge Reference Verifier")
    parser.add_argument("--selftest", action="store_true", help="Run HMAC and tax discrepancy self-test")
    args = parser.parse_args()
    run_selftest()
