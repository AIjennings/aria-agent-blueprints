---
name: aviation-weather-go-nogo
description: Deterministic NOAA METAR/TAF flight category classifier (VFR/MVFR/IFR/LIFR), runway crosswind component calculator, density altitude engine, and Go/No-Go risk scorer.
version: 1.0.0
author: Aria Technology Group
---

# General Aviation Weather Briefing & Go/No-Go Risk Engine

## Overview
Production reference pattern operated by **Aria Technology Group** for general aviation pre-flight weather briefings, combining live NOAA Aviation Weather Center (AWC) METAR/TAF telemetry with deterministic aerodynamic & personal-minimums math.

## Deterministic Calculations
1. **FAA Flight Category Classification:** Classifies ceiling (feet AGL) and visibility (statute miles) into `VFR`, `MVFR`, `IFR`, or `LIFR`.
2. **Runway Crosswind & Headwind Vector Decomposition:** Calculates exact crosswind and headwind components in knots using `wind_speed * sin(|wind_dir - runway_heading|)`.
3. **Density Altitude Approximation:** Computes pressure altitude and temperature-corrected density altitude for takeoff performance planning.

## CLI Usage
```bash
python metar_risk_scorer.py --selftest
```
