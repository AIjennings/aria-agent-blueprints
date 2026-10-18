---
name: hid-access-control-provisioning
description: Standard operating procedure, Wiegand 26-bit (H10301) and 37-bit (H10302) bitstream parity encoder/decoder, 125kHz (009P) vs Seos carrier diagnostics, and structured ticket generation for HID physical access control systems.
version: 1.0.0
author: Aria Technology Group
metadata:
  hermes:
    tags: [physical-security, hid, wiegand, osdp, access-control]
---

# HID Access Control & Wiegand Credential Provisioning

Use this skill when diagnosing "Access Denied" reader events, decoding raw Wiegand hex/binary frames, or provisioning credentials across HID Signo, VertX, Aero, PDK, and Brivo door controllers.

## 1. Standard 26-Bit Wiegand (H10301) Frame Layout

- **Bit 0 (MSB):** Even parity over bits 1–12
- **Bits 1–8 (8 bits):** Facility Code (`0–255`)
- **Bits 9–24 (16 bits):** Card Number (`0–65,535`)
- **Bit 25 (LSB):** Odd parity over bits 13–24

## 2. Diagnostic Checklist for Unread Badges

1. **No Beep / No LED change on HID Signo:** Check if the fob is laser-marked `HID 009P` (125 kHz Prox). HID Signo 20/40 readers often ship with the 125 kHz LF carrier disabled; enable 125 kHz Proximity support via HID Reader Manager.
2. **Single Red Flash + "Unrecognized Format" in Controller Log:** Bit length mismatch (e.g., 37-bit Corporate 1000 presented to a 26-bit-only door profile) or parity bit corruption on long unshielded cable runs.
3. **Single Red Flash + "Facility Code Mismatch":** Replacement card batch uses a different Facility Code than the site profile.
