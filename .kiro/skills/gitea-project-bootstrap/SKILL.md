---
name: gitea-project-bootstrap
description: Create or import the durable project repository in the user's private Gitea, seed the project control files, verify the remote, and establish the repository as the project's source of truth.
---

# Gitea Project Bootstrap

## Owner
Agent 19 — DevOps / CI-CD Engineer.

## Shared Use
Agent 01 supplies the approved project identity/scope and consumes the repository result. Agent 26 may organize project knowledge after the repository exists.

## Tool
Use the attached Gitea MCP for repository creation/import and remote verification. Use shell/git only for the temporary working copy.

## New Project Trigger
Run immediately after:
1. intake is validated;
2. vision and goals are recorded;
3. the complete numbered feature list is explicitly approved.

Do not wait for implementation to begin before creating the durable repository.

## New Project Procedure
1. Derive a concise repository name from the approved project name.
2. Create a **private** Gitea repository unless the user explicitly requests public visibility.
3. Create a temporary local working copy.
4. Seed the project control plane:
   - README.md
   - PROJECT_STATUS.md
   - ASSIGNMENTS.md
   - DECISIONS.md
   - HANDOFF.md
5. Record the approved vision, goals, and numbered feature baseline without inventing technical architecture.
6. Add a minimal .gitignore appropriate to the known project type; never include secrets.
7. Make the initial commit.
8. Push to Gitea.
9. Verify the remote repository contains the commit and control files.
10. Hand the repository identity/clone target back to Agent 01.
11. Remove the temporary clone when no longer required.

## Existing / Takeover Project Procedure
When the requested source is an existing private or public repository:
1. Identify the exact source repository and branch.
2. Establish the user's private Gitea repository as the durable working repository before material modifications.
3. Import/mirror or clone-and-push the source history as appropriate.
4. Preserve upstream attribution, license, and original remote information when applicable.
5. Do not overwrite an existing Gitea repository without verifying identity and intent.
6. Verify the imported repository remotely.
7. Hand off to Agent 26 for takeover assessment before feature implementation resumes.

## Source-of-Truth Rule
All project code, assets, tests, configuration, and durable project documents belong in the project's Gitea repository. They never belong in `kiro-team-core`.

## Hard Stop
Do not create a repository before the required new-project product gate, delete/replace an existing remote, change visibility to public, or rewrite imported history without explicit authorization.
