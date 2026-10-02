---
name: music-software-architecture
description: Define music-domain software boundaries, timing/audio/MIDI responsibilities, host integration seams, and real-time safety constraints beneath the approved system architecture.
---

# Music Software Architecture

## Owner
Agent 21 — Music Software Architect.

## Shared Use
Agents 22–25 consume the domain architecture. Agent 14 remains owner of overall system architecture.

## Procedure
1. Read approved system architecture, product behavior, and REAPER feasibility findings when applicable.
2. Partition the music domain into clear responsibilities:
   - audio/DSP;
   - MIDI/event handling;
   - host/REAPER integration;
   - UI/control layer;
   - persistence/presets;
   - OS/audio-platform boundary.
3. Define data/control flow between real-time and non-real-time components.
4. Identify hard real-time constraints and prohibit blocking operations on audio callbacks.
5. Define sample rate, block size, channel/layout, timestamp, and synchronization assumptions.
6. Define MIDI timing/routing assumptions separately from audio processing.
7. Define host integration boundaries without coupling domain logic unnecessarily to REAPER.
8. Define failure/fallback behavior for device loss, host disconnect, sample-rate change, and unavailable dependencies.
9. Record interfaces and domain decisions for Agents 22–25.
10. Route unresolved platform/REAPER feasibility questions through Agent 01.

## Hard Stop
Do not implement DSP, MIDI, REAPER scripts, or Linux audio configuration directly.
