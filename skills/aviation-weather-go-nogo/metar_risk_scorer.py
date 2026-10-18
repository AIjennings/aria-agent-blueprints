#!/usr/bin/env python3
"""
metar_risk_scorer.py
Deterministic FAA Flight Category Classifier, Runway Crosswind Vector Calculator, and Density Altitude Engine.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
import math
import sys
from typing import Any, Dict


def classify_flight_category(ceiling_agl_ft: int, visibility_sm: float) -> str:
    """Classifies weather into FAA VFR / MVFR / IFR / LIFR categories."""
    if ceiling_agl_ft < 500 or visibility_sm < 1.0:
        return "LIFR"
    if ceiling_agl_ft < 1000 or visibility_sm < 3.0:
        return "IFR"
    if ceiling_agl_ft <= 3000 or visibility_sm <= 5.0:
        return "MVFR"
    return "VFR"


def evaluate_runway_winds(
    field_elev_ft: int,
    altimeter_inhg: float,
    OAT_celsius: float,
    wind_dir_deg: int,
    wind_speed_kt: int,
    runway_heading_deg: int,
    max_crosswind_kt: float = 15.0,
) -> Dict[str, Any]:
    """Computes headwind/crosswind components and density altitude."""
    angle_rad = math.radians(abs(wind_dir_deg - runway_heading_deg) % 360)
    crosswind_kt = abs(wind_speed_kt * math.sin(angle_rad))
    headwind_kt = wind_speed_kt * math.cos(angle_rad)
    pressure_alt_ft = field_elev_ft + (29.92 - altimeter_inhg) * 1000.0
    isa_temp_c = 15.0 - (1.98 * (field_elev_ft / 1000.0))
    density_alt_ft = pressure_alt_ft + (120.0 * (OAT_celsius - isa_temp_c))
    return {
        "crosswind_kt": round(crosswind_kt, 1),
        "headwind_kt": round(headwind_kt, 1),
        "density_altitude_ft": int(round(density_alt_ft)),
        "within_crosswind_limit": crosswind_kt <= max_crosswind_kt,
    }


def run_selftest() -> int:
    assert classify_flight_category(ceiling_agl_ft=4500, visibility_sm=10.0) == "VFR"
    assert classify_flight_category(ceiling_agl_ft=2200, visibility_sm=6.0) == "MVFR"
    assert classify_flight_category(ceiling_agl_ft=800, visibility_sm=2.5) == "IFR"
    assert classify_flight_category(ceiling_agl_ft=400, visibility_sm=0.5) == "LIFR"

    winds = evaluate_runway_winds(
        field_elev_ft=980,
        altimeter_inhg=29.82,
        OAT_celsius=28.0,
        wind_dir_deg=240,
        wind_speed_kt=20,
        runway_heading_deg=270,
        max_crosswind_kt=15.0,
    )
    # 30 deg off runway -> sin(30) = 0.5 -> 10.0 kt crosswind
    assert math.isclose(winds["crosswind_kt"], 10.0, abs_tol=0.1)
    assert winds["within_crosswind_limit"] is True
    assert winds["density_altitude_ft"] > 2500
    print("[PASS] metar_risk_scorer.py --selftest: all assertions passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Aviation METAR Flight Category & Crosswind Risk Scorer")
    parser.add_argument("--selftest", action="store_true", help="Run deterministic self-test")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()
    print(json.dumps({"status": "ready", "tool": "metar_risk_scorer.py"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
