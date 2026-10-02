# Kiro Team Core

Reusable 30-agent Kiro CLI software team with strict role ownership, gated workflow, narrow tool attachment, deterministic visual fidelity checks, and repository-first workspace hygiene.

## Core Documents

- `AGENT_ROSTER.md` — permanent 01–30 roster.
- `SCOPE_GOVERNANCE.md` — ownership, hard-stop, anti-overlap, and review-independence rules.
- `WORKFLOW.md` — project flow and approval/release gates.
- `TOOLING.md` — validated tool surface, MCP connection methods, ownership, and deterministic utilities.
- `WORKSPACE_HYGIENE.md` — repository-first storage and cleanup policy.
- `KIRO_CLI_SETUP.md` — local/global Kiro CLI setup guidance.

## Runtime Layout

- `.kiro/agents/` — custom agent definitions.
- `.kiro/steering/agents/` — focused role steering.
- `.kiro/skills/` — reusable owner-scoped procedures.
- `tools/visual-compare/` — canonical deterministic visual-fidelity utility source.
- `tools/openrouter-image/` — canonical OpenRouter image MCP source.

## Repository Purpose

`kiro-team-core` is only the canonical source/template for the global Kiro runtime. It is not an application-project repository. Actual project source must never be committed into this repository.

The future installer will clone this repository temporarily, install the global runtime into `~/.kiro`, validate it, and then the installed runtime may operate without Git metadata.

## Global Principles

- One primary owner per responsibility.
- Out-of-scope work hard-stops and routes through Agent 01.
- Builders do not approve their own work.
- GitHub/Gitea is the durable source of truth; local working copies are temporary.
- Generated artifacts have a defined purpose and are deleted when that purpose is complete unless deliberately promoted into the repository.
- Visual fidelity uses the deterministic `visual-compare` composite score with a default pass threshold of 92.00.
- Agent 30 alone may mark development complete.
- After completion, the next user-facing question is exactly: **DO YOU WANT TO DEPLOY TO PRODUCTION?**
