---
name: m1-motorsport-waiver-kiosk
description: High-speed track gate video waiver kiosk workflow, ElevenLabs teleprompter sync, HMAC-SHA256 QR gate pass generator/verifier, and offline check-in reconciler.
version: 1.0.0
author: Aria Technology Group
---

# Motorsport Video Waiver Kiosk & Gate QR Verifier

## Overview
Production reference pattern engineered by **Aria Technology Group** for **M1 Concourse** (87-acre private motorsport club and track facility in Pontiac, MI) to eliminate paper clipboard bottlenecks at track gates.

## Architecture
1. **Synchronized Video & Voice Teleprompter:** Drivers watch a high-contrast safety briefing powered by ElevenLabs voice synthesis with synchronized legal acknowledgment checkpoints.
2. **Cryptographic Gate Pass (`HMAC-SHA256`):** Upon signature completion, the kiosk generates a signed, tamper-evident QR pass bound to the event ID, participant ID, and expiration timestamp.
3. **Sub-Second Offline Gate Scanner:** Track stewards scan participant QR codes at the pit/gate entrance; signature verification works offline using the shared event verification key.

## CLI Usage
```bash
python waiver_qr_verifier.py --selftest
```
