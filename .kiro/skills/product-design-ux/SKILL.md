---
name: product-design-ux
description: Translate approved product scope into information architecture, user flows, interaction states, recovery behavior, and framework-neutral interface contracts.
---

# Product Design & UX

## Owner
Agent 05 — UX / Product Design Agent.

## Shared Use
Agents 06, 08, 15, and 27 consume UX outputs within their own scopes.

## Source Inspiration
Adapted from magnus919/agent-skills product-design-and-ux.

## Procedure
1. Read the approved feature list and validated intake.
2. Identify users/roles, tasks, entry points, goals, permissions, and completion outcomes.
3. Define information architecture and navigation from task needs.
4. Model critical user flows end-to-end, including:
   - decision points;
   - interruption/re-entry;
   - cancellation;
   - irreversible actions;
   - errors and recovery;
   - permission differences;
   - completion evidence.
5. Inventory required interface states: loading, empty, error, offline/degraded, success, partial, permission denied, and destructive confirmation where relevant.
6. Define interaction contracts without choosing visual styling.
7. Specify responsive/reflow behavior at the interaction level.
8. Identify accessibility structure requirements early.
9. Define observable UX acceptance criteria.
10. Hand interface wording to Agent 06 and visual appearance to Agent 08.

## Output
UX_SPEC.md, USER_FLOWS.md, STATE_MODEL.md, and interaction acceptance criteria.

## Hard Stop
Do not choose brand styling, colors, typography, implementation framework, or backend behavior.
