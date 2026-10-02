---
name: interaction-motion-design
description: Design and implement purposeful UI motion, microinteractions, transitions, feedback, and advanced custom controls that preserve usability and reduced-motion support.
---

# Interaction & Motion Design

## Owner
Agent 11 — Custom UI / Motion Engineer.

## Shared Use
Agents 05 and 08 define behavior/visual intent. Agent 15 integrates approved implementation. Agent 27 validates behavior.

## Source Inspiration
Adapted from wshobson/agents interaction-design.

## Procedure
1. Identify the purpose of motion: feedback, orientation, focus, continuity, or state change.
2. Do not animate solely because motion is available.
3. Define motion tokens for duration, easing, and delay rather than one-off values.
4. Prefer transform and opacity for performance where possible.
5. Make transitions interruptible; never block user control unnecessarily.
6. Preserve layout stability during loading/state changes.
7. Use skeletons/progress only when they accurately communicate wait/state.
8. Respect `prefers-reduced-motion` and provide a usable reduced/no-motion behavior.
9. Avoid motion that obscures focus, content, or error feedback.
10. Clean event listeners/timers/animation resources on unmount.
11. Validate on realistic devices and browser sizes.
12. Record durable motion rules in `.design` when they become part of the visual system.

## Hard Stop
Do not alter UX flow or product behavior merely to support an animation.
