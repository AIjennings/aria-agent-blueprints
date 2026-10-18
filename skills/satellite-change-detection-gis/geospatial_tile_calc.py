#!/usr/bin/env python3
"""
geospatial_tile_calc.py
Deterministic Web Mercator XYZ Tile Calculator, GSD Resolution Verifier, and Footprint Delta Analyzer.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
import math
import sys
from typing import Any, Dict


def latlon_to_xyz_tile(lat_deg: float, lon_deg: float, zoom: int) -> Dict[str, Any]:
    """Converts WGS84 latitude/longitude to Web Mercator slippy-map XYZ tile indices and GSD."""
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    gsd_m_per_px = (156543.03392 * math.cos(lat_rad)) / n
    return {
        "zoom": zoom,
        "xtile": xtile,
        "ytile": ytile,
        "gsd_meters_per_pixel": round(gsd_m_per_px, 4),
        "suitable_for_roof_inspection": gsd_m_per_px <= 0.60,
    }


def evaluate_footprint_change(baseline_sqft: float, current_sqft: float, alert_threshold_pct: float = 5.0) -> Dict[str, Any]:
    """Calculates structural or shoreline area delta across multi-year aerial epochs."""
    delta_sqft = current_sqft - baseline_sqft
    delta_pct = (abs(delta_sqft) / baseline_sqft * 100.0) if baseline_sqft > 0 else 0.0
    return {
        "baseline_sqft": round(baseline_sqft, 1),
        "current_sqft": round(current_sqft, 1),
        "delta_sqft": round(delta_sqft, 1),
        "delta_pct": round(delta_pct, 2),
        "significant_change_detected": delta_pct >= alert_threshold_pct,
    }


def run_selftest() -> int:
    # Pontiac / Metro Detroit coordinates (~42.628, -83.275) at Zoom 19
    tile = latlon_to_xyz_tile(42.6280, -83.2750, zoom=19)
    assert tile["zoom"] == 19 and tile["xtile"] > 140000 and tile["ytile"] > 190000
    assert tile["gsd_meters_per_pixel"] < 0.30 and tile["suitable_for_roof_inspection"] is True

    delta = evaluate_footprint_change(baseline_sqft=48000.0, current_sqft=54240.0, alert_threshold_pct=5.0)
    assert delta["delta_pct"] == 13.0 and delta["significant_change_detected"] is True
    print("[PASS] geospatial_tile_calc.py --selftest: all assertions passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Satellite XYZ Tile, GSD & Multi-Epoch Footprint Analyzer")
    parser.add_argument("--selftest", action="store_true", help="Run deterministic self-test")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()
    print(json.dumps({"status": "ready", "tool": "geospatial_tile_calc.py"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
