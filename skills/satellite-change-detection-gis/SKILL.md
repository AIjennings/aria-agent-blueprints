---
name: satellite-change-detection-gis
description: Geospatial slippy-map XYZ tile calculator, Ground Sample Distance (GSD) resolution verifier, and multi-epoch property/roof footprint change analyzer.
version: 1.0.0
author: Aria Technology Group
---

# Satellite & Historical Aerial Change-Detection Pipeline

## Overview
Production reference pattern engineered by **Aria Technology Group** for acquiring multi-epoch satellite and historical aerial imagery (Planet SkySat, USGS, Wayback) to audit commercial roofing footprints, campus infrastructure, and shoreline/property boundary changes.

## Geospatial Math
1. **Web Mercator (`EPSG:3857`) XYZ Tile Coordinate Conversion:** Converts WGS84 `(lat, lon, zoom)` coordinates into exact slippy-map `(x, y, z)` tile indices.
2. **Ground Sample Distance (`GSD`) Calculation:** Computes exact meters-per-pixel resolution at a given latitude and zoom level: `GSD = (156543.03392 * cos(lat)) / (2^zoom)`.
3. **Impervious / Roof Footprint Delta Analysis:** Compares multi-year polygon areas in square feet to flag unpermitted structural additions or shoreline erosion.

## CLI Usage
```bash
python geospatial_tile_calc.py --selftest
```
