# Kiro Team Core — Project Workflow

## Default Flow

1. Agent 02 completes and validates intake.
2. Agent 03 generates the number of mockups required by the intake.
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

## Living Design Contract

For projects with a visual UI, Agent 08 maintains a project-root `.design` living visual contract using the AgentsORG `design.v1` approach after the mockup is approved and before detailed UI implementation.

The precedence order is:

1. explicit current user instruction;
2. approved product scope;
3. approved mockup;
4. project `.design` contract;
5. generic design guidance.

The `.design` file captures approved tokens, component appearance, visual constraints, locked decisions, and related design rules so downstream agents do not re-invent the visual system. It does not replace the approved mockup or the deterministic 92% visual-fidelity gate.

## Visual Source of Truth

The explicitly approved mockup is the visual source of truth for the project.

The 92% visual threshold applies to the rendered implementation compared with the approved mockup.

For deterministic visual review, Agent 09 uses the global `visual-compare` utility. The canonical fidelity score is fixed:

```text
fidelity_score =
    SSIM              * 0.50
  + pixel_similarity  * 0.30
  + edge_similarity   * 0.20
```

The default pass threshold is **92.00**. Reference and actual images must use identical dimensions; the tool must not silently resize mismatched inputs. Agent 09 must set the Playwright viewport to the approved reference dimensions before capture. A dimension mismatch fails the visual gate until a valid same-size comparison is produced.

The score is deterministic evidence, not an AI opinion. Functional correctness, accessibility, responsive behavior, and security are separate gates and cannot be traded away to increase visual similarity.

Playwright screenshots and comparison artifacts are temporary by default and must follow `WORKSPACE_HYGIENE.md` after the comparison purpose is complete.

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


## SYSTEM DESIGN GATE

After the numbered feature list is approved and before provisioning or coding:

1. The Technical Architect creates the full System Design Package.
2. Research validates unresolved technical assumptions.
3. The Technical Architect finalizes the architecture.
4. SYSTEM_DESIGN.md and the Mermaid architecture diagram become implementation baselines.
5. Agent 20 provisions the Proxmox development environment from that design.
6. Builders begin only after the required development environment exists.

If any builder finds that the design cannot support implementation, the affected work stops and returns through Agent 01 to the Technical Architect.

Agent 20 owns ongoing Proxmox project resource management on pve3/pve4 during development.


## REAPER FEASIBILITY GATE

This gate is mandatory for any project that depends on REAPER behavior, REAPER control, REAPER data, or REAPER synchronization.

After Agent 02 completes intake and before mockup generation or feature definition:

1. Agent 13 receives the requested REAPER capabilities from the approved intake.
2. Agent 13 researches current REAPER capabilities and relevant integration methods, including ReaScript, OSC, Web Remote, JSFX, extensions, regions, markers, transport state, project data access, and other applicable mechanisms.
3. Each requested capability is classified as:
   - POSSIBLE;
   - POSSIBLE WITH LIMITATIONS;
   - REQUIRES WORKAROUND OR CUSTOM EXTENSION;
   - NOT CURRENTLY PRACTICAL.
4. Material limitations and required workarounds are recorded in RESEARCH.md and DECISIONS.md.
5. Agent 01 routes any material product-impacting limitation back through Agent 02 and, when needed, to the user.
6. Only after feasibility is sufficiently established may Agent 03 generate mockups and Agent 04 define the final feature list.

Do not design, approve, or implement a REAPER-dependent feature based on assumption alone.


## WORKSPACE & ARTIFACT HYGIENE GATE

`WORKSPACE_HYGIENE.md` is a global rule for every project and every agent.

For any task that creates or clones local working files:

1. The authoritative durable copy must live in the project's GitHub or Gitea repository.
2. Local repository content exists only while active work requires it.
3. Required durable changes must be committed, pushed, and verified remotely before cleanup.
4. Temporary clones, source trees, generated images, screenshots, visual diffs, build outputs, downloads, logs, exports, and other task artifacts must be removed when their purpose is complete.
5. After cleanup, the local project directory may retain only the required project directory structure, required Kiro metadata, and Markdown files necessary for the agents.
6. Cleanup must be based on task state and purpose, never age alone.
7. No cleanup may delete unpushed or otherwise unverified durable work.

A task that creates local working material is not complete until durable work is pushed and verified and temporary material is cleaned.
