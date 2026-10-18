#!/usr/bin/env python3
"""
siklu_ipv6_bridge.py
Deterministic Siklu MultiHaul TG EUI-64 Link-Local Calculator, Sector Mapper, and IPv6-to-IPv4 TCP Bridge.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
import socket
import threading
from typing import Dict

MH_N366_SECTORS: Dict[int, Dict[str, str]] = {
    1: {"port": "Port 1 (ETH1 / PoE In)", "default_channel": "2 (60.48 GHz)", "coverage_deg": "0-90"},
    2: {"port": "Port 2 (ETH2 / PoE Out)", "default_channel": "1 (58.32 GHz)", "coverage_deg": "90-180"},
    3: {"port": "Port 3 (SFP+ Fiber)", "default_channel": "1 (58.32 GHz)", "coverage_deg": "180-270"},
    4: {"port": "Port 4 (USB / Reset)", "default_channel": "1 (58.32 GHz)", "coverage_deg": "270-360"},
}


def mac_to_ipv6_link_local(mac: str) -> str:
    """Convert a 48-bit MAC address (e.g. 46:5b:78:0c:5a:a0) into its RFC 4291 EUI-64 fe80:: address."""
    clean = mac.replace(":", "").replace("-", "").replace(".", "").lower()
    if len(clean) != 12:
        raise ValueError(f"Invalid MAC address: {mac}")
    b = [int(clean[i:i + 2], 16) for i in range(0, 12, 2)]
    b[0] ^= 0x02  # Flip Universal/Local bit
    eui = [b[0], b[1], b[2], 0xFF, 0xFE, b[3], b[4], b[5]]
    hextets = [
        (eui[0] << 8) | eui[1],
        (eui[2] << 8) | eui[3],
        (eui[4] << 8) | eui[5],
        (eui[6] << 8) | eui[7],
    ]
    return "fe80::" + ":".join(f"{h:x}" for h in hextets)


def _pipe(src: socket.socket, dst: socket.socket) -> None:
    try:
        while True:
            data = src.recv(8192)
            if not data:
                break
            dst.sendall(data)
    except OSError:
        pass
    finally:
        for s in (src, dst):
            try:
                s.close()
            except OSError:
                pass


def start_ipv4_to_ipv6_listener(listen_port: int, target_ipv6: str, target_port: int, interface: str) -> None:
    scope_id = socket.if_nametoindex(interface)
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", listen_port))
    srv.listen(16)
    while True:
        client, _ = srv.accept()
        try:
            upstream = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
            upstream.connect((target_ipv6, target_port, 0, scope_id))
            threading.Thread(target=_pipe, args=(client, upstream), daemon=True).start()
            threading.Thread(target=_pipe, args=(upstream, client), daemon=True).start()
        except OSError:
            client.close()


def run_selftest() -> None:
    ll = mac_to_ipv6_link_local("46:5b:78:0c:5a:a0")
    assert ll == "fe80::445b:78ff:fe0c:5aa0", f"Unexpected EUI-64: {ll}"
    assert len(MH_N366_SECTORS) == 4
    print(json.dumps({
        "selftest": "PASS",
        "sample_mac": "46:5b:78:0c:5a:a0",
        "computed_link_local": ll,
        "mh_n366_sectors": MH_N366_SECTORS,
    }, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Siklu MultiHaul TG EUI-64 & IPv6 Bridge Utility")
    parser.add_argument("--selftest", action="store_true", help="Run EUI-64 and sector mapping self-test")
    parser.add_argument("--mac", type=str, help="Calculate Siklu IPv6 link-local address from MAC")
    args = parser.parse_args()
    if args.selftest:
        run_selftest()
    elif args.mac:
        print(mac_to_ipv6_link_local(args.mac))
    else:
        run_selftest()
