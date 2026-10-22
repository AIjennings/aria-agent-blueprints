# Aria Agent Blueprints & Production Reference Skills

**21 production-grade agent skills (`SKILL.md`), reference implementations, and deterministic operational tools built and operated by [Aria Technology Group](https://www.ariawave.tech).**

Operated across **1.55B+ cumulative agent tokens**, **743+ working sessions**, and **430+ operational skills** across multi-profile Hermes Agent environments, commercial real estate underwriting, 60GHz millimeter-wave motorsport networks, enterprise telecom audits, and physical security deployments.

---

## Quick Start & One-Command Self-Test

Every reference skill in this repository includes a zero-dependency (Python 3.10+ standard library) deterministic verification tool with a built-in `--selftest` suite:

```bash
git clone https://github.com/AIjennings/aria-agent-blueprints.git
cd aria-agent-blueprints
python scripts/run_all_selftests.py
```

To install these skills directly into [Hermes Agent](https://github.com/NousResearch/hermes-agent):

```bash
cp -r skills/* ~/.hermes/skills/
```

---

## 21 Production Reference Skills & Verification Tools

| # | Skill Directory | Reference CLI Tool | Domain & Deterministic Verification Scope |
|---|---|---|---|
| 1 | [`skills/mmwave-vision-mesh-planner`](skills/mmwave-vision-mesh-planner) | `mmwave_network_planner.py` | **60GHz mmWave & Vision AI:** Friis path loss, oxygen/rain attenuation, 1st Fresnel zone clearance, EN 62676-4 DORI camera distances, and 3D Google Earth KML generator (deployed at M1 Concourse). |
| 2 | [`skills/siklu-multihaultg-mesh-ops`](skills/siklu-multihaultg-mesh-ops) | `siklu_ipv6_bridge.py` | **Siklu MultiHaul TG Mesh Ops:** IEEE EUI-64 `fe80::` link-local calculator from chassis MAC, V100 sector-to-port mapper, and IPv4-to-IPv6 TCP bridge over 5G Tailscale jumpboxes. |
| 3 | [`skills/hid-access-control-provisioning`](skills/hid-access-control-provisioning) | `wiegand_badge_analyzer.py` | **HID Physical Access Control:** Wiegand 26-bit (H10301) even/odd parity bit encoder/decoder and 125kHz (`009P`) vs. Seos (`900P`) reader carrier diagnostics. |
| 4 | [`skills/ecom-tax-exemption-bridge`](skills/ecom-tax-exemption-bridge) | `shopify_tax_bridge.py` | **E-Commerce Tax Bridge:** Constant-time Shopify `X-Shopify-Hmac-Sha256` webhook verifier, exempt-tag tax discrepancy detector, and draft-only QBO invoice payload builder. |
| 5 | [`skills/telecom-bill-audit-engine`](skills/telecom-bill-audit-engine) | `telecom_audit_parser.py` | **Telecom Audit & ETF Buyout:** Non-mandated carrier surcharge auditor (`USF`, `RCRF`, `ADMIN`), ETF contract buyout ROI calculator, and Porting LOA manifest generator. |
| 6 | [`skills/fleet-knox-mdm-telemetry`](skills/fleet-knox-mdm-telemetry) | `knox_staging_validator.py` | **Fleet Knox MDM & Samsara ELD:** Samsung Knox zero-touch rugged tablet kiosk policy validator and Samsara ELD HOS/J1939 fault alert normalizer. |
| 7 | [`skills/multi-agent-gateway-watchdog`](skills/multi-agent-gateway-watchdog) | `gateway_health_watchdog.py` | **Zero-Token Gateway Watchdog:** Hermes `no_agent=True` state-transition health monitor across multi-model lanes and SQLite WAL session stores. |
| 8 | [`skills/voice-to-crm-copilot`](skills/voice-to-crm-copilot) | `voice2crm_dispatcher.py` | **Voice-to-CRM Copilot:** Field voice-memo transcript parser, MRR/TCV deal stager, and human-gated follow-up draft dispatcher. |
| 9 | [`skills/cre-sovereign-underwriter`](skills/cre-sovereign-underwriter) | `cre_underwriter_calc.py` | **CRE Sovereign Underwriter:** Local-first T-12 operating statement NOI, Cap Rate sensitivity matrix (`±50 bps`), and DSCR debt-service calculator. |
| 10 | [`skills/twenty-crm-muse-connector`](skills/twenty-crm-muse-connector) | `twenty_crm_shim.py` | **Twenty CRM & Muse Connector Shim:** Term-encoded monthly MRR/TCV quote synchronizer, `TEST-FIXTURE` sync blocker, and support-ticket PII masker. |
| 11 | [`skills/elevenlabs-voice-telephony-bridge`](skills/elevenlabs-voice-telephony-bridge) | `elevenlabs_tool_verifier.py` | **ElevenLabs Voice & Telephony Bridge:** Standalone `webhook`/`client` tool schema validator, turn latency budgeter (`<950ms`), and E.164 outbound dial gate. |
| 12 | [`skills/m1-motorsport-waiver-kiosk`](skills/m1-motorsport-waiver-kiosk) | `waiver_qr_verifier.py` | **Motorsport Video Waiver Kiosk:** Track gate `HMAC-SHA256` QR pass issuer, constant-time offline gate scanner verifier, and expiration guard. |
| 13 | [`skills/google-workspace-sovereign-bridge`](skills/google-workspace-sovereign-bridge) | `workspace_mime_guard.py` | **Google Workspace Sovereign Bridge:** Dual-account RFC 2822 MIME draft builder, recipient-domain context mismatch guard, and calendar buffer conflict detector. |
| 14 | [`skills/live-motorsport-timing-extractor`](skills/live-motorsport-timing-extractor) | `motorsport_timing_analyzer.py` | **Live Motorsport Timing Analyzer:** SpeedHive/Mylaps sector split parser, purple-sector theoretical optimal lap calculator, and yellow-flag outlier filter. |
| 15 | [`skills/govcon-sam-rfp-compliance`](skills/govcon-sam-rfp-compliance) | `sam_rfp_matrix.py` | **GovCon SAM.gov RFP Compliance:** 13 CFR 125.6 SDVOSB subcontracting limitation calculator, FAR/DFARS risk clause scanner, and Section L/M matrix builder. |
| 16 | [`skills/mcp-security-governance-scanner`](skills/mcp-security-governance-scanner) | `mcp_schema_auditor.py` | **MCP Security Governance Scanner:** OWASP LLM07/LLM08 tool-schema auditor for destructive actions and unconstrained SSRF/command injection sinks. |
| 17 | [`skills/gcp-wif-keyless-auth-guard`](skills/gcp-wif-keyless-auth-guard) | `wif_token_auditor.py` | **GCP Workload Identity Federation Guard:** Keyless OIDC `external_account` configuration verifier and static service-account key blocker. |
| 18 | [`skills/aviation-weather-go-nogo`](skills/aviation-weather-go-nogo) | `metar_risk_scorer.py` | **Aviation Weather & Go/No-Go Engine:** FAA VFR/MVFR/IFR/LIFR classifier, runway crosswind vector calculator, and density altitude compute engine. |
| 19 | [`skills/invoice-qbo-time-reconciler`](skills/invoice-qbo-time-reconciler) | `billing_reconciler.py` | **Engineering Time & QBO Reconciler:** Ticket/commit worklog reconciler, retainer burn-down calculator, hardware vs. labor categorizer, and draft-only QBO builder. |
| 20 | [`skills/satellite-change-detection-gis`](skills/satellite-change-detection-gis) | `geospatial_tile_calc.py` | **Satellite & Aerial Change Detection:** Web Mercator XYZ slippy-map tile calculator, Ground Sample Distance (GSD) verifier, and roof/shoreline delta analyzer. |
| 21 | [`skills/php2shell-vulnerability-scanner`](skills/php2shell-vulnerability-scanner) | `php2shell_scanner.py` | **PHP2Shell Readiness & Mitigation Scanner (`CVE-2026-109618` / `CVE-2026-109619`):** Defensive PHP runtime/container/manifest version verifier (`8.5.12`/`8.4.27`/`8.3.36`/`8.2.35`), Apache `mod_php` & `RLimitMEM` hazard detector, `.htaccess`/INI override auditor, and `php.d` drop-in mitigation generator. |

---

## Human-in-the-Loop (HITL) Governance

All Aria Technology Group reference blueprints enforce three non-negotiable production rules:
1. **Draft-Only Financial & External Mutations:** Invoices, CRM deal mutations, and external emails are staged as drafts requiring explicit human confirmation.
2. **Fixture Isolation:** Any record tagged `TEST-FIXTURE` or `DO-NOT-SYNC` is deterministically blocked at the adapter boundary.
3. **Zero-Token Health Monitoring:** Recurring infrastructure watchdogs run as deterministic scripts (`no_agent=True`) that consume zero LLM tokens when systems are healthy.

## License

MIT License — Copyright (c) 2026 [Aria Technology Group LLC](https://www.ariawave.tech)
