---
name: twenty-crm-muse-connector
description: Twenty CRM REST/GraphQL deal synchronizer, monthly term-encoded MRR/TCV calculator, support-ticket PII masking shim, and human-gated pipeline dispatcher.
version: 1.0.0
author: Aria Technology Group
---

# Twenty CRM & Support Ticket Connector Shim

## Overview
Production reference pattern operated by **Aria Technology Group** for bridging **Twenty CRM** (`opportunities`, `people`, `companies`, `supportTickets`) with autonomous AI agents and custom HTTPS connectors.

## Core Guardrails
1. **Term-Encoded Monthly Line Items:** Monthly recurring items encode contract term in `quantity` (e.g., `qty=12` at `$1,500/mo` = 12-month term). `MRR` equals the unit rate; `TCV` equals `one_time + (MRR * term_months)`.
2. **Fixture Isolation:** Any record tagged `TEST-FIXTURE` or `DO-NOT-SYNC` is deterministically blocked before outbound CRM mutation.
3. **Client PII Masking on Read-Only Shims:** Support ticket connectors mask raw phone digits and personal email local-parts before returning payloads to external LLM contexts.

## CLI Usage
```bash
python twenty_crm_shim.py --selftest
```
