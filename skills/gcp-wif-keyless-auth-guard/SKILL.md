---
name: gcp-wif-keyless-auth-guard
description: GCP Workload Identity Federation (WIF) keyless OIDC token-exchange verifier, IAM service-account impersonation checker, and Cloud Run cost anomaly detector.
version: 1.0.0
author: Aria Technology Group
---

# GCP Workload Identity Federation (WIF) & Cost Guard

## Overview
Production reference pattern operated by **Aria Technology Group** for eliminating long-lived Google Cloud JSON service account keys on Vercel and GitHub Actions using **Workload Identity Federation (WIF)** OIDC token exchange.

## Capabilities
1. **OIDC Claim & Audience Binding Verification:** Validates that the Workload Identity Pool provider condition restricts `assertion.sub` and `aud` to the exact repository/project scope.
2. **Zero-Key Policy Check:** Rejects configurations that fall back to static `private_key` JSON files when WIF environment variables are misconfigured.
3. **Cloud Run Spend Spike Detector:** Evaluates daily Cloud Run/Firestore spend against a rolling baseline to flag runaway retry loops.

## CLI Usage
```bash
python wif_token_auditor.py --selftest
```
