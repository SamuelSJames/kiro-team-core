---
name: debugging-root-cause
description: Systematically reproduce, localize, reduce, fix, and guard against software failures instead of guessing.
---

# Root-Cause Debugging

## Owner
Agent 27 — QA Engineer (methodology owner).

## Shared Use
Builders (Agents 15–25) and Agent 29 may use this procedure within their own scope. Ownership of the broken component remains with its builder.

## Source Inspiration
Adapted from addyosmani/agent-skills debugging-and-error-recovery.

## Procedure
1. **Reproduce** — capture the smallest reliable reproduction, inputs, environment, and observed vs expected behavior.
2. **Localize** — identify the failing layer using logs, tests, traces, browser inspection, or targeted instrumentation.
3. **Reduce** — shrink the failure to the smallest code/data/config path that still fails.
4. **Form one hypothesis** — identify a specific causal explanation and the evidence that would disprove it.
5. **Test the hypothesis** — change or inspect one relevant variable at a time.
6. **Fix the root cause** — do not merely suppress the symptom.
7. **Guard** — add the smallest regression test or validation that proves the failure cannot silently return.
8. Run affected tests plus a sensible regression set.
9. Remove temporary diagnostic logging/files when no longer needed.
10. Record material root-cause findings when they affect architecture or operations.

## Stop-the-Line Rule
If the failure cannot be reproduced, the evidence contradicts the current hypothesis, or the fix requires another agent's owned change, stop guessing and route the finding through Agent 01.

## Hard Stop
Reviewers using this skill may diagnose and report but must not become the primary implementer of fixes they are independently reviewing.
