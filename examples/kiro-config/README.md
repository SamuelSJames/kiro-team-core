# Kiro IDE Configuration Examples

Reference templates for Kiro IDE 1.x / CLI 3.x configuration.

These files are examples only. They are intentionally stored outside the active `.kiro/` configuration tree so copying this repository does not automatically grant permissions, start MCP servers, or activate hooks.

## Examples

| Example | Real Kiro location |
|---|---|
| `mcp.workspace.example.json` | `<workspace>/.kiro/settings/mcp.json` |
| `mcp.user.example.json` | `~/.kiro/settings/mcp.json` |
| `permissions.user.example.yaml` | `~/.kiro/settings/permissions.yaml` |
| `permissions.workspace.example.yaml` | `~/.kiro/workspace-roots/<hash>/permissions.yaml` |
| `agent.example.md` | `<workspace>/.kiro/agents/<agent>.md` or `~/.kiro/agents/<agent>.md` |
| `hook.example.json` | `<workspace>/.kiro/hooks/<hook>.json` |
| `skill-example/SKILL.md` | `<workspace>/.kiro/skills/<skill>/SKILL.md` or `~/.kiro/skills/<skill>/SKILL.md` |
| `power-example/plugin.json` | Root of a Kiro Power package |
| `power-example/mcp.json` | Root of a Kiro Power package |
| `kiroignore.example` | `<workspace>/.kiroignore` |

## Important rules

- Never commit credentials or tokens.
- Reference secrets with environment variables.
- Workspace permission files are stored outside the repository so a cloned repository cannot grant itself trust.
- Prefer narrow permission rules over wildcards.
- A `deny` rule overrides `ask`, and `ask` overrides `allow`.
- MCP servers can access the local environment outside normal agent tool restrictions. Only configure trusted servers.
- Keep specialist agents narrowly scoped. Use `includeMcpJson: false` when an agent should not inherit every workspace/global MCP server.
- Load only the steering files and skills the agent needs when minimizing context is important.

## Kiro Team Core direction

For this project, these examples are intended to become the basis for:
1. shared permission conventions;
2. specialist MCP access;
3. agent-specific steering;
4. focused reusable skills;
5. hooks enforcing workflow gates.
