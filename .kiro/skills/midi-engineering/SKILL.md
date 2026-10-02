---
name: midi-engineering
description: Implement deterministic MIDI parsing, routing, mapping, timing, state, and feedback behavior without conflating MIDI control with audio processing.
---

# MIDI Engineering

## Owner
Agent 23 — MIDI Engineer.

## Shared Use
Agents 21 and 24 consume MIDI contracts. Agent 22 consumes timing/control inputs where architecture requires it.

## Procedure
1. Read approved MIDI behavior, device assumptions, and music architecture.
2. Define supported message types and channel semantics explicitly.
3. Parse malformed/partial input defensively.
4. Preserve timing information and avoid unnecessary quantization.
5. Keep mapping/state rules deterministic and documented.
6. Define note-on/note-off, CC, pitch-bend, program-change, aftertouch, NRPN/RPN, SysEx, clock, transport, or MPE behavior only when required.
7. Handle duplicate, out-of-order, disconnected, and reconnect states.
8. Prevent stuck notes through clear lifecycle/reset behavior.
9. Separate learn/mapping configuration from runtime event processing.
10. Test boundary values, multi-channel cases, rapid event bursts, and device reconnect.
11. Record routing/mapping contracts for REAPER/host integration.

## Hard Stop
Do not redefine DSP, UX, or host behavior merely to simplify MIDI implementation.
