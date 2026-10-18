#!/usr/bin/env python3
"""
motorsport_timing_analyzer.py
Deterministic Motorsport Lap Telemetry Parser, Theoretical Optimal Lap Calculator, and Consistency Scorer.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
import math
import statistics
import sys
from typing import Any, Dict, List


def analyze_stint(laps: List[Dict[str, float]]) -> Dict[str, Any]:
    """Analyzes a stint of sector times (s1, s2, s3 in seconds), filtering caution/pit laps."""
    totals = [round(l["s1"] + l["s2"] + l["s3"], 3) for l in laps]
    median_lap = statistics.median(totals)
    flying_laps = [l for l, t in zip(laps, totals) if t <= median_lap * 1.15]
    flying_totals = [round(l["s1"] + l["s2"] + l["s3"], 3) for l in flying_laps]

    best_actual = min(flying_totals)
    purple_s1 = min(l["s1"] for l in flying_laps)
    purple_s2 = min(l["s2"] for l in flying_laps)
    purple_s3 = min(l["s3"] for l in flying_laps)
    theoretical_best = round(purple_s1 + purple_s2 + purple_s3, 3)
    std_dev_sec = statistics.pstdev(flying_totals) if len(flying_totals) > 1 else 0.0

    return {
        "total_laps": len(laps),
        "flying_laps_counted": len(flying_laps),
        "filtered_pit_or_yellow_laps": len(laps) - len(flying_laps),
        "best_lap_sec": best_actual,
        "theoretical_optimal_sec": theoretical_best,
        "potential_gain_sec": round(best_actual - theoretical_best, 3),
        "consistency_std_ms": round(std_dev_sec * 1000.0, 1),
    }


def run_selftest() -> int:
    sample_stint = [
        {"s1": 28.410, "s2": 34.120, "s3": 25.300},  # 87.830
        {"s1": 28.150, "s2": 34.300, "s3": 25.250},  # 87.700
        {"s1": 28.220, "s2": 33.950, "s3": 25.180},  # 87.350 (best actual)
        {"s1": 35.000, "s2": 48.000, "s3": 39.500},  # 122.500 (pit/yellow outlier)
    ]
    res = analyze_stint(sample_stint)
    assert res["flying_laps_counted"] == 3 and res["filtered_pit_or_yellow_laps"] == 1
    assert math.isclose(res["best_lap_sec"], 87.350, abs_tol=1e-3)
    # Purple sectors: 28.150 + 33.950 + 25.180 = 87.280
    assert math.isclose(res["theoretical_optimal_sec"], 87.280, abs_tol=1e-3)
    assert math.isclose(res["potential_gain_sec"], 0.070, abs_tol=1e-3)
    print("[PASS] motorsport_timing_analyzer.py --selftest: all assertions passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Motorsport Lap Telemetry & Purple Sector Analyzer")
    parser.add_argument("--selftest", action="store_true", help="Run deterministic self-test")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()
    print(json.dumps({"status": "ready", "tool": "motorsport_timing_analyzer.py"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
