# OpenRouter Image MCP

Narrow stdio MCP server for the Kiro agent team. Wraps the OpenRouter **Image API**
(`POST /api/v1/images`, `GET /api/v1/images/models`) and exposes four tools:

| Tool | Purpose |
|------|---------|
| `list_image_models` | Compact catalog: slug, supported params, aspect ratios/resolutions, reference-image capability, pricing (when available). |
| `get_image_model_capabilities` | Capabilities for one model slug (call before generating/editing). |
| `generate_image` | Text→image. Decodes base64, saves to disk, returns paths + `usage.cost`. |
| `edit_image` | Image→image. Verifies the model supports `input_references`, encodes a local reference file as a data URL, saves output, returns paths + cost. |

## Secret handling

The OpenRouter key is **never** stored in source, `mcp.json`, launcher args, logs, or git.
At startup the server resolves it from **Infisical** via universal-auth and keeps it in
memory only:

- project `agent-fleet` · env `prod` · path `/llm` · secret `OPENROUTER_API`
- machine identity: the read-only `openclaw` client (same one the ws `gen-image.sh` uses)

The launcher injects only the Infisical **client** credentials as env vars
(`INFISICAL_API_URL`, `INFISICAL_CLIENT_ID`, `INFISICAL_CLIENT_SECRET`,
`INFISICAL_PROJECT_ID`). Override secret coordinates with `INFISICAL_ENV`,
`INFISICAL_SECRET_PATH`, `INFISICAL_SECRET_NAME` if ever needed.
`OPENROUTER_API_KEY` in the environment short-circuits Infisical (not used in prod).

Authorization headers are redacted from all error output; raw base64 is never returned.

## Storage

Images are written to the host path bind-mounted at `/data` in the container:
`/opt/mcp/data/openrouter-images/` on LXC 301. Filenames are
`<UTC-timestamp>_<model>_<idx>_<uuid>.<ext>`, sanitized and never overwritten.
`output_directory` (optional) must stay under that root.

## Run

```
/opt/mcp/run-openrouter-image.sh      # stdio; built for `ssh -T pve3 pct exec 301 -- ...`
```

## Health / test (no paid generation)

```
# initialize + tools/list + list_image_models, no image is generated
printf '%s\n' \
 '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"0"}}}' \
 '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
 '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
 '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"list_image_models","arguments":{}}}' \
 | /opt/mcp/run-openrouter-image.sh
```

`generate_image` / `edit_image` cost money — only call when authorized.

## Deps (pinned)

`mcp==1.2.1`, `httpx==0.27.2`, `anyio==4.6.2.post1`, base image `python:3.12-slim`.
