# Kiro Team Core — Tooling & Connection Governance

This file records the reusable tool surface for the Kiro 30-agent team and the connection patterns currently validated in the local Kiro CLI environment.

## Core Principle

Tools provide capability; agent scope determines whether that capability should be used.

Global runtime permissions may remain broad to avoid repetitive prompts. Tool ownership, workflow gates, and agent steering provide the organizational controls.

Do not expose, print, log, document, or commit secret values.

## Agent MCP Attachment Rule

Global `~/.kiro/settings/mcp.json` may contain the reusable server inventory, but specialist agents should not automatically inherit every global MCP.

For core specialist agents, prefer explicit agent-level `mcpServers` entries and keep `includeMcpJson: false` so each role receives only the MCP servers required by its scope. This reduces tool/context load and prevents accidental cross-scope capability use.

Current explicit attachments:
- Agent 03 -> OpenRouter Image
- Agent 09 -> Playwright
- Agent 10 -> OpenRouter Image
- Agent 15 -> Playwright
- Agent 18 -> OpenAPI + Infisical
- Agent 20 -> Proxmox
- Agent 27 -> Playwright

Additional MCP access must be added only when the role has a defined need.

## Built-in Kiro Tools

- `read` — file/content inspection.
- `write` — file modification where permitted.
- `shell` — deterministic local command execution.
- `web` — web research and retrieval.

## Connected MCP Servers

### Gitea

Connection:

```text
Kiro CLI -> ssh -T pve3 -> pct exec 301 -> /opt/mcp/run-gitea.sh -> stdio MCP
```

Purpose: repositories, commits, branches, issues, pull requests, releases, Actions, packages, wiki, and related repository operations.

Use only when repository work falls inside the assigned agent's scope.

### Proxmox

Connection:

```text
Kiro CLI -> ssh -T pve3 -> pct exec 301 -> /opt/mcp/run-proxmox.sh -> stdio MCP
```

Primary owner: Agent 20.

The server exposes broad infrastructure capability. Agent 20 may perform routine project operations on authorized pve3/pve4 resources when they are supported by the approved system design. Destructive, cluster-wide, identity, storage-destruction, or otherwise irreversible operations require the applicable workflow safeguard and must not be performed merely because the tool permits them.

### Infisical

Connection:

```text
Kiro CLI -> ssh -T ws -> ~/.local/bin/run-infisical-mcp.sh -> stdio MCP
```

Purpose: secret/project/environment access for integrations, DevOps, infrastructure, and security review where required.

Secret values must remain out of prompts, logs, documentation, Git, generated reports, and user-facing output.

### Playwright

Connection:

```text
Kiro CLI -> ssh -T pve3 -> pct exec 301 -> /opt/mcp/run-playwright.sh -> stdio MCP
```

Validated role support: Agents 09, 15, 27, and 29 when their assigned task requires browser inspection or validation.

Primary visual-fidelity workflow:
1. set the canonical viewport;
2. render the implementation;
3. capture a screenshot;
4. use the returned inline image content as temporary task material;
5. compare it with `visual-compare`;
6. delete temporary screenshot/diff artifacts after their purpose is complete unless explicitly promoted into the repository as durable evidence.

Do not add persistent Playwright screenshot storage merely for convenience.

### OpenAPI

Connection:

```text
Kiro CLI -> ssh -T pve3 -> pct exec 301 -> /opt/mcp/run-openapi.sh -> stdio MCP
```

Primary owner: Agent 18.

Purpose: inspect and validate OpenAPI documents, enumerate operations, generate supported request examples, and support external API integration work.

### OpenRouter Image

Connection:

```text
Kiro CLI -> ssh -T pve3 -> pct exec 301 -> /opt/mcp/run-openrouter-image.sh -> stdio MCP
```

Primary owner: Agent 03.
Supporting owner when assigned: Agent 10.

Validated tools:
- `list_image_models`
- `get_image_model_capabilities`
- `generate_image`
- `edit_image`

The OpenRouter key is retrieved from Infisical at runtime and must never be copied into source, MCP configuration, launcher arguments, Git, logs, or agent output.

Generated images are temporary by default and follow `WORKSPACE_HYGIENE.md`.

## Deterministic Local Tool — visual-compare

Canonical command:

```bash
visual-compare \
  --reference approved-mockup.png \
  --actual implementation.png \
  --threshold 92 \
  --output-dir ./visual-comparison
```

Canonical source location in this repository:

```text
tools/visual-compare/
```

Deployed runtime location:

```text
~/.kiro/tools/visual-compare/
~/.local/bin/visual-compare
```

Primary owner: Agent 09.

The fidelity score is deterministic and fixed:

```text
fidelity_score =
    SSIM              * 0.50
  + pixel_similarity  * 0.30
  + edge_similarity   * 0.20
```

Default pass threshold: **92.00**.

Rules:
- reference and actual images must have identical dimensions;
- the tool must not silently resize either image;
- dimension mismatch fails the fidelity gate;
- score calculation is deterministic and not replaced by model judgment;
- functional correctness, accessibility, responsive behavior, security, and other release gates remain independent;
- screenshots, diff images, amplified diffs, and temporary inputs are deleted when their purpose is complete unless deliberately retained as repository evidence.

## Tool Addition Rule

Before adding a new global tool:

1. identify a real agent/task capability gap;
2. check whether an existing built-in, MCP, or deterministic CLI already covers it;
3. prefer the narrowest reliable connection;
4. validate health and tool discovery before depending on it;
5. document ownership and retention behavior;
6. keep secrets out of repository configuration;
7. avoid adding redundant tools that increase context or operational ambiguity.

