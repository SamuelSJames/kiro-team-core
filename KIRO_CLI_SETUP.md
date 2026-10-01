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

These areas must be completed or validated from the machine where Kiro CLI runs:

- MCP server definitions and credentials;
- Proxmox connectivity and authentication;
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
