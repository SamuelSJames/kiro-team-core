# Kiro Team Core — Project Workflow

## Default Flow

1. Agent 02 completes and validates intake.
2. Agent 29 generates the number of mockups required by the intake.
3. USER APPROVAL GATE: no build begins until the user explicitly approves the required mockup set.
4. Rejected mockups are deleted and regenerated from user feedback.
5. If mockup feedback changes broad scope, Agent 02 updates and revalidates the intake.
6. The Product Architect creates a complete numbered feature list from the approved intake and mockup.
7. The Research Agent performs bounded supporting research and returns evidence-based missing-feature or add-on suggestions.
8. The Product Architect finalizes required features and clearly separated optional add-ons.
9. USER FEATURE APPROVAL GATE: the user must explicitly approve the numbered feature list before technical architecture begins.
10. The approved numbered feature list becomes the project scope baseline. Later material changes require scope-change handling.
11. The Technical Architect defines the technical architecture from the approved intake, mockup, and feature list.
12. Development architecture defaults to the authorized Proxmox environment on pve3/pve4 unless the intake explicitly requires another target.
13. Only one development system design is required by default: the Proxmox development design.
14. Builders implement the project in the Proxmox development environment.
15. Visual implementations must be reviewed against the approved mockup and achieve at least 92% visual similarity before release approval.
16. Independent review verifies function, security, and architecture/code quality.
17. The Release / Completion Auditor performs the final completion audit.
18. After project completion, ask the user exactly: **DO YOU WANT TO DEPLOY TO PRODUCTION?**
19. Only after a YES is production architecture designed.
20. AWS is the default production architecture target unless the intake or user specifies another target.
21. Linode/Akamai is an alternative production target when selected.

## Visual Source of Truth

The explicitly approved mockup is the visual source of truth for the project.

The 92% visual threshold applies to the rendered implementation compared with the approved mockup. Functional correctness, accessibility, responsive behavior, and security are separate gates and cannot be traded away to increase visual similarity.

## Resource Rule

Do not design production infrastructure during initial development unless the intake explicitly requires it. This avoids unnecessary work and resource use.


## Research Checkpoints

Research is a bounded support function and is invoked at four checkpoints:

1. **Feature Definition**
   - Product Architect sends draft features to Research.
   - Research returns expected capabilities, gaps, and evidence-based add-on suggestions.

2. **Technical Architecture**
   - Technical Architect sends unresolved technical questions to Research before committing to uncertain technologies or platforms.

3. **Integration / API**
   - Integration / API Engineer sends external-provider questions to Research before implementation when provider behavior, limits, auth, pricing constraints, deprecations, or compatibility are uncertain.

4. **Pre-Release Validation**
   - Before final completion audit, Research verifies critical external assumptions that could have changed during development.

Research must always return findings to the owning agent. Research does not own product scope, architecture, integrations, or release decisions.
