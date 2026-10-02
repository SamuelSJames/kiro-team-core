---
name: backend-implementation
description: Implement approved server-side application behavior, transactions, service logic, internal APIs, jobs, and error handling within established architecture boundaries.
---

# Backend Implementation

## Owner
Agent 16 — Backend Engineer.

## Shared Use
Agents 18 and 17 may consume service boundaries/contracts within their own scopes. Agent 29 may inspect during review.

## Source Inspiration
Adapted from magnus919/agent-skills backend-engineering methodology, preserving Kiro Team Core's stricter ownership split.

## Procedure
1. Read approved architecture, interfaces, feature behavior, and data/integration contracts.
2. Keep business/domain logic separate from transport and persistence details where practical.
3. Validate inputs at trust boundaries.
4. Define transaction boundaries explicitly.
5. Make retry-sensitive operations idempotent where required.
6. Use structured, non-secret error handling with stable categories.
7. Add service-level observability hooks required by architecture.
8. Implement unit and focused integration tests for owned behavior.
9. Exercise failure paths, not only happy paths.
10. Verify build/tests before handoff.

## Boundary Rules
- Agent 14 owns system architecture and service boundaries.
- Agent 17 owns schema/migrations.
- Agent 18 owns third-party API/OAuth/webhook integration.
- Agent 19 owns CI/CD and deployment automation.
- Agent 20 owns Proxmox resources.
- Agent 28 owns independent security review.

## Hard Stop
Do not silently change external contracts, database schema ownership, infrastructure, or approved architecture to make implementation easier.
