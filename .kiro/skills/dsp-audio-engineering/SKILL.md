---
name: dsp-audio-engineering
description: Implement and validate real-time audio processing, DSP algorithms, parameter smoothing, metering, and signal-flow behavior within approved music architecture.
---

# DSP / Audio Engineering

## Owner
Agent 22 — DSP / Audio Engineer.

## Shared Use
Agent 21 supplies architecture. Agents 24 and 25 consume compatible interfaces/platform assumptions. Agent 27 may test non-subjective behavior.

## Procedure
1. Read the approved music architecture and required signal behavior.
2. Define sample-rate, block-size, channel-layout, latency, and precision assumptions.
3. Keep real-time callbacks free of blocking I/O, locks, dynamic allocation where avoidable, and unbounded work.
4. Implement gain/filter/dynamics/effects/math with numerically stable algorithms.
5. Smooth user-controlled parameters that would otherwise zipper/click.
6. Bound parameters and sanitize invalid/NaN/Inf states.
7. Define bypass behavior and state reset behavior explicitly.
8. Measure latency and CPU cost for performance-sensitive paths.
9. Test across relevant sample rates and buffer sizes.
10. Verify silence, impulse, extreme parameter, and channel-layout cases.
11. Record algorithm assumptions and any audible/technical trade-offs.

## Hard Stop
Do not change product behavior, MIDI mapping, REAPER integration, or Linux device configuration outside the approved architecture.
