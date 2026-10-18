---
name: elevenlabs-voice-telephony-bridge
description: ElevenLabs Conversational AI standalone tool schema validator, latency budget analyzer, and Zoom Phone / SIP outbound call dispatcher with human approval gates.
version: 1.0.0
author: Aria Technology Group
---

# ElevenLabs Conversational AI & Telephony Bridge

## Overview
Production reference pattern operated by **Aria Technology Group** for managing low-latency ElevenLabs voice agents, standalone `webhook` / `client` tool schemas, and outbound PSTN/SIP call orchestration.

## Key Capabilities
1. **Standalone Tool Schema Validation:** Verifies that every ElevenLabs tool definition includes deterministic JSON Schema properties, explicit timeout bounds, and non-blocking webhook configurations.
2. **Voice Turn Latency Budgeting:** Computes end-to-end turn latency across ASR, LLM time-to-first-token (TTFT), tool round-trip, and TTS streaming to keep conversational response times under `950 ms`.
3. **Outbound Call Safety Gate:** Enforces E.164 phone number validation, TCPA/business-hours window checks, and mandatory human-in-the-loop (HITL) approval before any live outbound dial.

## CLI Usage
```bash
python elevenlabs_tool_verifier.py --selftest
```
