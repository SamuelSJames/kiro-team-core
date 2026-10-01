# Scope Enforcement

This rule applies to every Kiro Team Core agent.

## Mandatory Hard Stop

Before performing any task, compare the requested work against SCOPE_GOVERNANCE.md.

If any part of the work belongs to another agent:

- STOP that part immediately.
- Do not perform it "just to help."
- Do not silently expand your role.
- Do not use your tools to bypass the correct owner.
- Return the out-of-scope item to Agent 01 — Orchestrator for routing.
- Continue only the portions clearly inside your assigned scope.

If ownership is ambiguous, stop and ask Agent 01 to assign a primary owner.

## Skill Ownership

Every reusable skill must declare one primary owning agent.

A skill may be used by supporting agents only when:
- the skill explicitly permits shared use; and
- using it does not transfer ownership of the underlying responsibility.

Do not create duplicate skills that perform the same responsibility under different names.

When a new skill overlaps an existing skill, extend the existing skill or create a narrowly scoped sub-skill instead.

## Review Separation

Agents 27–30 are independent reviewers.

They may identify failures and required remediation, but must not become the primary builder of the work they are reviewing.
