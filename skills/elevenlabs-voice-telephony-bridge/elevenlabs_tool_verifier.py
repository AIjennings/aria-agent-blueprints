#!/usr/bin/env python3
"""
elevenlabs_tool_verifier.py
ElevenLabs Conversational AI Tool Schema Validator, Turn Latency Budgeter, and Outbound Call Gate.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from typing import Any, Dict, List

E164_REGEX = re.compile(r"^\+[1-9]\d{9,14}$")


def validate_convai_tool(tool_def: Dict[str, Any]) -> Dict[str, Any]:
    """Validates an ElevenLabs ConvAI standalone tool definition for production safety."""
    issues: List[str] = []
    tool_type = tool_def.get("type")
    name = str(tool_def.get("name", ""))
    if tool_type not in {"webhook", "client"}:
        issues.append(f"Unsupported tool type: {tool_type}")
    if not re.match(r"^[a-z][a-z0-9_]{2,63}$", name):
        issues.append("Tool name must be snake_case (3-64 chars)")
    if tool_type == "webhook":
        api_schema = tool_def.get("api_schema", {})
        url = str(api_schema.get("url", ""))
        if not url.startswith("https://"):
            issues.append("Webhook URL must use HTTPS")
        timeout_sec = int(tool_def.get("response_timeout_secs", 20))
        if timeout_sec > 15:
            issues.append(f"Webhook timeout ({timeout_sec}s) exceeds 15s voice stall threshold")
    return {
        "name": name,
        "valid": len(issues) == 0,
        "issues": issues,
    }


def evaluate_turn_latency(asr_ms: int, llm_ttft_ms: int, tts_ttfb_ms: int, tool_ms: int = 0) -> Dict[str, Any]:
    """Calculates total conversational turn latency and grades real-time responsiveness."""
    base_turn_ms = asr_ms + llm_ttft_ms + tts_ttfb_ms
    total_with_tool_ms = base_turn_ms + tool_ms
    grade = "EXCELLENT" if base_turn_ms <= 750 else ("ACCEPTABLE" if base_turn_ms <= 1100 else "HIGH_LATENCY")
    return {
        "base_turn_ms": base_turn_ms,
        "total_with_tool_ms": total_with_tool_ms,
        "grade": grade,
        "requires_filler_phrase": total_with_tool_ms > 900,
    }


def stage_outbound_call(e164_number: str, local_hour_24: int, human_approved: bool) -> Dict[str, Any]:
    """Stages an outbound voice call with E.164, quiet-hours, and HITL verification."""
    valid_number = bool(E164_REGEX.match(e164_number))
    within_window = 8 <= local_hour_24 < 20
    can_dial = valid_number and within_window and human_approved
    return {
        "destination": e164_number,
        "valid_e164": valid_number,
        "within_calling_window": within_window,
        "human_approved": human_approved,
        "dispatch_status": "READY_TO_DIAL" if can_dial else "HELD_FOR_REVIEW",
    }


def run_selftest() -> int:
    good_tool = {
        "type": "webhook",
        "name": "lookup_dispatch_status",
        "response_timeout_secs": 8,
        "api_schema": {"url": "https://api.ariawave.tech/v1/dispatch/status", "method": "POST"},
    }
    res = validate_convai_tool(good_tool)
    assert res["valid"] is True, f"Expected valid tool, got {res}"

    lat = evaluate_turn_latency(asr_ms=180, llm_ttft_ms=310, tts_ttfb_ms=190, tool_ms=420)
    assert lat["base_turn_ms"] == 680 and lat["grade"] == "EXCELLENT"
    assert lat["requires_filler_phrase"] is True

    call = stage_outbound_call("+12485550142", local_hour_24=14, human_approved=False)
    assert call["dispatch_status"] == "HELD_FOR_REVIEW", "Unapproved outbound call must be held"
    print("[PASS] elevenlabs_tool_verifier.py --selftest: all assertions passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="ElevenLabs ConvAI Tool Verifier & Latency Budgeter")
    parser.add_argument("--selftest", action="store_true", help="Run deterministic self-test")
    args = parser.parse_args()
    if args.selftest:
        return run_selftest()
    print(json.dumps({"status": "ready", "tool": "elevenlabs_tool_verifier.py"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
