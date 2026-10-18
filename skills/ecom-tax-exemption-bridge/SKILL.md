---
name: ecom-tax-exemption-bridge
description: High-volume Shopify checkout webhook HMAC-SHA256 verifier, state non-profit tax exemption validator, idempotency guard, and QuickBooks Online draft invoice staging engine.
version: 1.0.0
author: Aria Technology Group
metadata:
  hermes:
    tags: [shopify, tax-exemption, cloud-run, quickbooks, ecommerce, webhooks]
---

# High-Volume E-Commerce Tax Exemption Bridge

Use this skill when operating or auditing Cloud Run / serverless bridges that reconcile Shopify B2B/non-profit orders with tax-exemption certificates and accounting ledgers.

## 1. Security & Financial Guardrails

1. **Constant-Time HMAC Verification:** Every Shopify webhook (`X-Shopify-Hmac-Sha256`) must be verified with `hmac.compare_digest` against the raw request body before parsing JSON.
2. **Idempotency Keys:** Deduplicate incoming `orders/create` and `orders/updated` events by `(order_id, updated_at)` to prevent duplicate ledger entries during webhook retries.
3. **Draft-Only Accounting Staging:** When an order shows a tax mismatch or requires a tax-exempt credit memo, stage the QuickBooks Online invoice/adjustment as `Draft` (`send_email: false`) and notify an operator for human approval.
