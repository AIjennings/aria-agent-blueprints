#!/usr/bin/env python3
"""
mmwave_network_planner.py
60GHz Millimeter-Wave RF Link Budget, EN 62676-4 Camera DORI Calculator, and 3D Google Earth KML Generator.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
import math
from dataclasses import dataclass, asdict
from typing import List, Dict

EARTH_RADIUS_M = 6_371_000.0


@dataclass
class SiteNode:
    node_id: str
    name: str
    role: str  # "distribution_hub" | "camera_pole" | "core_gateway"
    lat: float
    lon: float
    mount_height_m: float
    camera_res_w: int = 3840
    camera_hfov_deg: float = 90.0
    azimuth_deg: float = 0.0


@dataclass
class RFLinkAssessment:
    source_id: str
    target_id: str
    distance_m: float
    freq_ghz: float
    fresnel_r1_m: float
    fspl_db: float
    oxygen_loss_db: float
    total_path_loss_db: float
    estimated_rssi_dbm: float
    status: str


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    return 2.0 * EARTH_RADIUS_M * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


def analyze_60ghz_link(
    src: SiteNode,
    dst: SiteNode,
    freq_ghz: float = 60.48,
    tx_eirp_dbm: float = 40.0,
    rx_gain_dbi: float = 38.0,
) -> RFLinkAssessment:
    horiz_m = haversine_m(src.lat, src.lon, dst.lat, dst.lon)
    dz = dst.mount_height_m - src.mount_height_m
    dist_m = max(1.0, math.hypot(horiz_m, dz))
    dist_km = dist_m / 1000.0

    fresnel_r1_m = 8.657 * math.sqrt(dist_km / freq_ghz)
    fspl_db = 92.45 + 20.0 * math.log10(dist_km) + 20.0 * math.log10(freq_ghz)
    oxygen_loss_db = 15.0 * dist_km  # 60GHz O2 resonance absorption
    total_loss_db = fspl_db + oxygen_loss_db
    rssi_dbm = tx_eirp_dbm + rx_gain_dbi - total_loss_db

    if rssi_dbm >= -60.0:
        status = "OPTIMAL_MCS12_MULTI_GIGABIT"
    elif rssi_dbm >= -68.0:
        status = "VIABLE_HIGH_THROUGHPUT"
    elif rssi_dbm >= -75.0:
        status = "MARGINAL_REQUIRES_HIGH_GAIN_TU"
    else:
        status = "OUT_OF_RANGE_ADD_RELAY"

    return RFLinkAssessment(
        source_id=src.node_id,
        target_id=dst.node_id,
        distance_m=round(dist_m, 2),
        freq_ghz=freq_ghz,
        fresnel_r1_m=round(fresnel_r1_m, 3),
        fspl_db=round(fspl_db, 2),
        oxygen_loss_db=round(oxygen_loss_db, 2),
        total_path_loss_db=round(total_loss_db, 2),
        estimated_rssi_dbm=round(rssi_dbm, 2),
        status=status,
    )


def compute_dori_distances_m(horizontal_px: int, hfov_deg: float) -> Dict[str, float]:
    half_angle_rad = math.radians(max(1.0, min(175.0, hfov_deg)) / 2.0)
    tan_half = math.tan(half_angle_rad)
    thresholds = {
        "identification_250ppm_m": 250.0,
        "recognition_125ppm_m": 125.0,
        "observation_62_5ppm_m": 62.5,
        "detection_25ppm_m": 25.0,
    }
    return {
        k: round(horizontal_px / (2.0 * ppm * tan_half), 2)
        for k, ppm in thresholds.items()
    }


def project_point(lat: float, lon: float, bearing_deg: float, distance_m: float) -> tuple[float, float]:
    brng = math.radians(bearing_deg)
    d_rad = distance_m / EARTH_RADIUS_M
    lat1 = math.radians(lat)
    lon1 = math.radians(lon)
    lat2 = math.asin(math.sin(lat1) * math.cos(d_rad) + math.cos(lat1) * math.sin(d_rad) * math.cos(brng))
    lon2 = lon1 + math.atan2(
        math.sin(brng) * math.sin(d_rad) * math.cos(lat1),
        math.cos(d_rad) - math.sin(lat1) * math.sin(lat2),
    )
    return math.degrees(lat2), math.degrees(lon2)


def generate_kml(nodes: List[SiteNode], links: List[RFLinkAssessment]) -> str:
    node_map = {n.node_id: n for n in nodes}
    placemarks: List[str] = []

    for n in nodes:
        dori = compute_dori_distances_m(n.camera_res_w, n.camera_hfov_deg)
        obs_dist = dori["observation_62_5ppm_m"]
        left_lat, left_lon = project_point(n.lat, n.lon, n.azimuth_deg - n.camera_hfov_deg / 2.0, obs_dist)
        right_lat, right_lon = project_point(n.lat, n.lon, n.azimuth_deg + n.camera_hfov_deg / 2.0, obs_dist)
        placemarks.append(
            f"""    <Placemark>
      <name>{n.name} ({n.node_id})</name>
      <description>Role: {n.role} | Mount: {n.mount_height_m}m | DORI ID: {dori['identification_250ppm_m']}m, Obs: {obs_dist}m</description>
      <Point><altitudeMode>relativeToGround</altitudeMode><coordinates>{n.lon:.6f},{n.lat:.6f},{n.mount_height_m:.1f}</coordinates></Point>
    </Placemark>
    <Placemark>
      <name>{n.node_id} FOV Cone (Observation {obs_dist}m)</name>
      <Polygon>
        <altitudeMode>relativeToGround</altitudeMode>
        <outerBoundaryIs><LinearRing><coordinates>
          {n.lon:.6f},{n.lat:.6f},{n.mount_height_m:.1f}
          {left_lon:.6f},{left_lat:.6f},1.5
          {right_lon:.6f},{right_lat:.6f},1.5
          {n.lon:.6f},{n.lat:.6f},{n.mount_height_m:.1f}
        </coordinates></LinearRing></outerBoundaryIs>
      </Polygon>
    </Placemark>"""
        )

    for lk in links:
        s, d = node_map[lk.source_id], node_map[lk.target_id]
        placemarks.append(
            f"""    <Placemark>
      <name>60GHz Link {lk.source_id} -> {lk.target_id} ({lk.distance_m}m)</name>
      <description>Fresnel r1: {lk.fresnel_r1_m}m | Path Loss: {lk.total_path_loss_db}dB | Est RSSI: {lk.estimated_rssi_dbm}dBm | {lk.status}</description>
      <LineString>
        <altitudeMode>relativeToGround</altitudeMode>
        <coordinates>{s.lon:.6f},{s.lat:.6f},{s.mount_height_m:.1f} {d.lon:.6f},{d.lat:.6f},{d.mount_height_m:.1f}</coordinates>
      </LineString>
    </Placemark>"""
        )

    body = "\n".join(placemarks)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Aria 60GHz mmWave &amp; 3D Camera FOV Topology</name>
{body}
  </Document>
</kml>
"""


