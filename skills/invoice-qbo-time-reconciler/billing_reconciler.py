#!/usr/bin/env python3
"""
billing_reconciler.py
Deterministic Engineering Time-Log Reconciler & Draft-Only QuickBooks Invoice Builder.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
import sys
from typing import Any, Dict, List


def reconcile_worklog(
    entries: List[Dict[str, Any]],
    hourly_rate_usd: float,
    included_retainer_hours: float = 0.0,
) -> Dict[str, Any]:
    """Reconciles engineering time entries and hardware items into a draft-only QBO invoice payload."""
    billable_hours = 0.0
    non_billable_hours = 0.0
    hardware_subtotal = 0.0

    for entry in entries:
        kind = str(entry.get("kind", "labor")).lower()
        if kind == "hardware":
            hardware_subtotal += float(entry.get("unit_cost", 0.0)) * int(entry.get("qty", 1))
        else:
            hrs = float(entry.get("hours", 0.0))
            if entry.get("billable", True):
                billable_hours += hrs
            else:
                non_billable_hours += hrs

    overage_hours = max(0.0, billable_hours - included_retainer_hours)
    labor_subtotal = round(overage_hours * hourly_rate_usd, 2)
    hardware_subtotal = round(hardware_subtotal, 2)
    total_due = round(labor_subtotal + hardware_subtotal, 2)

    return {
        "invoice_mode": "DRAFT_ONLY",
        "auto_send_email": False,
        "billable_hours": round(billable_hours, 2),
        "non_billable_hours": round(non_billable_hours, 2),
        "retainer_applied_hours": round(min(billable_hours, included_retainer_hours), 2),
        "net_billable_hours": round(overage_hours, 2),
        "labor_service_usd": labor_subtotal,
        "hardware_equipment_usd": hardware_subtotal,
        "total_draft_usd": total_due,
    }


def run_selftest() -> int:
    logs = [
        {"kind": "labor", "ticket": "TCK-101", "hours": 6.5, "billable": True},
        {"kind": "labor", "ticket": "TCK-102", "hours": 4.5, "billable": True},
        {"kind": "labor", "ticket": "INTERNAL-QA", "hours": 2.0, "billable": False},
        {"kind": "hardware", "sku": "MH-T280-cCG", "unit_cost": 1450.0, "qty": 2},
    ]
    res = reconcile_worklog(logs, hourly_rate_usd=185.0, included_retainer_hours=5.0)
    assert res["invoice_mode"] == "DRAFT_ONLY" and res["auto_send_email"] is False
    assert res["billable_hours"] == 11.0 and res["net_billable_hours"] == 6.0
    assert res["labor_service_usd"] == 1110.0 and res["hardware_equipment_usd"] == 2900.0
    assert res["total_draft_usd"] == 4010.0
    print("[PASS] billing_reconciler.py --selftest: all assertions passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Engineering Time & QBO Draft Invoice Reconciler")
    parser.add_argument("--selftest", action="store_true", help="Run deterministic self-test")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()
    print(json.dumps({"status": "ready", "tool": "billing_reconciler.py"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
