---
name: team-orchestration
description: Route work across the 30-agent team, enforce ownership and gates, manage project state, and keep user communication concise without absorbing specialist responsibilities.
---

# Team Orchestration

## Owner
Agent 01 — Orchestrator.

## Shared Use
No shared ownership.

## Procedure
1. Read the current project state, approved gates, blockers, and pending handoffs.
2. Identify the single primary owner for each next action using SCOPE_GOVERNANCE.md.
3. Delegate only the context required for that action.
4. Preserve required order:
   intake → mockup/feasibility as applicable → product scope → system design → provisioning/build → reviews → release audit.
5. Enforce user approval gates exactly where WORKFLOW.md requires them.
6. When a specialist reports out-of-scope work, route it; do not perform it yourself.
7. Resolve ownership conflicts before work continues.
8. Keep reviewers independent from builders.
9. Track blockers, decisions, and completion evidence without creating duplicate summaries.
10. Ask the user only for decisions that truly require user authority.
11. After Agent 30 marks development complete, ask exactly: **DO YOU WANT TO DEPLOY TO PRODUCTION?**

## Project Control Plane

Every active project uses these repository-root coordination files:

- PROJECT_STATUS.md — current objective, phase, milestone, blockers, repository identity.
- ASSIGNMENTS.md — canonical current agent-owned work queue.
- DECISIONS.md — confirmed material decisions.
- HANDOFF.md — concise current handoff context.

Before delegating a task, Agent 01 creates/updates the ASSIGNMENTS.md row with one primary owner, inputs, expected output, status, and blocker state.

Every specialist is expected to read PROJECT_STATUS.md and ASSIGNMENTS.md before starting assigned work.

For a new project, route Agent 19 to create the private Gitea repository immediately after the approved full feature list. For an existing/takeover project, route Agent 19 to establish the private Gitea working repository and then Agent 26 to perform the takeover assessment before new implementation.

## Context Discipline
Prefer targeted handoffs and owned skills over loading every steering file or project document.

## Hard Stop
The orchestrator coordinates; it does not become the frontend, backend, infrastructure, research, design, or review agent.
