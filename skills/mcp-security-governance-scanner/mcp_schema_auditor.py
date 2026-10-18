#!/usr/bin/env python3
"""
mcp_schema_auditor.py
Deterministic Model Context Protocol (MCP) Tool-Schema Security & Excessive-Agency Auditor.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from typing import Any, Dict, List

DESTRUCTIVE_VERBS = re.compile(r"(delete|drop|destroy|send_email|charge_card|wire_transfer|execute_sql)", re.IGNORECASE)
DANGEROUS_PARAM_NAMES = {"command", "shell", "raw_sql", "target_url", "webhook_url"}


def audit_mcp_tools(tools: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Audits a list of MCP tool definitions for OWASP LLM07/LLM08 risks."""
    findings: List[Dict[str, str]] = []
    for tool in tools:
        name = str(tool.get("name", "unknown"))
        schema = tool.get("inputSchema", tool.get("parameters", {}))
        props = schema.get("properties", {})

        if DESTRUCTIVE_VERBS.search(name):
            has_gate = any(k in props for k in ("dry_run", "require_approval", "draft_only", "confirm_token"))
            if not has_gate:
                findings.append({
                    "tool": name,
                    "severity": "HIGH",
                    "rule": "OWASP-LLM08-EXCESSIVE-AGENCY",
                    "detail": "Destructive or external-action tool lacks dry_run / draft_only / require_approval parameter.",
                })

        for param_name, param_spec in props.items():
            if param_name.lower() in DANGEROUS_PARAM_NAMES:
                has_constraint = "enum" in param_spec or "pattern" in param_spec
                if not has_constraint:
                    findings.append({
                        "tool": name,
                        "severity": "CRITICAL",
                        "rule": "OWASP-LLM07-UNCONSTRAINED-SINK",
                        "detail": f"Parameter '{param_name}' accepts arbitrary unconstrained strings (SSRF/Injection risk).",
                    })

    return {
        "tools_scanned": len(tools),
        "finding_count": len(findings),
        "passed_governance": len(findings) == 0,
        "findings": findings,
    }


def run_selftest() -> int:
    unsafe_tools = [
        {
            "name": "delete_customer_account",
            "inputSchema": {"type": "object", "properties": {"account_id": {"type": "string"}}},
        },
        {
            "name": "run_remote_diagnostic",
            "inputSchema": {"type": "object", "properties": {"command": {"type": "string"}}},
        },
    ]
    report = audit_mcp_tools(unsafe_tools)
    assert report["finding_count"] == 2 and report["passed_governance"] is False

    safe_tools = [
        {
            "name": "send_email_notification",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "recipient": {"type": "string"},
                    "draft_only": {"type": "boolean", "default": True},
                },
            },
        }
    ]
    safe_report = audit_mcp_tools(safe_tools)
    assert safe_report["passed_governance"] is True
    print("[PASS] mcp_schema_auditor.py --selftest: all assertions passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="MCP Tool-Schema Security & Governance Auditor")
    parser.add_argument("--selftest", action="store_true", help="Run deterministic self-test")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()
    print(json.dumps({"status": "ready", "tool": "mcp_schema_auditor.py"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
