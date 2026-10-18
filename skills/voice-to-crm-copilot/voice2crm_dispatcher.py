#!/usr/bin/env python3
"""
voice2crm_dispatcher.py
Deterministic Transcript-to-CRM Deal Calculator (MRR/TCV) and Human-Gated Draft Dispatcher.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class QuoteLine:
    description: str
    billing_type: str  # "one_time" | "monthly_recurring"
    unit_rate_usd: float
    quantity_or_months: int


def build_crm_opportunity_draft(
    account_name: str,
    contact_email: str,
    next_step: str,
    lines: List[QuoteLine],
) -> Dict[str, Any]:
    one_time_usd = sum(x.unit_rate_usd * x.quantity_or_months for x in lines if x.billing_type == "one_time")
    mrr_usd = sum(x.unit_rate_usd for x in lines if x.billing_type == "monthly_recurring")
    recurring_total_usd = sum(
        x.unit_rate_usd * x.quantity_or_months for x in lines if x.billing_type == "monthly_recurring"
    )
    tcv_usd = one_time_usd + recurring_total_usd

    return {
        "opportunity_name": f"{account_name} - Sovereign AI & Infrastructure Deployment",
        "contact_email": contact_email,
        "stage": "PROPOSAL_STAGED",
        "next_step": next_step,
        "metrics": {
            "one_time_usd": round(one_time_usd, 2),
            "mrr_usd": round(mrr_usd, 2),
            "tcv_usd": round(tcv_usd, 2),
        },
        "outbound_email_draft": {
            "to": contact_email,
            "subject": f"Next Steps & Architecture Scope — {account_name}",
            "send_immediately": False,
            "requires_human_approval": True,
        },
    }


def run_selftest() -> None:
    lines = [
        QuoteLine("Siklu 60GHz Mesh & Camera Turnkey Installation", "one_time", 8500.0, 1),
        QuoteLine("Managed AI Voice & Sovereign CRM Retainer (12-Month Term)", "monthly_recurring", 1500.0, 12),
    ]
    draft = build_crm_opportunity_draft(
        account_name="Great Lakes Motorsport Campus",
        contact_email="ops@example.com",
        next_step="Review 3D KML line-of-sight model on Friday at 2:00 PM ET",
        lines=lines,
    )
    assert draft["metrics"]["mrr_usd"] == 1500.0
    assert draft["metrics"]["tcv_usd"] == 26500.0
    assert draft["outbound_email_draft"]["requires_human_approval"] is True
    print(json.dumps({"selftest": "PASS", "crm_draft": draft}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Voice-to-CRM Deal & TCV Draft Dispatcher")
    parser.add_argument("--selftest", action="store_true", help="Run MRR/TCV and approval-gate self-test")
    args = parser.parse_args()
    run_selftest()
