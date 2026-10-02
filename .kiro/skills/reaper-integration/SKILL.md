---
name: reaper-integration
description: Implement approved REAPER-specific behavior using ReaScript, JSFX, OSC, Web Remote, extensions, actions, project data, or other validated integration mechanisms.
---

# REAPER Integration

## Owner
Agent 24 — REAPER Integration Engineer.

## Shared Use
Agent 21 supplies domain architecture. Agent 13 supplies feasibility evidence. Agents 22/23/25 provide DSP/MIDI/platform boundaries.

## Prerequisite
The mandatory REAPER feasibility gate must be complete for requested capabilities.

## Procedure
1. Read RESEARCH.md/DECISIONS.md and the approved REAPER integration contract.
2. Choose the least invasive validated mechanism:
   - ReaScript for project/action automation;
   - JSFX for in-host DSP/MIDI when appropriate;
   - OSC for external control;
   - Web Remote for browser-based control surfaces;
   - extension/plugin only when simpler mechanisms cannot satisfy the requirement.
3. Keep REAPER-specific code behind a clear boundary from reusable domain logic.
4. Validate project/track/item/FX identifiers and lifecycle assumptions.
5. Avoid polling when event/state mechanisms can provide reliable updates.
6. Handle project close/reload, transport stop/start, missing track/FX, and changed routing gracefully.
7. Test against the supported REAPER version/environment.
8. Record required actions, scripts, ports, paths, and user setup steps.
9. Route any capability that contradicts feasibility findings back through Agent 01.

## Hard Stop
Do not invent unsupported REAPER APIs or bypass feasibility limits with unverified assumptions.
