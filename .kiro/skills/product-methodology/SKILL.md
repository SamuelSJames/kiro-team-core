---
name: product-methodology
description: Turn validated intake, evidence, and research into a complete numbered feature baseline, prioritization, scope boundaries, and product decisions without taking over UX or technical architecture.
---

# Product Methodology

## Owner
Agent 04 — Product Architect.

## Shared Use
Agents 01, 05, 13, and 14 may consume the approved product baseline. They do not own product scope.

## Source Inspiration
Adapted from magnus919/agent-skills product-methodology, narrowed to Kiro Team Core's approval gates and ownership model.

## Prerequisites
Validated intake, approved mockup when applicable, and relevant bounded research.

## Procedure
1. Confirm the validated user problem, target users, goals, constraints, and evidence.
2. Convert the intake into explicit product behaviors and outcomes.
3. Draft a numbered feature list with one testable capability per item.
4. Separate:
   - required features;
   - optional add-ons;
   - explicit exclusions;
   - unresolved product questions.
5. Use prioritization only when needed:
   - MoSCoW for bounded release scope;
   - RICE only when comparing independent proposals with meaningful evidence.
6. Send uncertain market/technical assumptions to Agent 13 for bounded research.
7. Record important product decisions, trade-offs, and expected outcomes in PRODUCT_SPEC.md / DECISIONS.md.
8. Check for hidden edge cases, permissions, recovery behavior, and non-happy paths.
9. Present the numbered feature list for explicit user approval.
10. After approval, freeze it as the product scope baseline until a formal scope change occurs.

## Output
PRODUCT_SPEC.md and an approved numbered feature list.

## Hard Stop
Do not define visual layout, UX flow, technical architecture, database design, or implementation details.
