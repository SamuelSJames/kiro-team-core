# Kiro Team Core — Workspace & Artifact Hygiene

This policy is global for every project managed by the Kiro team.

## Repository Is the Source of Truth

Every project must live primarily in a Git repository, normally GitHub or Gitea.

Durable project material belongs in the repository, including:

- application/source code;
- tests;
- configuration that is safe to version;
- approved visual assets;
- approved documentation;
- build/deployment definitions;
- other files required to reconstruct or continue the project.

A local project directory is a temporary working location, not the authoritative project store.

## Minimal Local Project Directory

After active work is complete, the local project directory may retain only:

- the required directory structure;
- project/agent Markdown files required for Kiro operation;
- minimal Kiro metadata required to identify or manage the project.

Normal source trees, generated assets, build outputs, downloaded dependencies, temporary clones, screenshots, visual diffs, test artifacts, exports, logs, and other working files must not remain locally after their purpose is complete.

## Clone → Work → Push → Verify → Clean

When an agent needs repository content:

1. Clone, fetch, pull, or create only the files required for the task.
2. Perform the work locally.
3. Test and validate the work.
4. Commit all durable changes.
5. Push the commit to the authoritative GitHub or Gitea repository.
6. Verify that the remote push succeeded and that required durable files exist remotely.
7. Verify that no required untracked or unpushed files remain.
8. Remove the temporary local working files or clone.
9. Leave only the permitted minimal project structure and required Markdown/Kiro metadata.

Cleanup is part of task completion.

## Purpose Rule for Every Generated File

Every generated file must have a defined:

- project or task;
- purpose;
- owner;
- destination;
- retention requirement.

Do not create or retain files merely because a tool can generate them.

If the purpose is temporary, delete the file completely when that purpose is finished.

If the file becomes a durable project asset or required evidence, place it in the appropriate repository path, commit it, push it, verify the remote copy, and then remove the temporary local copy.

## Images, Mockups, Screenshots, and Visual Diffs

Generated visual files are temporary by default.

This includes:

- image-generation outputs;
- rejected or superseded mockups;
- Playwright screenshots;
- browser captures;
- visual-comparison inputs;
- diff images;
- amplified diff images;
- intermediate image conversions.

Keep a visual file only while it is needed for its active task.

When the task or review cycle finishes:

- if the file is an approved durable project asset or required project evidence, commit and push it to the repository;
- otherwise delete it completely.

Rejected, superseded, abandoned, or failed-generation artifacts must be deleted as soon as they no longer serve an active debugging or review purpose.

## Temporary Shared Storage

Shared locations such as `/opt/mcp/data/` are temporary working storage, not permanent project archives.

Temporary artifacts should be associated with a project and task when practical, for example:

```text
/opt/mcp/data/tasks/
└── <project-id>/
    └── <task-id>/
        ├── generated/
        ├── screenshots/
        └── diffs/
```

A task is not complete until its temporary shared-storage artifacts have been either:

1. promoted into the authoritative repository and verified there; or
2. deleted.

Shared storage must not become an accumulation point for unrelated or completed artifacts.

## Cleanup by Task State, Not File Age

Never decide that a file is safe to delete merely because it is old.

Cleanup decisions must be based on task state and retention purpose.

A newer file can be disposable if its purpose is finished. An older file must remain if an active task still requires it.

## Never Delete Unpushed Work

Before deleting local project material, verify all of the following:

- required changes are committed;
- the target remote is correct;
- the push succeeded;
- required files are present in the remote repository;
- no required untracked files remain;
- no required local-only work remains.

If any of these checks fail or cannot be verified, stop cleanup and preserve the material until the state is resolved.

## Generated Image MCP Rule

The OpenRouter image-generation MCP output directory is temporary working storage.

Generated images must not accumulate there.

Each generated image must either:

- be consumed by its active mockup/asset/review task and then deleted; or
- be promoted into the project repository as an approved durable asset, pushed successfully, verified remotely, and then removed from temporary MCP storage.

## Visual Comparison Rule

Playwright screenshots and deterministic visual-comparison artifacts are temporary validation material by default.

After the visual-fidelity decision has been recorded:

- preserve only evidence explicitly required by the project;
- push any required evidence to the project repository;
- delete the temporary reference copies, screenshots, diff files, and intermediate artifacts that no longer have an active purpose.

## Completion Rule

Work is not complete merely because implementation or testing succeeded.

For tasks that create local working files, completion also requires:

**durable work pushed and verified + temporary work cleaned.**
