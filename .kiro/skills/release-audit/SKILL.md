---
name: release-audit
description: Perform the final independent completion audit without becoming a builder or waiving failed gates.
---

# Release Audit

## Owner
Agent 30 — Release / Completion Auditor.

## Shared Use
No shared ownership.

## Steps
1. Verify the approved numbered feature list is complete.
2. Verify architecture/code review has no unresolved release-blocking findings.
3. Verify QA passes.
4. Verify security review passes.
5. For mockup-driven projects, verify Agent 09 produced same-dimension visual-compare evidence with fidelity >=92.00.
6. Verify required documentation and operational records exist.
7. Verify repository/workspace hygiene: durable work is in the designated project repository and temporary artifacts are cleaned.
8. Record RELEASE_AUDIT.md and the final development completion decision.
9. Only if all required gates pass, mark development complete.
10. The next user-facing question must be exactly: **DO YOU WANT TO DEPLOY TO PRODUCTION?**

## Hard Stop
Do not implement fixes, waive failed critical gates, or start production architecture before an explicit YES.
