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
- Agent 19 -> Infisical
- Agent 20 -> Proxmox
- Agent 27 -> Playwright

Additional MCP access must be added only when the role has a defined need.

## Where Tool Limits Live

Actual tool exposure belongs in each custom agent definition under `.kiro/agents/*.md`:

- `tools` defines the tools the agent can see/use;
- `allowedTools` defines which attached tools may run without an extra approval prompt;
- agent-level `mcpServers` attaches only the MCP servers required by that role;
- `includeMcpJson: false` prevents a specialist from inheriting the entire global MCP inventory.

Steering does **not** provide the technical restriction. Steering documents when and why the attached tools should be used, reinforces ownership, and requires a hard stop when a missing capability belongs to another role.

## Core Tool Assignment Matrix

| Agent | Shell | Web | MCP |
|---|---|---|---|
| 01 Orchestrator | No | No | None |
| 02 Intake Analyst | No | No | None |
| 03 Mock Image Generator | Yes | No | OpenRouter Image |
| 04 Product Architect | No | No | None |
| 05 UX / Product Design | No | No | None |
| 06 Content / UX Copy | No | No | None |
| 07 Brand Strategy | No | No | None |
| 08 UI / Visual Design | No | No | None |
| 09 Visual Reconstruction | Yes | No | Playwright |
| 10 Visual Asset Engineer | Yes | No | OpenRouter Image |
| 11 Custom UI / Motion | Yes | No | None |
| 12 3D / Interactive Visual | Yes | No | None |
| 13 Research | No | Yes | None |
| 14 Technical Architect | No | No | None |
| 15 Frontend Engineer | Yes | No | Playwright |
| 16 Backend Engineer | Yes | No | None |
| 17 Database Engineer | Yes | No | None |
| 18 Integration / API Engineer | Yes | No | OpenAPI, Infisical |
| 19 DevOps / CI-CD Engineer | Yes | No | Infisical |
| 20 Proxmox Infrastructure Engineer | Yes | No | Proxmox |
| 21 Music Software Architect | No | No | None |
| 22 DSP / Audio Engineer | Yes | No | None |
| 23 MIDI Engineer | Yes | No | None |
| 24 REAPER Integration Engineer | Yes | No | None until REAPER tooling is added |
| 25 Linux Audio Platform Engineer | Yes | No | None |
| 26 Documentation / Knowledge Engineer | Yes | No | None |
| 27 QA Engineer | Yes | No | Playwright |
| 28 Security Reviewer | Yes | No | None |
| 29 Architecture / Code Reviewer | Yes | No | None |
| 30 Release / Completion Auditor | No | No | None |

All agents retain only their ordinary document/context tools needed for their role. No specialist inherits Gitea, Proxmox, Infisical, Playwright, OpenAPI, or image-generation tooling simply because the server exists globally.

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

Validated role support: Agents 09, 15, and 27 when their assigned task requires browser inspection or validation.

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

## Deterministic Local Tool — Graphify

Graphify is a local deterministic codebase knowledge-graph CLI used to reduce broad source reads and expose relationships across code, docs, configs, schemas, and manifests.

Official package/CLI:

```bash
uv tool install graphifyy
# command installed:
graphify
```

Primary owner: Agent 26.

Shared use when relevant: Agents 14, 15, 16, 17, 18, 27, and 29.

Kiro Team Core manages its own Graphify skill and steering. Do not run `graphify kiro install` inside the managed global runtime unless intentionally migrating away from the framework-owned integration, because the upstream command writes its own `.kiro/skills/` and `.kiro/steering/` entries.

Rules:
- build/query graphs only for the active project/task scope;
- query the graph before broad source inspection when relationship mapping will help;
- verify exact implementation facts against source files;
- keep `graphify-out/` temporary by default;
- remove graph outputs during workspace cleanup unless explicitly promoted as durable project material.

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

