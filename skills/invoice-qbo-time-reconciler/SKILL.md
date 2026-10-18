---
name: invoice-qbo-time-reconciler
description: Engineering time-log & ticket reconciler, QuickBooks Online hardware vs. labor item categorizer, retainer burn-down calculator, and draft-only invoice generator.
version: 1.0.0
author: Aria Technology Group
---

# Engineering Time-Tracking & QuickBooks Draft Reconciler

## Overview
Production reference pattern operated by **Aria Technology Group** for reconciling engineering commits, support tickets, and field deployments into auditable **QuickBooks Online (QBO)** and **Invoice Ninja** draft invoices.

## Financial Guardrails
1. **Draft-Only Billing Creation:** Every generated invoice payload defaults to `status: "DRAFT"` with `auto_email_client: False`. No invoice or payment link is ever transmitted without explicit human approval.
2. **Explicit Hardware vs. Labor Categorization:** Separates taxable physical hardware SKUs (e.g., Siklu radios, Axis cameras, HID readers) from non-taxable professional engineering labor.

## CLI Usage
```bash
python billing_reconciler.py --selftest
```
