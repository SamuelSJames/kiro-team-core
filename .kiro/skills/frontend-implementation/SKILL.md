---
name: frontend-implementation
description: Implement approved browser-facing features as accessible, responsive, maintainable UI without redefining product, UX, or visual design.
---

# Frontend Implementation

## Owner
Agent 15 — Frontend Engineer.

## Shared Use
Agent 27 may consume implementation structure during QA. Agent 29 may inspect it during review.

## Source Inspiration
Adapted from production UI engineering patterns in addyosmani/agent-skills, narrowed to Kiro Team Core ownership boundaries.

## Prerequisites
Approved product behavior, architecture, UX/UI direction, and project `.design` contract when present.

## Procedure
1. Read the approved feature behavior, interface contract, mockup, and `.design`.
2. Identify the smallest component/page boundaries that match the architecture.
3. Separate data access/state orchestration from presentational rendering.
4. Prefer composition and focused components over large configuration-heavy components.
5. Implement loading, empty, error, success, permission, and disabled states where applicable.
6. Use semantic HTML first; add ARIA only where native semantics are insufficient.
7. Preserve keyboard navigation and visible focus.
8. Implement responsive behavior from project rules rather than ad-hoc breakpoints.
9. Use design tokens; avoid arbitrary visual values when a project token exists.
10. Run the project lint/type/test/build checks.
11. Use Playwright for implementation-side browser inspection when needed.
12. Hand visual-fidelity measurement to Agent 09 and independent behavior QA to Agent 27.

## Quality Rules
- Do not redesign an approved mockup.
- Do not invent backend behavior or database contracts.
- Do not hide missing states behind placeholder UI.
- Do not weaken accessibility to match appearance.
- Do not use generic visual defaults when the project has an approved design system.

## Hard Stop
If implementation requires a product, UX, visual, API, database, or architecture change, stop that portion and route through Agent 01.
