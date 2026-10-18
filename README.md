# Aria Agent Blueprints & Production Reference Skills

**Production-grade agent skills (`SKILL.md`), reference implementations, and deterministic operational tools built and operated by [Aria Technology Group](https://www.ariawave.tech) (Rochester, MI).**

These blueprints power real-world multi-agent operations across **1.55B+ production agent tokens**, **740+ autonomous and human-in-the-loop sessions**, and **430+ specialized operational skills** spanning enterprise voice AI, 60GHz millimeter-wave wireless mesh engineering, physical access control, telecom expense audits, fleet MDM, and e-commerce tax compliance.

---

## Architecture Principles

1. **Deterministic Tools Over Prompt Guessing:** Math, RF link budgets, Wiegand bitstreams, HMAC webhook verification, and financial calculations run in deterministic Python/TypeScript tools—never freehand LLM arithmetic.
2. **Human-in-the-Loop (HITL) Boundaries:** Agents classify, calculate, and stage drafts (CRM updates, QuickBooks draft invoices, carrier porting LOAs, outbound emails). High-impact financial, legal, or external communication actions require explicit human approval.
3. **Zero-Token Watchdogs (`no_agent` Pattern):** Infrastructure health, LiteLLM/proxy routing, and session store checks run via deterministic scripts that consume zero LLM tokens when systems are healthy and wake an agent only on state transitions.
4. **Portable `SKILL.md` Standard:** Every blueprint ships with a structured `SKILL.md` (compatible with [Hermes Agent](https://github.com/NousResearch/hermes-agent), Claude Code, Cursor, and MCP hosts) paired with a zero-dependency runnable Python reference script.

---

## Included Production Blueprints

| Blueprint | Skill & Reference Tool | Primary Stack | Operational Scope |
| :--- | :--- | :--- | :--- |
| **1. 60GHz mmWave & 3D Camera FOV Planner** | [`skills/mmwave-vision-mesh-planner`](./skills/mmwave-vision-mesh-planner) | Siklu MultiHaul TG, Google Earth KML, Python | Computes 60GHz Free Space Path Loss, O₂ absorption, 1st Fresnel zone clearance, EN 62676-4 DORI camera distances, and exports 3D `.kml` FOV cones. |
| **2. Siklu Terragraph Field Jumpbox & IPv6 Bridge** | [`skills/siklu-multihaultg-mesh-ops`](./skills/siklu-multihaultg-mesh-ops) | Siklu MH-N366 / T280, Tailscale, Python Sockets | Maps MH-N366 physical sectors, configures Linux UDP GRO routing for 5G field jumpboxes, and bridges IPv6 link-local radios to IPv4 ports. |
| **3. HID Access Control & Wiegand Provisioning** | [`skills/hid-access-control-provisioning`](./skills/hid-access-control-provisioning) | HID Signo / VertX / Aero, OSDP v2, Wiegand 26/37 | Decodes raw 26-bit (H10301) and 37-bit (H10302) hex/binary credential frames, verifies even/odd parity bits, and diagnoses 125kHz (`009P`) vs Seos reader profiles. |
| **4. E-Commerce Tax Exemption Webhook Bridge** | [`skills/ecom-tax-exemption-bridge`](./skills/ecom-tax-exemption-bridge) | FastAPI, GCP Cloud Run, Shopify Webhooks, QBO | Validates Shopify HMAC-SHA256 checkout webhooks, audits state tax-exemption certificates, prevents duplicate order processing, and stages draft accounting payloads. |
| **5. Telecom Expense Audit & Carrier Buyout Engine** | [`skills/telecom-bill-audit-engine`](./skills/telecom-bill-audit-engine) | Python CSV/OCR Parser, RingCentral Partner API | Audits monthly carrier line items for unauthorized regulatory/admin surcharges, calculates Early Termination Fee (ETF) buyout ROI, and generates porting LOA manifests. |
| **6. Enterprise Fleet Knox MDM & ELD Validator** | [`skills/fleet-knox-mdm-telemetry`](./skills/fleet-knox-mdm-telemetry) | Samsung Knox Cloud, Samsara ELD, Android Enterprise | Validates zero-touch rugged tablet kiosk profiles, normalizes Samsara ELD hours-of-service & J1939 fault webhooks, and tracks driver hardware custody receipts. |
| **7. Self-Healing Multi-Model Gateway Watchdog** | [`skills/multi-agent-gateway-watchdog`](./skills/multi-agent-gateway-watchdog) | LiteLLM, Hermes Agent Cron, SQLite WAL | Zero-token health poller for multi-model inference proxies and SQLite session databases with state-transition alerting. |
| **8. Voice-to-CRM Copilot & Deal Dispatcher** | [`skills/voice-to-crm-copilot`](./skills/voice-to-crm-copilot) | ElevenLabs, Whisper, Twenty CRM, Google Workspace | Extracts structured BANT/MEDDIC next steps from field voice transcripts and stages draft CRM opportunity updates and follow-up emails behind an approval gate. |

---

## Quick Start & Self-Test

Every reference script in this repository runs with the Python 3.10+ standard library and includes a built-in `--selftest` mode that executes a deterministic verification suite:

```bash
git clone https://github.com/AIjennings/aria-agent-blueprints.git
cd aria-agent-blueprints

# Run the verification suite across all 8 reference tools
python scripts/run_all_selftests.py
```

To install any skill into [Hermes Agent](https://github.com/NousResearch/hermes-agent):

```bash
cp -r skills/* ~/.hermes/skills/
```

---

## Live Blueprints & Executive Advisory

- **Interactive Blueprint Library & Audio Briefings:** [https://www.ariawave.tech/resources](https://www.ariawave.tech/resources)
- **Business AI Operations Index:** [https://www.ariawave.tech/ai-operations](https://www.ariawave.tech/ai-operations)
- **M1 Concourse Full-Stack Case Study:** [https://www.ariawave.tech/case-studies/m1-concourse](https://www.ariawave.tech/case-studies/m1-concourse)
- **Book an Architecture Review:** [Schedule via Zoom](https://scheduler.zoom.us/andrew-jennings-rzou8s/technology-consult)

---

## License

MIT License · Copyright © 2026 Aria Technology Group LLC (127 E 3rd Street, Rochester, MI 48307).
