#!/usr/bin/env python3
"""
sam_rfp_matrix.py
Deterministic GovCon SAM.gov 13 CFR 125.6 Set-Aside Calculator & Section L/M Compliance Matrix Builder.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from typing import Any, Dict, List

HIGH_RISK_CLAUSES = {
    "252.204-7012": "DFARS Safeguarding Covered Defense Information (NIST SP 800-171)",
    "252.204-7021": "CMMC Cybersecurity Maturity Model Certification Requirement",
    "52.211-11": "FAR Liquidated Damages - Supplies, Services, or Research",
    "52.222-41": "FAR Service Contract Labor Standards (SCA Wage Determination)",
}


def evaluate_set_aside_compliance(
    total_contract_price: float,
    prime_cost_share: float,
    similarly_situated_sub_share: float,
    non_similarly_situated_sub_share: float,
) -> Dict[str, Any]:
    """Evaluates 13 CFR 125.6 Limitation on Subcontracting (<= 50% to non-similarly situated firms for services)."""
    non_sim_ratio = non_similarly_situated_sub_share / total_contract_price if total_contract_price > 0 else 1.0
    qualifying_share = prime_cost_share + similarly_situated_sub_share
    compliant = non_sim_ratio <= 0.50
    return {
        "total_contract_usd": round(total_contract_price, 2),
        "qualifying_small_business_usd": round(qualifying_share, 2),
        "non_similarly_situated_pct": round(non_sim_ratio * 100.0, 2),
        "compliant_13_cfr_125_6": compliant,
    }


def extract_compliance_matrix(solicitation_text: str) -> Dict[str, Any]:
    """Extracts mandatory 'shall'/'must' statements and flags high-risk FAR/DFARS clauses."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", solicitation_text) if s.strip()]
    requirements = []
    for idx, sent in enumerate(sentences, start=1):
        if re.search(r"\b(shall|must)\b", sent, flags=re.IGNORECASE):
            requirements.append({"req_id": f"REQ-{idx:03d}", "statement": sent, "status": "NEEDS_MAPPING"})

    detected_clauses = []
    for code, desc in HIGH_RISK_CLAUSES.items():
        if code in solicitation_text:
            detected_clauses.append({"clause": code, "description": desc})

    return {
        "mandatory_requirement_count": len(requirements),
        "requirements": requirements,
        "high_risk_clauses": detected_clauses,
    }


def run_selftest() -> int:
    los = evaluate_set_aside_compliance(250000.0, prime_cost_share=110000.0, similarly_situated_sub_share=35000.0, non_similarly_situated_sub_share=105000.0)
    assert los["compliant_13_cfr_125_6"] is True and los["non_similarly_situated_pct"] == 42.0

    rfp_sample = (
        "The Offeror shall provide 24/7 network monitoring under DFARS 252.204-7012. "
        "All field engineers must hold active security clearances. "
        "Evaluation will consider past performance under FAR 52.211-11."
    )
    matrix = extract_compliance_matrix(rfp_sample)
    assert matrix["mandatory_requirement_count"] == 2
    assert len(matrix["high_risk_clauses"]) == 2
    print("[PASS] sam_rfp_matrix.py --selftest: all assertions passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="GovCon SAM.gov Set-Aside & RFP Compliance Matrix Tool")
    parser.add_argument("--selftest", action="store_true", help="Run deterministic self-test")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()
    print(json.dumps({"status": "ready", "tool": "sam_rfp_matrix.py"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
