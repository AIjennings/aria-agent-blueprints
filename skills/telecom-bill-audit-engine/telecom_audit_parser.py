#!/usr/bin/env python3
"""
telecom_audit_parser.py
Deterministic Carrier Invoice Surcharge Auditor, ETF Buyout ROI Calculator, and Porting LOA Manifest Generator.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class CarrierLineItem:
    btn: str
    description: str
    category: str  # "seat" | "circuit" | "discretionary_surcharge" | "statutory_tax"
    monthly_charge_usd: float
    active_30d_usage: bool = True


@dataclass
class TelecomAuditReport:
    current_monthly_spend_usd: float
    flagged_waste_monthly_usd: float
    projected_monthly_spend_usd: float
    monthly_savings_usd: float
    annual_savings_usd: float
    savings_pct: float
    etf_penalty_usd: float
    partner_buyout_credit_usd: float
    net_migration_payback_months: float
    loa_porting_manifest: Dict[str, Any]


def audit_carrier_account(
    account_name: str,
    service_address: str,
    lines: List[CarrierLineItem],
    remaining_contract_months: int,
    etf_per_month_usd: float,
    proposed_per_seat_usd: float = 24.99,
    partner_buyout_cap_usd: float = 5000.0,
) -> TelecomAuditReport:
    current_total = sum(x.monthly_charge_usd for x in lines)
    flagged_waste = 0.0
    active_seats = 0
    porting_btns = sorted({x.btn for x in lines if x.btn})

    for item in lines:
        if item.category == "discretionary_surcharge":
            flagged_waste += item.monthly_charge_usd
        elif not item.active_30d_usage:
            flagged_waste += item.monthly_charge_usd
        elif item.category == "seat":
            active_seats += 1

    circuits_and_tax = sum(
        x.monthly_charge_usd
        for x in lines
        if x.category in ("circuit", "statutory_tax") and x.active_30d_usage
    )
    projected_spend = (active_seats * proposed_per_seat_usd) + circuits_and_tax
    monthly_savings = max(0.0, current_total - projected_spend)
    annual_savings = monthly_savings * 12.0
    savings_pct = (monthly_savings / current_total * 100.0) if current_total > 0 else 0.0

    etf_total = max(0, remaining_contract_months) * etf_per_month_usd
    buyout_credit = min(etf_total, partner_buyout_cap_usd)
    net_etf = max(0.0, etf_total - buyout_credit)
    payback_months = (net_etf / monthly_savings) if monthly_savings > 0 else 0.0

    loa_manifest = {
        "customer_legal_name": account_name,
        "service_location": service_address,
        "billing_telephone_numbers": porting_btns,
        "active_seats_to_port": active_seats,
        "requires_authorized_signature": True,
        "status": "DRAFT_READY_FOR_CLIENT_REVIEW",
    }

    return TelecomAuditReport(
        current_monthly_spend_usd=round(current_total, 2),
        flagged_waste_monthly_usd=round(flagged_waste, 2),
        projected_monthly_spend_usd=round(projected_spend, 2),
        monthly_savings_usd=round(monthly_savings, 2),
        annual_savings_usd=round(annual_savings, 2),
        savings_pct=round(savings_pct, 1),
        etf_penalty_usd=round(etf_total, 2),
        partner_buyout_credit_usd=round(buyout_credit, 2),
        net_migration_payback_months=round(payback_months, 2),
        loa_porting_manifest=loa_manifest,
    )


def run_selftest() -> None:
    sample_lines = [
        CarrierLineItem("248-555-0100", "Legacy UCaaS Seat Bundle (40 Active Seats)", "seat", 1680.00, True),
        CarrierLineItem("248-555-0199", "Unassigned Ghost DIDs & Idle Fax Lines (12 Seats)", "seat", 504.00, False),
        CarrierLineItem("248-555-0100", "Carrier Administrative Cost Recovery Fee", "discretionary_surcharge", 198.40, True),
        CarrierLineItem("248-555-0100", "Dedicated Fiber DIA 1Gbps", "circuit", 650.00, True),
        CarrierLineItem("248-555-0100", "E911 & Statutory Telecom Taxes", "statutory_tax", 112.50, True),
    ]
    # 40 active seats expanded via list comprehension for accurate seat count
    expanded = [
        CarrierLineItem(f"248-555-01{i:02d}", "Active Voice Seat", "seat", 42.00, True)
        for i in range(40)
    ] + sample_lines[1:]

    report = audit_carrier_account(
        account_name="Midwest Fleet Logistics LLC",
        service_address="100 Industrial Pkwy, Detroit, MI",
        lines=expanded,
        remaining_contract_months=8,
        etf_per_month_usd=250.0,
    )
    assert 15.0 <= report.savings_pct <= 45.0, f"Unexpected savings_pct: {report.savings_pct}"
    assert report.loa_porting_manifest["requires_authorized_signature"] is True
    print(json.dumps({"selftest": "PASS", "report": asdict(report)}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Telecom Bill Audit & Carrier Buyout Reference Engine")
    parser.add_argument("--selftest", action="store_true", help="Run deterministic audit self-test")
    args = parser.parse_args()
    run_selftest()
