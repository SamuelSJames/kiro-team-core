---
name: project-takeover-assessment
description: Assess an existing project repository, determine its current state against the end objective, organize durable project knowledge, and produce a concrete completion map before new implementation begins.
---

# Project Takeover Assessment

## Owner
Agent 26 — Documentation / Knowledge Engineer.

## Shared Use
Agent 19 establishes the Gitea working repository first. Agents 13, 14, 27, and 29 may provide bounded research, architecture, QA, or code-review evidence. Agent 01 owns routing after the assessment.

## Prerequisite
The project must already exist in the user's private Gitea as the durable working repository.

## Procedure
1. Read the stated end objective, approved requirements if available, and repository history.
2. Inspect the repository structure, README/docs, manifests, configuration, tests, CI, migrations, and current branch state.
3. Run Graphify over the active project to map code/docs/config/schema relationships.
4. Identify the detected stack, entry points, major modules, data stores, integrations, build/test commands, and deployment assumptions.
5. Run only safe, non-destructive discovery checks needed to understand current state.
6. Separate findings into:
   - completed and working;
   - present but incomplete;
   - present but failing;
   - missing relative to the end objective;
   - unknown / requires specialist validation.
7. Identify stale, duplicate, contradictory, or misplaced documentation. Organize knowledge without restructuring application code merely for neatness.
8. Create/update:
   - PROJECT_STATUS.md — current phase, objective, blockers, next milestone;
   - ASSIGNMENTS.md — current agent-owned work queue;
   - docs/PROJECT_MAP.md — structure, stack, modules, interfaces, commands;
   - docs/TAKEOVER_ASSESSMENT.md — evidence-based gap assessment;
   - DECISIONS.md — only confirmed decisions;
   - HANDOFF.md — immediate routing context.
9. Preserve existing useful conventions instead of forcing a new structure when the current one is coherent.
10. Route architecture uncertainty to Agent 14, external assumptions to Agent 13, behavior verification to Agent 27, and code-quality/architecture-conformance questions to Agent 29.
11. Return a completion map to Agent 01 ordered by dependencies, not by arbitrary file order.

## Completion Standard
The team should be able to answer:
- What is this project supposed to become?
- What already works?
- What is incomplete or broken?
- What remains to reach the end objective?
- Which agent owns each next piece of work?
- Where is the authoritative repository and project state?

## Hard Stop
Do not rewrite architecture, refactor application code, or declare features complete based only on static presence. Record uncertainty and route verification to the owning specialist.
