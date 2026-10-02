---
name: linux-audio-platform
description: Configure and diagnose Linux audio services, devices, routing, permissions, latency, and package/runtime dependencies for the approved project.
---

# Linux Audio Platform

## Owner
Agent 25 — Linux Audio Platform Engineer.

## Shared Use
Agents 21–24 consume platform guarantees. Agent 20 owns Proxmox infrastructure, not Linux audio configuration.

## Procedure
1. Identify the exact host/distro/session and audio stack in use.
2. Inventory ALSA devices and current PipeWire/JACK/Pulse compatibility state before changing configuration.
3. Confirm sample rate, channel count, profile, clock source, and device availability.
4. Prefer PipeWire-native configuration on modern Linux unless the approved project explicitly requires JACK-specific operation.
5. Check user groups, realtime limits, permissions, and service state.
6. Diagnose XRUNs/dropouts by isolating CPU scheduling, buffer size, device/USB, clock, and graph-routing causes.
7. Make the smallest reversible configuration change first.
8. Preserve system audio usability unless the project explicitly requires exclusive operation.
9. Verify audio after restart/login changes when required.
10. Record package/config/service changes and rollback steps.
11. Never hardcode machine-specific paths into reusable project logic without an abstraction/config layer.

## Hard Stop
Do not alter Proxmox networking/resources or music application behavior outside platform scope.
