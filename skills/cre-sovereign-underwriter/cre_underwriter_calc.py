#!/usr/bin/env python3
"""
cre_underwriter_calc.py
Deterministic Commercial Real Estate T-12 NOI, Cap Rate Sensitivity, and DSCR Underwriting Engine.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
from typing import Dict, Any


def underwrite_property(
    gross_potential_rent_usd: float,
    vacancy_rate_pct: float,
    other_income_usd: float,
    operating_expenses_usd: float,
    purchase_price_usd: float,
    annual_debt_service_usd: float,
) -> Dict[str, Any]:
    vacancy_loss = gross_potential_rent_usd * (vacancy_rate_pct / 100.0)
    effective_gross_income = gross_potential_rent_usd - vacancy_loss + other_income_usd
    noi = effective_gross_income - operating_expenses_usd
    going_in_cap_rate_pct = (noi / purchase_price_usd * 100.0) if purchase_price_usd > 0 else 0.0
    dscr = (noi / annual_debt_service_usd) if annual_debt_service_usd > 0 else 0.0

    sensitivity_valuation = {
        f"{cap:.2f}%": round(noi / (cap / 100.0), 2)
        for cap in (6.50, 7.00, 7.50, 8.00, 8.50)
    }
    return {
        "effective_gross_income_usd": round(effective_gross_income, 2),
        "net_operating_income_usd": round(noi, 2),
        "going_in_cap_rate_pct": round(going_in_cap_rate_pct, 2),
        "dscr": round(dscr, 2),
        "lender_dscr_pass_1_25x": dscr >= 1.25,
        "valuation_by_cap_rate_usd": sensitivity_valuation,
    }


def run_selftest() -> None:
    res = underwrite_property(
        gross_potential_rent_usd=640_000.0,
        vacancy_rate_pct=5.0,
        other_income_usd=18_000.0,
        operating_expenses_usd=216_000.0,
        purchase_price_usd=5_250_000.0,
        annual_debt_service_usd=295_000.0,
    )
    assert res["net_operating_income_usd"] == 410_000.0
    assert res["lender_dscr_pass_1_25x"] is True
    print(json.dumps({"selftest": "PASS", "underwriting": res}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CRE Sovereign Underwriter NOI/CapRate/DSCR Engine")
    parser.add_argument("--selftest", action="store_true", help="Run deterministic T-12 underwriting self-test")
    args = parser.parse_args()
    run_selftest()
