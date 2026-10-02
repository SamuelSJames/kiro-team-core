---
name: ci-cd-pipeline
description: Build repeatable CI/CD pipelines that enforce project quality gates, protect secrets, produce reproducible artifacts, and support safe rollback.
---

# CI/CD Pipeline

## Owner
Agent 19 — DevOps / CI-CD Engineer.

## Shared Use
Agent 27 supplies test gates, Agent 28 supplies security requirements, and builders supply build/test commands. Agent 19 owns pipeline implementation.

## Source Inspiration
Adapted from addyosmani/agent-skills ci-cd-and-automation, narrowed for Kiro Team Core's development/production gates.

## Procedure
1. Discover the project's real lint, type, unit, integration, E2E, security, and build commands.
2. Define the minimum required quality-gate sequence.
3. Fail closed: failed required checks block promotion.
4. Cache dependencies/artifacts safely without making builds depend on stale state.
5. Keep credentials in the approved secrets system; never hardcode them into CI configuration.
6. Separate development/test credentials from production credentials.
7. Produce reproducible/versioned artifacts where applicable.
8. Keep deployment distinct from release/enablement when feature flags or staged rollout are used.
9. Define rollback before production automation.
10. Keep failure output useful enough for the owning agent to reproduce locally.
11. Optimize slow pipelines by parallelizing independent checks and scoping work to relevant changes without skipping required gates.
12. Record pipeline behavior and required manual gates.

## Kiro Team Core Gate
Initial project development does not imply production deployment. Production automation follows the explicit post-completion production decision and approved production architecture.

## Hard Stop
Do not bypass required tests/reviews merely to make the pipeline green.
