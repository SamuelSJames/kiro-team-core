---
name: repository-work-cycle
description: Perform project work from a designated repository while keeping the global Kiro framework and temporary local workspace cleanly separated.
---

# Repository Work Cycle

## Owner
Agent 19 — DevOps / CI-CD Engineer.

## Shared Use
Builders and reviewers may follow this procedure. Use does not transfer repository or deployment ownership.

## Repository Separation
- `SamuelSJames/kiro-team-core` is only the canonical source for the global Kiro framework.
- Never commit application/project source into `kiro-team-core`.
- A project's durable repository is the repository designated for that project, normally Gitea unless the user explicitly chooses another target.
- The installed `~/.kiro` runtime is not required to remain a Git working tree.

## Steps
1. Identify the project's designated repository before making durable code changes.
2. Create/clone a temporary working copy only for the active task.
3. Perform and validate the assigned work.
4. Commit durable changes to the project repository only.
5. Push and verify the remote state.
6. Confirm no required untracked or unpushed work remains.
7. Remove temporary clone/worktree and generated artifacts whose purpose is complete.
8. Preserve only required local project Markdown/Kiro metadata allowed by workspace policy.

## Hard Stop
Never delete unpushed work. Never redirect project source into the Kiro framework repository.