def sample_campus() -> tuple[List[SiteNode], List[RFLinkAssessment]]:
    nodes = [
        SiteNode("DN-01", "Central Paddock Distribution Hub (MH-N366)", "distribution_hub", 42.61520, -83.25810, 9.0, 7680, 180.0, 180.0),
        SiteNode("TU-02", "Turn 1 Timing & Telemetry Mast (MH-T280)", "camera_pole", 42.61685, -83.25640, 6.0, 3840, 60.0, 225.0),
        SiteNode("TU-03", "West Straightaway Optical Gate (MH-T260)", "camera_pole", 42.61410, -83.26020, 6.0, 7680, 180.0, 90.0),
    ]
    links = [
        analyze_60ghz_link(nodes[0], nodes[1]),
        analyze_60ghz_link(nodes[0], nodes[2]),
    ]
    return nodes, links


def run_selftest() -> None:
    nodes, links = sample_campus()
    assert len(links) == 2
    assert 0.4 < links[0].fresnel_r1_m < 0.9, f"Unexpected Fresnel radius: {links[0].fresnel_r1_m}"
    assert links[0].status in ("OPTIMAL_MCS12_MULTI_GIGABIT", "VIABLE_HIGH_THROUGHPUT")
    dori = compute_dori_distances_m(7680, 120.0)
    assert dori["identification_250ppm_m"] > 8.0
    kml = generate_kml(nodes, links)
    assert "<kml" in kml and "60GHz Link DN-01 -> TU-02" in kml
    print(json.dumps({
        "selftest": "PASS",
        "links": [asdict(lk) for lk in links],
        "sample_dori_7680px_120deg": dori,
    }, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="60GHz mmWave & Camera DORI KML Planner")
    parser.add_argument("--selftest", action="store_true", help="Run deterministic verification suite")
    parser.add_argument("--output", type=str, default="", help="Write 3D KML topology to file")
    args = parser.parse_args()

    if args.selftest:
        run_selftest()
    else:
        nodes, links = sample_campus()
        kml_text = generate_kml(nodes, links)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(kml_text)
            print(f"Wrote {len(kml_text)} bytes to {args.output}")
        else:
            print(kml_text)
