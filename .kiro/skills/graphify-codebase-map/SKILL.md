---
name: graphify-codebase-map
description: Build and query a temporary Graphify knowledge graph to understand code, docs, configs, schemas, and dependency relationships before broad source inspection.
---

# Graphify Codebase Map

## Owner
Agent 26 — Documentation / Knowledge Engineer.

## Shared Use
Agents 14, 15, 16, 17, 18, 27, and 29 may use the Graphify CLI for navigation and analysis. Shared use does not transfer ownership of project knowledge.

## Tool
Graphify CLI from the official `graphifyy` package.

Kiro Team Core installs the CLI with:

```bash
uv tool install graphifyy
```

The CLI command remains `graphify`.

Do not run Graphify's own Kiro installer inside managed Kiro Team Core unless the framework is intentionally being migrated; this repository provides its own controlled skill and steering.

## Purpose
Reduce repeated broad file reads by giving agents a deterministic relationship map of a project before deeper inspection.

## Steps
1. Identify the active temporary project working copy.
2. Build or refresh the graph for only the required project scope.
3. Query the graph first for architecture, dependency, symbol, schema, config, and documentation relationships.
4. Read raw source only when the graph identifies the relevant files or when exact implementation detail is required.
5. Treat graph results as navigation/relationship evidence, not as a replacement for source-of-truth code.
6. Refresh the graph after material source changes when later analysis depends on current relationships.
7. Keep Graphify outputs task-scoped and temporary by default.
8. Delete graph outputs during project cleanup unless the user explicitly requires them as durable project artifacts.

## Context Rule
Use Graphify to reduce unnecessary context, not to generate another permanent duplicate knowledge store.

## Hard Stop
Do not use graph inference to override source code, approved architecture, or explicit project documentation. If Graphify and source disagree, inspect the source and report the discrepancy.
