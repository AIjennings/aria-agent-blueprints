#!/usr/bin/env python3
"""
twenty_crm_shim.py
Deterministic Twenty CRM MRR/TCV Quote Synchronizer, Fixture Guard, and Support Ticket PII Masker.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from typing import Any, Dict, List

BLOCKED_TAGS = {"TEST-FIXTURE", "DO-NOT-SYNC", "INTERNAL-SANDBOX"}


def calculate_quote_metrics(line_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """ Computes one-time total, MRR, and TCV from term-encoded line items."""
    one_time_total = 0.0
    mrr_total = 0.0
    recurring_tcv = 0.0
    max_term_months = 0

    for item in line_items:
        billing_type = str(item.get("billing_type", "one_time")).lower()
        unit_price = float(item.get("unit_price", 0.0))
        qty = int(item.get("quantity", 1))
        if billing_type == "monthly":
            # In Aria quoting convention, qty on monthly items encodes term in months
            mrr_total += unit_price
            recurring_tcv += unit_price * qty
            if qty > max_term_months:
                max_term_months = qty
        else:
            one_time_total += unit_price * qty

    tcv = round(one_time_total + recurring_tcv, 2)
    return {
        "one_time_usd": round(one_time_total, 2),
        "mrr_usd": round(mrr_total, 2),
        "recurring_tcv_usd": round(recurring_tcv, 2),
        "tcv_usd": tcv,
        "amount_micros": int(round(tcv * 1_000_000)),
        "term_months": max_term_months,
    }


def mask_ticket_pii(ticket: Dict[str, Any]) -> Dict[str, Any]:
    """Masks phone numbers and email addresses in support ticket summaries for external LLM shims."""
    raw_text = str(ticket.get("description", ""))
    masked_phone = re.sub(r"(\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?)\d{3}([-.\s]?\d{4})", r"\1***\2", raw_text)
    masked_both = re.sub(r"([a-zA-Z0-9_.+-]{2})[a-zA-Z0-9_.+-]*(@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", r"\1***\2", masked_phone)
    tags = {str(t).upper() for t in ticket.get("tags", [])}
    blocked = bool(tags & BLOCKED_TAGS)
    return {
        "ticket_id": ticket.get("id", "UNKNOWN"),
        "subject": ticket.get("subject", ""),
        "masked_description": masked_both,
        "sync_allowed": not blocked,
        "blocked_reason": "Tag guard triggered" if blocked else None,
    }


def run_selftest() -> int:
    items = [
        {"name": "Siklu MultiHaul Base + Installation", "billing_type": "one_time", "unit_price": 8500.0, "quantity": 1},
        {"name": "Managed 60GHz Mesh & Agent Monitoring", "billing_type": "monthly", "unit_price": 1500.0, "quantity": 12},
    ]
    metrics = calculate_quote_metrics(items)
    assert metrics["one_time_usd"] == 8500.0, f"Expected 8500, got {metrics['one_time_usd']}"
    assert metrics["mrr_usd"] == 1500.0, f"Expected 1500 MRR, got {metrics['mrr_usd']}"
    assert metrics["tcv_usd"] == 26500.0, f"Expected 26500 TCV, got {metrics['tcv_usd']}"

    ticket = {
        "id": "TCK-2049",
        "subject": "Gate Reader Offline",
        "description": "Contact ops lead at 248-555-0199 or ops.lead@example.com immediately.",
        "tags": ["TEST-FIXTURE"],
    }
    masked = mask_ticket_pii(ticket)
    assert "555" not in masked["masked_description"], "Phone middle digits must be masked"
    assert masked["sync_allowed"] is False, "TEST-FIXTURE must block sync"
    print("[PASS] twenty_crm_shim.py --selftest: all assertions passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Twenty CRM MRR/TCV Quote Synchronizer & PII Masker")
    parser.add_argument("--selftest", action="store_true", help="Run deterministic self-test")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()
    print(json.dumps({"status": "ready", "tool": "twenty_crm_shim.py"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
