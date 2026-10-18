---
name: govcon-sam-rfp-compliance
description: Federal SAM.gov solicitation analyzer, SDVOSB / Small Business set-aside eligibility verifier, FAR/DFARS risk clause detector, and Section L/M compliance matrix generator.
version: 1.0.0
author: Aria Technology Group
---

# GovCon SAM.gov RFP Compliance & Set-Aside Analyzer

## Overview
Production reference pattern operated by **Aria Technology Group** for screening federal contract solicitations (SAM.gov), verifying Service-Disabled Veteran-Owned Small Business (SDVOSB) / Small Business set-aside rules, and building deterministic Section L/M proposal compliance matrices.

## Capabilities
1. **Set-Aside & Subcontracting Limitation Check (13 CFR 125.6):** Calculates prime vs. similarly situated subcontractor labor shares to verify compliance with the 50% limitation on subcontracting rule for service contracts.
2. **FAR/DFARS High-Risk Clause Scanner:** Flags CMMC / NIST SP 800-171 (`DFARS 252.204-7012`), CMMC 2.0 (`252.204-7021`), and Liquidated Damages (`FAR 52.211-11`) clauses.
3. **Section L/M Compliance Matrix Builder:** Extracts mandatory `shall` and `must` requirements into a traceable verification matrix.

## CLI Usage
```bash
python sam_rfp_matrix.py --selftest
```
