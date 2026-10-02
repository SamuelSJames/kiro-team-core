---
name: system-design-package
description: Produce the approved technical system design package before provisioning or coding.
---

# System Design Package

## Owner
Agent 14 — Technical Architect.

## Shared Use
Agent 01 routes the package. Agent 20 provisions from it.

## Required Inputs
Approved intake, approved numbered feature list, approved mockup when applicable, and relevant research findings.

## Steps
1. Define system boundaries and component responsibilities.
2. Select technologies and justify material choices.
3. Define interfaces, protocols, data flow, persistence boundaries, and integration contracts.
4. Define the Proxmox development topology required to build/test the system.
5. Record implementation sequence and major dependencies.
6. Produce/update:
   - SYSTEM_DESIGN.md
   - ARCHITECTURE.md
   - TECH_STACK.md
   - INTERFACES.md
   - DATA_FLOW.md when useful
   - DECISIONS.md for material choices
7. Verify the design is sufficient for Agent 20 and builders without guessing.
8. Hand back to Agent 01.

## Hard Stop
Do not provision infrastructure or implement application code.
