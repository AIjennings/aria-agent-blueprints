---
name: live-motorsport-timing-extractor
description: Motorsport lap-time telemetry parser, purple-sector theoretical best calculator, driver consistency scorer, and yellow-flag outlier filter.
version: 1.0.0
author: Aria Technology Group
---

# Live Motorsport Timing & Telemetry Analyzer

## Overview
Production reference pattern built by **Aria Technology Group** for extracting and analyzing live race-timing feeds (SpeedHive / Mylaps / Assetto Corsa telemetry bridges) for track stewards and driver coaching.

## Capabilities
1. **Theoretical Best Lap (`Optimal Lap`):** Aggregates the fastest individual sector splits (`S1`, `S2`, `S3`) across a session to compute the driver's theoretical optimal lap and potential time gain.
2. **Yellow-Flag / Pit-Lap Outlier Filtering:** Automatically excludes pit-in/pit-out and caution laps exceeding `115%` of the session median pace before calculating consistency metrics.
3. **Driver Consistency Index:** Computes standard deviation in milliseconds across flying laps.

## CLI Usage
```bash
python motorsport_timing_analyzer.py --selftest
```
