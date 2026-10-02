# Kiro CLI — Team Core Setup

This repository is designed for Kiro CLI as the primary runtime.

## Context Isolation

For this multi-agent team, disable default resource inheritance so custom agents receive only the resources explicitly attached to their agent configuration.

Run locally from Kiro CLI:

```bash
kiro-cli settings --workspace chat.disableInheritingDefaultResources true
```

This is intentionally a local/workspace CLI setting and is not being forced from this repository.

## Agent Steering

Each agent has one focused steering file:

```text
.kiro/steering/agents/<number>-<agent>.md
```

Each custom agent explicitly references its own steering file.

Do not restore a broad `file://.kiro/steering/**/*.md` resource glob to specialist agents unless there is a deliberate reason to increase their context.

## Local Runtime Configuration

The currently validated reusable MCP connections are:

- Gitea — direct SSH/stdin-stdout launcher through pve3 LXC 301;
- Proxmox — direct SSH/stdin-stdout launcher through pve3 LXC 301;
- Infisical — direct SSH/stdin-stdout launcher through `ws`;
- Playwright — direct SSH/stdin-stdout launcher through pve3 LXC 301;
- OpenAPI — direct SSH/stdin-stdout launcher through pve3 LXC 301;
- OpenRouter Image — direct SSH/stdin-stdout launcher through pve3 LXC 301.

See `TOOLING.md` for ownership, connection patterns, and usage rules.

The deterministic `visual-compare` utility is deployed globally through `~/.local/bin/visual-compare` from an isolated environment under `~/.kiro/tools/visual-compare/`. Its canonical source belongs in this repository under `tools/visual-compare/`.

These areas still require validation from the machine where Kiro CLI runs when applicable:

- REAPER bridge/integration tooling;
- hook commands that depend on installed local tools;
- user/workspace permissions;
- environment variables and secret stores;
- local executable paths.

The repository may contain reference examples, but examples must not be treated as active credentials or trusted local configuration.

## Context Principle

Each agent should load only:

1. its own steering;
2. the task-specific project documents it actually needs;
3. the skills required for that task;
4. the MCP tools explicitly required for its scope.

Agent 01 coordinates the team. Specialist agents do not load other specialists' steering by default.

## CLI Commands

Start in the project:

```bash
cd <project>
kiro-cli
```

Useful controls:

```text
/agent      switch custom agents
/context    inspect current context/token usage
/tools      inspect or manage tool trust
/guide      ask Kiro about CLI configuration
```

Use Kiro CLI's local Guide/introspection when validating version-specific hooks, permissions, MCP servers, or settings before enabling them.


## Graphify CLI

Graphify is an external deterministic CLI dependency used by the framework-owned `graphify-codebase-map` skill.

Install globally in WSL with:

```bash
uv tool install graphifyy
```

Do not automatically run `graphify kiro install` during Kiro Team Core installation. The upstream command creates its own Kiro skill/steering files; this repository already carries the controlled integration we want.


## Bootstrap Installer

Install or refresh the global Kiro Team Core runtime with:

```bash
bash scripts/install-kiro-team-core.sh
```

The installer clones this GitHub framework only into a temporary directory, validates it, copies the managed runtime into `~/.kiro`, installs/verifies `visual-compare` and Graphify, and never leaves `~/.kiro` as a Git working tree.

For validation without changing `~/.kiro`:

```bash
bash scripts/install-kiro-team-core.sh --dry-run
```

Project repositories are separate: all durable project work uses the user's private Gitea. Agent 19 owns new-project repository bootstrap/import; Agent 26 owns existing-project takeover assessment.
