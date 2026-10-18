---
name: mmwave-vision-mesh-planner
description: Standard operating procedure, KML 3D geospatial modeling, camera Field of View (FOV) / EN 62676-4 DORI calculation, and 60GHz Siklu MultiHaul TG RF Fresnel zone link-budget verification for high-speed motorsport venues and commercial campuses.
version: 1.0.0
author: Aria Technology Group
metadata:
  hermes:
    tags: [rf-planning, mmwave, siklu, google-earth, kml, camera-dori, gis]
---

# 60GHz Millimeter-Wave Mesh & 3D Camera FOV Planner

Use this skill when designing outdoor multi-gigabit wireless backhaul (Siklu MultiHaul TG 60GHz Terragraph / 5GHz backup) and optical camera coverage across racetracks, industrial yards, and multi-building campuses.

## 1. RF Link Budget & Fresnel Clearance Model

At 60 GHz (V-band, Channels 1–4: 58.32 GHz to 64.80 GHz), two physical properties govern link reliability:

1. **1st Fresnel Zone Radius ($r_1$):**
   $$r_1 = 8.657 \times \sqrt{\frac{d_{\text{km}}}{f_{\text{GHz}}}} \text{ (meters)}$$
   At 60 GHz over a 300 m (0.3 km) link, $r_1 = 0.61\text{ m (2.0 ft)}$. This narrow beam clears grandstands, light poles, and fences without multipath interference when 60%+ of $r_1$ is unobstructed.
2. **Free Space Path Loss (FSPL) + Atmospheric Absorption:**
   - $\text{FSPL (dB)} = 92.45 + 20\log_{10}(d_{\text{km}}) + 20\log_{10}(f_{\text{GHz}})$
   - Oxygen ($\text{O}_2$) resonance absorption at 60 GHz adds $\approx 15\text{ dB/km}$, plus rain fade margin based on ITU-R P.838.

## 2. Camera Sensor & EN 62676-4 DORI Thresholds

Pixels-per-meter ($\text{PPM}$) at target distance $D$ for horizontal resolution $W_{\text{px}}$ and horizontal field of view $\text{HFOV}$:
$$\text{PPM} = \frac{W_{\text{px}}}{2 \times D \times \tan(\text{HFOV} / 2)}$$

- **Identification (250 px/m):** License plates, car numbers, badge faces
- **Recognition (125 px/m):** Vehicle make/model/livery
- **Observation (62.5 px/m):** Lane tracking, apex trajectory, gate queues
- **Detection (25 px/m):** Perimeter intrusion and incident detection

## 3. Running the Reference Planner

```bash
python mmwave_network_planner.py --selftest
python mmwave_network_planner.py --output campus_topology.kml
```

## 4. Verification & Limitations

- Calculated link margins must be validated against a physical line-of-sight walk test before trenching PoE or mounting masts.
- Foliage and heavy precipitation degrade 60 GHz links beyond 400 m; pair long-haul MH-T280 terminal runs with 5 GHz automatic failover where uptime is safety-critical.
