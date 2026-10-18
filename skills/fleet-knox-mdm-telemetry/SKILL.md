---
name: fleet-knox-mdm-telemetry
description: Samsung Knox Zero-Touch rugged tablet kiosk policy validator, Samsara ELD hours-of-service & J1939 fault webhook normalizer, and driver custody receipt tracker.
version: 1.0.0
author: Aria Technology Group
metadata:
  hermes:
    tags: [fleet, samsung-knox, samsara, mdm, logistics, android-enterprise]
---

# Enterprise Fleet Telemetry, Knox MDM & Driver Dispatch Assistant

Use this skill when deploying rugged commercial driver tablets (Samsung Galaxy Tab Active series), enforcing Knox kiosk containment, or integrating Samsara ELD telemetry and hardware custody receipts.

## 1. Zero-Touch Knox Kiosk Policy Requirements

- **Locked Kiosk Allowlist:** Only ELD (`com.samsara.driver`), navigation, and dispatch apps are permitted in foreground kiosk mode.
- **Location & Telemetry Persistence:** `location_mode: HIGH_ACCURACY`, `lock_location_settings: true`, and `usb_debugging_enabled: false`.
- **Hardware Custody Chain:** Every tablet IMEI and serial number is paired with a signed driver receipt record before field handoff.
