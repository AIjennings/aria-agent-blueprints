---
name: compliance-stack-hardening
description: "Harden Docker-based compliance and GRC frameworks (e.g., CISO Assistant, Invoice Ninja, billing/audit stacks) for SOC 2, ISO 27001, and audit readiness. Covers localhost network binding, container security, reverse proxy headers, image digest pinning, log rotation, and SOC 2 Trust Services Criteria mapping."
version: 1.0.0
author: Aria Technology Group (https://www.ariawave.tech)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Compliance, SOC2, ISO27001, GRC, Docker, Hardening, Security, Audit, AriaWave]
---

# Compliance & Billing Stack Hardening (`SOC 2` / `ISO 27001`)

Production audit skill and zero-dependency Python 3.10+ CLI tool engineered by **[Aria Technology Group](https://www.ariawave.tech)** (`AriaWave`) to audit and harden Docker-based compliance, GRC, and financial/billing stacks (such as CISO Assistant, Invoice Ninja, and internal control planes) against **SOC 2 Trust Services Criteria (`CC6.1`, `CC7.1`, `CC7.2`, `CC8.1`, `A1.2`)**.

> **Safety & Non-Destructive Guarantee:** `compliance_compose_auditor.py` operates strictly as a **read-only static configuration & header auditor** with deterministic SOC 2 evidence generation. It never restarts containers or mutates firewall rules automatically.

---

## Default Threat Model & SOC 2 Control Matrix

| Control ID | Finding / Default Risk | Required Hardening Baseline | SOC 2 Trust Criteria |
| :--- | :--- | :--- | :--- |
| **`NET-01`** | Ports bound to `0.0.0.0` (e.g. `8443:8443`, `6333:6333`) | Prefix host port mappings with `127.0.0.1:` unless behind an authenticated edge proxy | **CC6.1** — Logical access & network segmentation |
| **`APP-01`** | `DJANGO_DEBUG=True` or `APP_DEBUG=true` | Force `DJANGO_DEBUG=False` / `APP_DEBUG=false` in all non-ephemeral environments | **CC7.2** — System monitoring & error disclosure |
| **`PRX-01`** | Missing HTTP security headers or exposed `Server` banner | Enforce `X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin` | **CC6.1 / CC7.2** — Web application boundary protection |
| **`CNT-01`** | Mutable `:latest` image tags without SHA-256 digest | Pin production images to immutable `@sha256:...` digests | **CC7.2 / CC8.1** — Change management & supply-chain integrity |
| **`LOG-01`** | Unbounded container stdout logs | Configure `json-file` log rotation (`max-size: 10m`, `max-file: 3`) | **CC7.2 / A1.2** — System availability & log retention |

---

## Quickstart CLI Commands

```bash
# 1. Run the built-in deterministic self-test suite
python compliance_compose_auditor.py --selftest

# 2. Audit a docker-compose.yml file and emit a SOC 2 JSON evidence report
python compliance_compose_auditor.py --compose /path/to/docker-compose.yml --json
```
