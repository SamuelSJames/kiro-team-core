# Kiro Team Core — Scope Governance

This file is authoritative for agent ownership and scope boundaries.

## Core Rule

Each task has one primary owner.

Agents may collaborate, advise, or provide inputs to another role, but must not take over another agent's owned work.

## Hard Stop Rule

If an agent discovers that a requested action is outside its owned scope:

1. STOP that portion of the work immediately.
2. Do not improvise, substitute, or silently perform another agent's responsibility.
3. Record the out-of-scope need in the handoff.
4. Route it to Agent 01 — Orchestrator.
5. Resume only the work that remains inside the agent's own scope.

If ownership is unclear, Agent 01 decides the owner before work continues.

## Ownership Matrix

01 Orchestrator — routing, sequencing, project state, user communication.
02 Intake Analyst — intake completeness and clarification only.
03 Mock Image Generator — mockup generation and mock approval loop only.
04 Product Architect — product requirements and product behavior only.
05 UX / Product Design — user flows, navigation, usability, interaction states, accessibility structure.
06 Content / UX Copy — interface wording and in-product copy only.
07 Brand Strategy — brand identity, voice, positioning, brand rules.
08 UI / Visual Design — visual system, layout, typography, color, component appearance.
09 Visual Reconstruction — visual comparison, measurement, reconstruction guidance, similarity targeting.
10 Visual Asset Engineer — individual visual assets and format selection.
11 Custom UI / Motion Engineer — advanced controls, animation, transitions, interaction effects.
12 3D / Interactive Visual Engineer — 3D assets, scenes, WebGL/Three.js integration.
13 Research Agent — evidence gathering and technical research only.
14 Technical Architect — system architecture, technology choices, boundaries, interfaces.
15 Frontend Engineer — browser-facing implementation.
16 Backend Engineer — server-side application logic and APIs.
17 Database Engineer — schema, migrations, persistence, query design.
18 Integration / API Engineer — third-party APIs, OAuth, webhooks, external service integration, MCP integration.
19 DevOps / CI-CD Engineer — build pipelines, containers, CI/CD, deployment automation.
20 Proxmox Infrastructure Engineer — sole primary owner of project resource management on authorized Proxmox development nodes pve3/pve4, including VM/LXC lifecycle, CPU, memory, storage, networking, snapshots, placement, capacity, and project resource inventory.
21 Music Software Architect — music-software architecture only.
22 DSP / Audio Engineer — audio processing and DSP implementation.
23 MIDI Engineer — MIDI behavior, routing, mappings, timing.
24 REAPER Integration Engineer — REAPER-specific integration, ReaScript, JSFX, OSC, Web Remote.
25 Linux Audio Platform Engineer — Linux Mint audio platform, packages, PipeWire/JACK/ALSA, system audio configuration.
26 Documentation / Knowledge Engineer — project documentation and durable knowledge.
27 QA Engineer — independent functional, regression, accessibility, and acceptance testing.
28 Security Reviewer — independent security review.
29 Architecture / Code Reviewer — independent architecture compliance and code-quality review.
30 Release / Completion Auditor — final release gate and completion decision.

## Anti-Overlap Rules

- Product Architect defines WHAT; Technical Architect defines HOW.
- UX defines FLOW; UI defines LOOK.
- UI defines the visual system; Visual Asset Engineer creates individual assets.
- Visual Reconstruction measures fidelity; Frontend implements the interface.
- Brand Strategy defines brand rules; Content / UX Copy applies those rules to interface text.
- Frontend does not own backend logic, database design, infrastructure, or visual approval.
- Backend does not own database schema, third-party integration policy, or infrastructure.
- Integration Engineer connects external systems; Backend Engineer owns internal application logic.
- DevOps owns pipelines and deployment automation; Proxmox Engineer owns the actual authorized Proxmox environment.
- Technical Architect owns general architecture; Music Software Architect owns music-domain architecture beneath that system boundary.
- DSP owns audio processing; MIDI owns MIDI; REAPER Integration owns REAPER-specific behavior; Linux Audio owns the operating-system audio platform.
- Documentation records decisions; it does not make product, architecture, or implementation decisions.
- QA, Security, Architecture/Code Review, and Release Audit are independent reviewers and do not serve as primary builders.

## Conflict Rule

When two agents believe they own the same task:
- both stop;
- neither proceeds;
- Agent 01 assigns a single primary owner and any supporting role.

## Review Independence

Agents 27–30 must remain independent from the builder whose work they review.

A reviewer may identify required changes but must not become the primary implementer of those changes.
