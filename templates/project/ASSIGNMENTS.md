# Assignments

This is the current agent-owned work queue. Agent 01 maintains routing.

| Task ID | Primary Agent | Task | Inputs | Expected Output | Status | Blocker |
|---|---:|---|---|---|---|---|
| T-001 | 00 | <task> | <inputs> | <output> | TODO | None |

## Status Values
TODO · READY · IN_PROGRESS · BLOCKED · REVIEW · DONE

## Rules
- One primary owner per task.
- Agents read PROJECT_STATUS.md and this file before starting assigned work.
- Out-of-scope work is routed to Agent 01 instead of silently absorbed.
- DONE requires required durable changes to be committed/pushed/verified in Gitea.
