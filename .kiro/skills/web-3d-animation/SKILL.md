---
name: web-3d-animation
description: Design and implement performant browser-based 3D scenes, motion, and interaction using Three.js/WebGL patterns without sacrificing page usability or accessibility.
---

# Web 3D Animation

## Owner
Agent 12 — 3D / Interactive Visual Engineer.

## Shared Use
Agents 08 and 11 may define visual/motion intent. Agent 15 integrates the approved scene into the product shell. Agent 27 tests user-visible behavior.

## Source Inspiration
Adapted from Three.js/WebGL skills in magnus919/agent-skills and Emmraan/agent-skills.

## Procedure
1. Define the 3D scene's purpose before choosing effects: storytelling, product visualization, ambient depth, interaction, data visualization, or transition.
2. Decide whether 3D materially improves the experience; avoid 3D for decoration that harms performance or clarity.
3. Choose camera deliberately:
   - perspective for natural depth;
   - orthographic for technical/isometric composition.
4. Establish scene scale, coordinate system, lighting, materials, and asset budget.
5. Use GLTF/GLB for external models when appropriate; optimize geometry/textures before shipping.
6. Make animation time-based, never frame-count based.
7. Use requestAnimationFrame/render loops only while needed; pause or reduce work when offscreen.
8. Cap device pixel ratio and adapt quality for weaker devices when necessary.
9. Use instancing/LOD for repeated or distant objects.
10. Dispose geometries, materials, textures, render targets, and event handlers when scenes are replaced.
11. Use ResizeObserver/container dimensions and update renderer/camera projection on resize.
12. Keep pointer/raycast interaction scoped to intended selectable objects.
13. Respect `prefers-reduced-motion`; provide a usable non-animated/fallback experience.
14. Lazy-load below-fold 3D and code-split heavy Three.js modules where practical.
15. Validate CPU/GPU load, memory growth, responsiveness, and interaction on target browsers.

## Design Rule
3D motion must follow the approved mockup and project `.design` contract. It must not obscure primary content, navigation, form controls, or readability.

## Hard Stop
Do not introduce a heavy 3D stack when CSS/2D motion satisfies the approved design with materially lower complexity.
