---
name: documentation-adr
description: Maintain concise durable project documentation, runbooks, and architecture decision records that explain current truth and the reasons behind material decisions.
---

# Documentation & ADR

## Owner
Agent 26 — Documentation / Knowledge Engineer.

## Shared Use
Decision owners provide rationale and facts. Agent 26 records them without changing the underlying decision.

## Source Inspiration
Adapted from addyosmani/agent-skills documentation-and-adrs.

## Procedure
1. Inspect the project for an existing documentation/ADR convention and follow it.
2. Document the current truth; do not infer or invent missing behavior.
3. Prefer documentation that explains **why**, constraints, trade-offs, and operational consequences.
4. Write an ADR for material decisions that are expensive to reverse or likely to be questioned later.
5. ADRs should include, at minimum:
   - status;
   - context;
   - decision;
   - alternatives considered;
   - consequences.
6. Do not delete historical ADRs; supersede them with a new record when decisions change.
7. Keep README/runbooks focused on actions humans/agents actually need.
8. Remove duplicated or contradictory documentation when a single authoritative source exists.
9. Link to canonical specs/ADRs instead of copying long content.
10. Never put secrets, credentials, tokens, or private runtime values in documentation.
11. Use Graphify when relationship mapping can reduce broad file reading.

## Hard Stop
Do not make architecture, product, security, or implementation decisions while documenting them.
