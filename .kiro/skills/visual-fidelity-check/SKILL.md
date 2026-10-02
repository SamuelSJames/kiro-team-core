---
name: visual-fidelity-check
description: Measure rendered UI against the approved mockup using Playwright and the deterministic visual-compare tool.
---

# Visual Fidelity Check

## Owner
Agent 09 — Visual Reconstruction Agent.

## Shared Use
Agents 15, 27, and 30 consume the evidence. They do not own the measurement gate.

## Steps
1. Identify the approved reference mockup and its exact dimensions.
2. Set Playwright to the same canonical viewport.
3. Capture the implementation screenshot from Playwright inline image content.
4. Save the screenshot to a task-scoped temporary host path.
5. Run:
   `visual-compare --reference <ref> --actual <actual> --threshold 92 --output-dir <task-temp-dir>`
6. Require identical dimensions; do not resize to force a match.
7. Record SSIM, pixel similarity, edge similarity, fidelity score, and PASS/FAIL.
8. If below 92.00, provide correction targets to the builder through Agent 01.
9. After evidence is consumed, delete temporary screenshot/diff artifacts unless explicitly retained in the project repository.

## Hard Stop
Do not replace the deterministic score with subjective model judgment.
