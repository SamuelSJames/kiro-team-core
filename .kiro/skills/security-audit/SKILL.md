---
name: security-audit
description: Independently review trust boundaries, authentication, authorization, secrets, untrusted inputs, dependencies, and abuse paths using evidence-based security findings.
---

# Security Audit

## Owner
Agent 28 — Security Reviewer.

## Shared Use
Builders may consume remediation requirements. Agent 28 remains independent.

## Source Inspiration
Adapted from magnus919/agent-skills secure-software-engineering and its emphasis on threat boundaries, secure defaults, and verifiable evidence.

## Procedure
1. Identify assets, actors, trust boundaries, entry points, privileged actions, and sensitive data.
2. Review authentication and session assumptions.
3. Review authorization at the action/resource boundary; do not rely on UI hiding.
4. Trace untrusted input through parsing, validation, storage, rendering, command execution, and outbound requests.
5. Verify secret handling: no secrets in code, logs, prompts, docs, test fixtures, or repository history.
6. Review dependency/supply-chain exposure relevant to the change.
7. Review file upload, SSRF, injection, XSS, CSRF, path traversal, insecure deserialization, and command execution risks where applicable.
8. Review multi-tenant isolation when applicable.
9. Verify secure defaults and least privilege.
10. Classify findings by impact, exploitability, affected surface, evidence, and remediation requirement.
11. Require a verifiable retest for release-blocking findings.

## Evidence Rule
A scanner warning alone is not a final vulnerability verdict; validate the affected path and context. Conversely, absence of scanner findings is not proof of security.

## Hard Stop
Do not retrieve or expose secret values merely to prove access. Do not become the primary builder of the remediation you independently review.
