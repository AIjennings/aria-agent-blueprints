---
name: voice-to-crm-copilot
description: Field voice-memo transcript parser, structured deal/next-step extractor, and Twenty CRM / HubSpot draft-staging dispatcher with mandatory human-in-the-loop approval gates.
version: 1.0.0
author: Aria Technology Group
metadata:
  hermes:
    tags: [elevenlabs, whisper, twenty-crm, hubspot, revops, voice-ai]
---

# Voice-to-CRM Copilot & Multi-Tenant Deal Dispatcher

Use this skill when converting field voice memos or call transcripts into structured CRM opportunity updates, support tickets, and client follow-up drafts.

## 1. Non-Destructive CRM & Communication Rules

1. **Append, Never Overwrite:** Notes and call summaries append to the opportunity timeline rather than replacing existing deal descriptions.
2. **Explicit Term & MRR Encoding:** Monthly recurring items record unit monthly rate (`MRR`) and term months explicitly (`TCV = one_time + MRR * term_months`).
3. **Draft-First Outbound Gate:** Generated client follow-up emails and proposals are staged as drafts (`requires_human_approval: true`) until an operator confirms recipient and terms.
