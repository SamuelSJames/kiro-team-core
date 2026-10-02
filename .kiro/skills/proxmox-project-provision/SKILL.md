---
name: proxmox-project-provision
description: Provision and manage authorized pve3/pve4 development resources from an approved system design.
---

# Proxmox Project Provision

## Owner
Agent 20 — Proxmox Infrastructure Engineer.

## Shared Use
Agent 19 may consume environment records for CI/CD. No other agent provisions Proxmox resources.

## Prerequisite
Approved SYSTEM_DESIGN.md with sufficient resource requirements.

## Steps
1. Read the approved system design and project resource requirements.
2. Confirm scope is limited to authorized pve3/pve4 development resources.
3. Check capacity and existing project inventory.
4. Provision only the required VMs/LXCs, networking, storage, templates, and snapshots.
5. Use reproducible names and record resource identifiers.
6. Verify service reachability and expected resource state.
7. Update INFRASTRUCTURE.md/environment records.
8. Route architecture gaps back through Agent 01 instead of guessing.

## Hard Stop
Destructive, cluster-wide, identity, storage-destruction, production, or irreversible operations require the applicable explicit authorization safeguard.
