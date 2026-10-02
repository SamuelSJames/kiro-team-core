---
name: e2e-browser-testing
description: Build and run reliable end-to-end browser tests with Playwright against approved acceptance criteria and user-visible workflows.
---

# E2E Browser Testing

## Owner
Agent 27 — QA Engineer.

## Shared Use
Agent 15 may run focused browser checks during implementation. Agent 27 owns the independent E2E verdict.

## Source Inspiration
Adapted from Playwright/E2E testing patterns in wshobson/agents.

## Procedure
1. Select an approved acceptance criterion or critical user journey.
2. Start from user-visible behavior, not implementation details.
3. Prefer stable semantic locators: role, label, accessible name, test id only when necessary.
4. Arrange deterministic test data and known starting state.
5. Perform the workflow using realistic user actions.
6. Assert outcomes the user or system can observe.
7. Cover at least the critical success path plus material error/permission states.
8. Avoid arbitrary sleeps; wait on explicit UI/network/state conditions.
9. Capture failure evidence only when useful; clean temporary screenshots/traces after review.
10. Treat flaky tests as defects: identify nondeterminism rather than rerunning until green.
11. Report failures with reproduction steps and affected acceptance criteria.

## Visual Boundary
E2E behavior testing does not replace Agent 09's deterministic visual-fidelity check.

## Hard Stop
Do not modify product logic to make a test pass. Route implementation failures to the owning builder through Agent 01.
