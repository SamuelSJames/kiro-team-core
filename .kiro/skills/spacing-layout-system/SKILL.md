---
name: spacing-layout-system
description: Establish and enforce coherent spacing, rhythm, density, alignment, and responsive whitespace across interfaces.
---

# Spacing & Layout System

## Owner
Agent 08 — UI / Visual Design Agent.

## Shared Use
Agents 05, 09, 11, 12, and 15 may consume and apply the spacing contract. Agent 08 owns changes to the spacing system.

## Source Inspiration
Adapted from design-token and responsive-layout patterns in wshobson/agents plus spacing guidance in addyosmani/agent-skills.

## Purpose
Prevent arbitrary padding/margin decisions and create consistent visual rhythm from page scale down to component internals.

## Procedure
1. Read the approved mockup and project `.design`.
2. Identify the project's density target: compact, standard, spacious, or explicitly mixed by context.
3. Establish a base spacing unit and a small named scale. Prefer existing project tokens; do not invent a second scale.
4. Distinguish:
   - **inset** spacing — padding inside a surface/component;
   - **stack** spacing — vertical distance between related elements;
   - **inline** spacing — horizontal distance between related elements;
   - **section** spacing — distance between major content groups;
   - **layout/gutter** spacing — page/column edges and grid gaps.
5. Use proximity to communicate relationship: tighter within a group, larger between groups.
6. Keep repeated components internally consistent.
7. Align edges to a deliberate grid/column/container system.
8. Avoid double-spacing where parent gap and child margins compound.
9. Prefer `gap` for sibling layout relationships; use margins for exceptional relationships rather than default structure.
10. Define responsive spacing with tokens, clamp(), container rules, or project breakpoints rather than random per-screen values.
11. Preserve minimum touch-target and readable-content constraints when tightening density.
12. Check optical balance: mathematically equal spacing may need small tokenized compensation around icons, headings, or asymmetric shapes.
13. Record final spacing tokens/rules in `.design` and DESIGN_TOKENS.md.
14. Agent 09 verifies rendered placement against the approved mockup; the spacing system does not override visual-fidelity evidence.

## Default Heuristic
If the project has no established scale, Agent 08 may propose a compact 4px-based scale for approval, but it must become an explicit project token system before implementation.

## Red Flags
- isolated 13px/19px/27px values with no approved reason;
- every section using the same large padding regardless of hierarchy;
- nested card padding compounding into excessive whitespace;
- inconsistent form/control gaps;
- centered elements whose optical balance is visibly wrong;
- mobile layouts retaining desktop section spacing unchanged.

## Hard Stop
Do not alter content hierarchy or UX flow merely to make spacing easier.
