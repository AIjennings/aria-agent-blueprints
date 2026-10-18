---
name: mcp-security-governance-scanner
description: Model Context Protocol (MCP) tool-schema security auditor that detects shell injection sinks, SSRF URL parameters, and unguarded destructive actions.
version: 1.0.0
author: Aria Technology Group
---

# MCP Security Governance & Tool-Schema Auditor

## Overview
Production reference pattern engineered by **Aria Technology Group** for auditing Model Context Protocol (MCP) servers and LLM tool registries against **OWASP LLM Top 10** (`LLM07: Insecure Plugin/Tool Design` & `LLM08: Excessive Agency`) before exposing them to autonomous agents.

## Security Checks
1. **Destructive Action Gate Check:** Flags any tool matching `delete`, `drop`, `terminate`, `send_email`, `transfer`, or `charge` that lacks an explicit human-approval or dry-run parameter.
2. **Unbounded SSRF / Shell Sink Detection:** Identifies unconstrained `url`, `command`, `shell`, or `sql` string parameters lacking allowlist `enum` or regex `pattern` constraints.

## CLI Usage
```bash
python mcp_schema_auditor.py --selftest
```
