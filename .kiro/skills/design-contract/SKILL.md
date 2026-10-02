---
name: design-contract
description: Create, maintain, and enforce a project .design living visual contract for UI projects using the AgentsORG design.v1 approach.
---

# .design Living Visual Contract

## Owner
Agent 08 — UI / Visual Design Agent.

## Shared Use
Agents 05, 06, 07, 09, 15, 27, and 30 may read and follow the contract. Agent 08 remains the primary owner of visual-system changes.

## Purpose
Keep approved visual decisions machine-readable and consistent across agent sessions so builders do not repeatedly invent colors, spacing, typography, components, or interaction appearance.

## Contract
For UI projects, maintain a single project-root `.design` file using the AgentsORG `design.v1` living-contract approach.

The project `.design` contract is subordinate to:
1. explicit current user instruction;
2. approved product scope;
3. the explicitly approved mockup.

Within those boundaries, `.design` is the normative visual-system contract for implementation and review.

## Minimum Content
Capture only what the project actually needs:
- identity and status;
- intent / visual direction;
- design tokens: color, typography, spacing, radius, elevation, motion when applicable;
- component appearance and usage rules;
- responsive visual rules;
- voice/copy rules when supplied by Agents 06/07;
- constraints and anti-patterns;
- locked decisions that should not drift;
- relevant assets/integrations.

Do not invent brand or product decisions that belong to another agent.

## Lifecycle
Use the design.v1 lifecycle concept:
- bootstrap — initial contract from approved inputs;
- refine — fill in validated details;
- lock — mark approved design decisions that must not drift;
- evolve — update only through an approved design/scope change.

## Steps
1. Read the approved mockup, UX outputs, brand rules, product spec, and existing `.design` if present.
2. Create or update one project-root `.design` contract.
3. Preserve existing approved/locked decisions unless an authorized change supersedes them.
4. Record tokens and component rules precisely enough for Agent 15 to implement without visual guessing.
5. Require UI implementation agents to read `.design` before styling or restyling.
6. Require Agent 09 to compare the rendered result against the approved mockup; `.design` does not replace the 92% visual-fidelity gate.
7. Keep the contract concise; do not duplicate long rationale already stored elsewhere unless it materially guides design decisions.
8. Commit the project `.design` file to the project's own durable repository when it is part of the approved project source.

## Hard Stop
Do not use `.design` to redesign an approved mockup, alter product behavior, or override current explicit user direction.
