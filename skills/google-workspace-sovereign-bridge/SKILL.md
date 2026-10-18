---
name: google-workspace-sovereign-bridge
description: Dual-account Google Workspace REST bridge with RFC 2822 MIME draft staging, recipient-context mismatch guard, and executive calendar conflict resolver.
version: 1.0.0
author: Aria Technology Group
---

# Google Workspace Sovereign Bridge & Outbound Draft Guard

## Overview
Production reference pattern operated by **Aria Technology Group** for managing multi-account Google Workspace operations (corporate + executive inboxes, Calendar, and Drive) without exposing raw mailbox send permissions to autonomous execution loops.

## Safety Architecture
1. **Draft-First Outbound Rule:** External client communications are staged as Gmail drafts (`users.drafts.create`) rather than sent directly (`users.messages.send`), requiring explicit owner confirmation.
2. **Recipient Domain Context Guard:** Verifies that every recipient address matches the active client engagement domain or explicit allowlist before staging an email.
3. **Deterministic Calendar Conflict Detection:** Evaluates proposed meeting intervals against existing busy blocks including mandatory travel/prep buffer windows.

## CLI Usage
```bash
python workspace_mime_guard.py --selftest
```
