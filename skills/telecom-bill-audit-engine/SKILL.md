---
name: telecom-bill-audit-engine
description: Automated carrier invoice surcharge auditor, USF/regulatory recovery calculator, Early Termination Fee (ETF) contract buyout evaluator, and Letter of Authorization (LOA) porting manifest generator.
version: 1.0.0
author: Aria Technology Group
metadata:
  hermes:
    tags: [telecom, bill-audit, ucaas, ringcentral, loa, expense-management]
---

# Telecom Expense Management & Carrier Buyout Engine

Use this skill when auditing commercial telecom, fiber, PRI/SIP, and UCaaS invoices (Comcast Business, AT&T, Spectrum, Verizon) to identify billing anomalies, unused DIDs, expired promotional discounts, and contract buyout ROI.

## 1. Audit Methodology

1. **Surcharge & Junk-Fee Classification:** Distinguish statutory taxes (E911, state sales tax) from carrier-imposed discretionary recovery fees (Administrative Expense Fee, Cost Recovery Charge, Non-Published DID Surcharge).
2. **Idle Circuit & Seat Utilization:** Cross-reference billed seat/trunk counts against active 30-day call detail records (CDRs).
3. **Contract Buyout Arithmetic:** Compare remaining months $\times$ Early Termination Fee (ETF) penalty against monthly run-rate reduction + partner contract buyout credits.
4. **Human-Reviewed Porting LOA:** Stage Letter of Authorization (LOA) and Customer Service Record (CSR) requests with verified Service Address and Billing Telephone Numbers (BTNs) for client signature.
