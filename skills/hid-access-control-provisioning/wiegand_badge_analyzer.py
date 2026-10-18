#!/usr/bin/env python3
"""
wiegand_badge_analyzer.py
Deterministic Wiegand 26-bit (H10301) Encoder/Decoder, Parity Verifier, and Access Control Diagnostic Tool.
Built by Aria Technology Group (https://www.ariawave.tech)
"""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass, asdict


@dataclass
class Wiegand26Frame:
    raw_hex: str
    raw_bits: str
    facility_code: int
    card_number: int
    even_parity_bit: int
    odd_parity_bit: int
    even_parity_valid: bool
    odd_parity_valid: bool
    frame_valid: bool


def encode_wiegand26(facility_code: int, card_number: int) -> Wiegand26Frame:
    if not (0 <= facility_code <= 255):
        raise ValueError("26-bit Wiegand facility_code must be 0..255")
    if not (0 <= card_number <= 65535):
        raise ValueError("26-bit Wiegand card_number must be 0..65535")

    payload24 = (facility_code << 16) | card_number
    upper12 = (payload24 >> 12) & 0xFFF
    lower12 = payload24 & 0xFFF

    even_parity = bin(upper12).count("1") % 2  # Makes total 1s in first 13 bits even
    odd_parity = 1 if (bin(lower12).count("1") % 2 == 0) else 0  # Makes total 1s in last 13 bits odd

    frame_int = (even_parity << 25) | (payload24 << 1) | odd_parity
    return decode_wiegand26(frame_int)


def decode_wiegand26(frame_int: int) -> Wiegand26Frame:
    if not (0 <= frame_int < (1 << 26)):
        raise ValueError("Frame exceeds 26 bits")
    bits = f"{frame_int:026b}"
    even_bit = int(bits[0])
    fc = int(bits[1:9], 2)
    cn = int(bits[9:25], 2)
    odd_bit = int(bits[25])

    upper13_ones = bits[0:13].count("1")
    lower13_ones = bits[13:26].count("1")
    even_ok = (upper13_ones % 2 == 0)
    odd_ok = (lower13_ones % 2 == 1)

    return Wiegand26Frame(
        raw_hex=f"0x{frame_int:07X}",
        raw_bits=bits,
        facility_code=fc,
        card_number=cn,
        even_parity_bit=even_bit,
        odd_parity_bit=odd_bit,
        even_parity_valid=even_ok,
        odd_parity_valid=odd_ok,
        frame_valid=(even_ok and odd_ok),
    )


def run_selftest() -> None:
    frame = encode_wiegand26(facility_code=105, card_number=42019)
    assert frame.frame_valid is True
    assert frame.facility_code == 105 and frame.card_number == 42019
    corrupted = decode_wiegand26(int(frame.raw_hex, 16) ^ 0x1)
    assert corrupted.frame_valid is False
    print(json.dumps({
        "selftest": "PASS",
        "encoded_frame": asdict(frame),
        "corrupted_parity_detected": not corrupted.frame_valid,
    }, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HID Wiegand 26-bit Credential Encoder/Decoder")
    parser.add_argument("--selftest", action="store_true", help="Run parity & frame verification suite")
    parser.add_argument("--fc", type=int, help="Facility code (0-255)")
    parser.add_argument("--card", type=int, help="Card number (0-65535)")
    args = parser.parse_args()
    if args.selftest or (args.fc is None or args.card is None):
        run_selftest()
    else:
        print(json.dumps(asdict(encode_wiegand26(args.fc, args.card)), indent=2))
