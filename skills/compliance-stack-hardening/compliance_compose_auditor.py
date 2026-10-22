#!/usr/bin/env python3
"""
compliance_compose_auditor.py
Deterministic SOC 2 (CC6.1 / CC7.2 / CC8.1 / A1.2) Docker Compose & reverse-proxy
hardening auditor by Aria Technology Group (https://www.ariawave.tech).
Zero external dependencies (Python 3.10+ stdlib only).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_HEADERS = {
    "x-frame-options": "SAMEORIGIN",
    "x-content-type-options": "nosniff",
    "referrer-policy": "strict-origin-when-cross-origin",
}

_PORT_RE = re.compile(r'^\s*-\s*["\']?([^"\']+)["\']?\s*$')
_IMAGE_RE = re.compile(r'^\s*image:\s*["\']?(\S+?)["\']?\s*$')
_DEBUG_TRUE_RE = re.compile(r'(?:DJANGO_DEBUG|APP_DEBUG)\s*[:=]\s*["\']?(?:true|1|yes)["\']?', re.IGNORECASE)


def audit_compose_text(compose_text: str) -> dict[str, Any]:
    """Audit a docker-compose YAML text for SOC 2 hardening controls."""
    findings: list[dict[str, str]] = []
    lines = compose_text.splitlines()

    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        # 1. Check port bindings (NET-01 / CC6.1)
        m_port = _PORT_RE.match(line)
        if m_port:
            val = m_port.group(1).strip()
            # Match port mappings like "8443:8443" or "0.0.0.0:8443:8443"
            if re.match(r'^(?:\d+\.\d+\.\d+\.\d+:)?\d+:\d+(?:/(?:tcp|udp))?$', val):
                if not val.startswith("127.0.0.1:"):
                    findings.append({
                        "control": "NET-01",
                        "soc2_criteria": "CC6.1",
                        "severity": "HIGH",
                        "line": str(idx),
                        "detail": f"Port mapping '{val}' is not bound to 127.0.0.1",
                    })

        # 2. Check debug flags (APP-01 / CC7.2)
        if _DEBUG_TRUE_RE.search(stripped):
            findings.append({
                "control": "APP-01",
                "soc2_criteria": "CC7.2",
                "severity": "HIGH",
                "line": str(idx),
                "detail": f"Debug mode enabled in configuration: '{stripped}'",
            })

        # 3. Check mutable :latest image tags without @sha256 digest (CNT-01 / CC8.1)
        m_img = _IMAGE_RE.match(line)
        if m_img:
            img = m_img.group(1)
            if "@sha256:" not in img and (img.endswith(":latest") or ":" not in img.split("/")[-1]):
                findings.append({
                    "control": "CNT-01",
                    "soc2_criteria": "CC8.1",
                    "severity": "MEDIUM",
                    "line": str(idx),
                    "detail": f"Image '{img}' uses mutable tag without @sha256 digest pin",
                })

    # 4. Check log rotation presence (LOG-01 / CC7.2 & A1.2)
    if "max-size" not in compose_text or "max-file" not in compose_text:
        findings.append({
            "control": "LOG-01",
            "soc2_criteria": "CC7.2 / A1.2",
            "severity": "LOW",
            "line": "global",
            "detail": "Missing Docker log rotation options (max-size / max-file)",
        })

    return {
        "compliant": len(findings) == 0,
        "finding_count": len(findings),
        "findings": findings,
    }


def audit_proxy_headers(headers: dict[str, str]) -> dict[str, Any]:
    """Verify reverse-proxy HTTP response headers against SOC 2 CC6.1/CC7.2."""
    lower = {k.lower(): v.strip() for k, v in headers.items()}
    missing_or_weak: list[str] = []
    for req_key, expected in REQUIRED_HEADERS.items():
        actual = lower.get(req_key, "")
        if actual.lower() != expected.lower():
            missing_or_weak.append(f"{req_key} (expected '{expected}', got '{actual or 'missing'}')")
    if "server" in lower and lower["server"]:
        missing_or_weak.append(f"server banner exposed ('{lower['server']}')")
    return {
        "compliant": len(missing_or_weak) == 0,
        "issues": missing_or_weak,
    }


def run_selftest() -> int:
    vulnerable_compose = """
services:
  backend:
    image: ghcr.io/intuitem/ciso-assistant-community/backend:latest
    environment:
      - DJANGO_DEBUG=True
    ports:
      - "8443:8443"
"""
    res_vuln = audit_compose_text(vulnerable_compose)
    assert not res_vuln["compliant"], "Expected vulnerable compose to fail"
    controls = {f["control"] for f in res_vuln["findings"]}
    assert {"NET-01", "APP-01", "CNT-01", "LOG-01"}.issubset(controls), f"Missing controls: {controls}"

    hardened_compose = """
services:
  backend:
    image: ghcr.io/intuitem/ciso-assistant-community/backend@sha256:0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    environment:
      - DJANGO_DEBUG=False
    ports:
      - "127.0.0.1:8443:8443"
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
"""
    res_hard = audit_compose_text(hardened_compose)
    assert res_hard["compliant"], f"Expected hardened compose to pass, got: {res_hard}"

    bad_hdrs = {"X-Frame-Options": "SAMEORIGIN", "Server": "Caddy"}
    assert not audit_proxy_headers(bad_hdrs)["compliant"]

    good_hdrs = {
        "X-Frame-Options": "SAMEORIGIN",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
    assert audit_proxy_headers(good_hdrs)["compliant"]
    print("[PASS] compliance_compose_auditor.py --selftest: all SOC 2 CC6.1/CC7.2/CC8.1 assertions passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="SOC 2 Docker Compose & Proxy Hardening Auditor")
    parser.add_argument("--selftest", action="store_true", help="Run built-in deterministic assertions")
    parser.add_argument("--compose", type=str, help="Path to docker-compose.yml to audit")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    if args.selftest:
        return run_selftest()
    if args.compose:
        text = Path(args.compose).read_text(encoding="utf-8")
        result = audit_compose_text(text)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Compliant: {result['compliant']} ({result['finding_count']} findings)")
            for f in result["findings"]:
                print(f"  [{f['severity']}] {f['control']} ({f['soc2_criteria']}) line {f['line']}: {f['detail']}")
        return 0 if result["compliant"] else 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
