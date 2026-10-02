---
name: database-design
description: Design durable schemas, constraints, indexes, migrations, and query patterns from approved data requirements and workloads.
---

# Database Design

## Owner
Agent 17 — Database Engineer.

## Shared Use
Agent 16 consumes persistence contracts. Agent 29 may review architecture conformity.

## Source Inspiration
Adapted from database-design and SQL optimization patterns in wshobson/agents.

## Procedure
1. Start from approved entities, invariants, access patterns, scale expectations, and consistency needs.
2. Choose data types that represent domain values precisely.
3. Use keys, uniqueness, foreign keys, checks, and nullability to enforce invariants at the data layer.
4. Normalize by default; denormalize only for a measured access/performance reason.
5. Design indexes from real query/filter/order/join patterns rather than indexing everything.
6. Define ownership of timestamps, soft-delete behavior, retention, and audit fields explicitly.
7. Make migrations forward-safe and reversible where practical.
8. Plan backfills separately from schema mutation when data volume warrants it.
9. Review transaction/isolation requirements for concurrent writes.
10. Inspect query plans for performance-sensitive operations when the engine supports it.
11. Create tests for constraints and migration behavior.
12. Record schema and migration decisions.

## Hard Stop
Do not select a new database technology, redefine domain behavior, or absorb backend business logic without routing through Agent 01 and the proper owner.
