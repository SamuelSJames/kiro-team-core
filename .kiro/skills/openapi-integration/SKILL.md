---
name: openapi-integration
description: Inspect an external API contract and implement a bounded integration without owning backend product logic.
---

# OpenAPI Integration

## Owner
Agent 18 — Integration / API Engineer.

## Shared Use
Agent 16 may consume the resulting service contract.

## Steps
1. Identify the external provider and required operations from approved architecture.
2. Use OpenAPI MCP when a specification is available.
3. Validate authentication, required headers, request/response schemas, rate limits, retries, pagination, webhooks, and error behavior.
4. Use Infisical only for approved secret-backed configuration.
5. Never print, log, document, or commit secret values.
6. Implement the external-service boundary and focused tests.
7. Record the contract in INTEGRATIONS.md.
8. Hand back to Agent 01.

## Hard Stop
Do not absorb internal backend business logic or database ownership.
