---
name: multi-agent-gateway-watchdog
description: Zero-token self-healing LLM gateway watchdog (no_agent=True cron pattern) that probes multi-model proxy lanes, verifies SQLite WAL session integrity, and emits alerts only on state transitions.
version: 1.0.0
author: Aria Technology Group
metadata:
  hermes:
    tags: [litellm, hermes-agent, watchdog, cron, sqlite, observability]
---

# Self-Healing Multi-Model Gateway Watchdog (`no_agent` Pattern)

Use this skill to monitor multi-model LLM gateways (LiteLLM, local proxy bridges, and SQLite FTS5 session stores) on a 5-minute schedule without burning LLM tokens on healthy ticks.

## 1. The Zero-Token Watchdog Contract

When scheduled with `no_agent=True` in Hermes Agent:
1. **Healthy State → Silent (`stdout = ""`):** When all upstream model lanes respond within latency thresholds and SQLite `PRAGMA quick_check` passes, the script writes state to disk and exits `0` with empty stdout. Zero messages are sent and zero tokens are consumed.
2. **Degraded / Recovery Transition → Concise Alert:** Only when a lane transitions from `UP -> DOWN` or `DOWN -> RECOVERED` does the script print a diagnostic summary to stdout, triggering an immediate operator notification.
