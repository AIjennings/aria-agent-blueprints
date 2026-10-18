---
name: siklu-multihaultg-mesh-ops
description: Standard operating procedure, sector-to-port mapping, 5G jumpbox Tailscale provisioning, and IPv6 link-local to IPv4 TCP bridge daemon for Siklu MultiHaul TG (MH-N366, MH-T260, MH-T280) 60GHz Terragraph radios.
version: 1.0.0
author: Aria Technology Group
metadata:
  hermes:
    tags: [siklu, terragraph, 60ghz, networking, tailscale, ipv6]
---

# Siklu MultiHaul TG (Terragraph 60GHz) Mesh Operations

Use this skill when provisioning, tunneling into, or troubleshooting Siklu MultiHaul TG distribution nodes (`MH-N366`) and terminal units (`MH-T260`, `MH-T280`) across remote field sites.

## 1. MH-N366 Physical Port-to-Sector Mapping

| Sector | Default Channel / Freq | Physical Alignment on MH-N366 Chassis |
| :--- | :--- | :--- |
| **Sector 1** | Ch 2 (60.48 GHz) | Directly above **Port 1 (ETH1 / PoE In)** |
| **Sector 2** | Ch 1 (58.32 GHz) | Directly above **Port 2 (ETH2 / PoE Out)** |
| **Sector 3** | Ch 1 (58.32 GHz) | Directly above **Port 3 (SFP+ Fiber)** |
| **Sector 4** | Ch 1 (58.32 GHz) | Directly above **Port 4 (USB / Reset)** |

## 2. Out-of-Band 5G Jumpbox Provisioning

When managing an unconfigured or isolated Siklu radio via a Linux jumpbox (e.g., Raspberry Pi + USB 5G modem on `eth1` and PoE data on `eth0`):

```bash
echo "net.ipv4.ip_forward = 1" | sudo tee -a /etc/sysctl.d/99-tailscale.conf
echo "net.ipv6.conf.all.forwarding = 1" | sudo tee -a /etc/sysctl.d/99-tailscale.conf
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf
sudo ethtool -K eth0 rx-udp-gro-forwarding on rx-gro-list off 2>/dev/null || true
```

## 3. IPv6 Link-Local to IPv4 TCP Bridge

Siklu MultiHaul TG nodes always expose an IPv6 link-local management address (`fe80::...%eth0`) even when IPv4 DHCP fails. Use `siklu_ipv6_bridge.py` to expose the Web UI (`443`) and CLI (`22`) on local IPv4 ports (`8443` and `2222`).
