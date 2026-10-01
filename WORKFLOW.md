# Kiro Team Core — Project Workflow

## Default Flow

1. Agent 02 completes and validates intake.
2. Agent 29 generates the number of mockups required by the intake.
3. USER APPROVAL GATE: no build begins until the user explicitly approves the required mockup set.
4. Rejected mockups are deleted and regenerated from user feedback.
5. If mockup feedback changes broad scope, Agent 02 updates and revalidates the intake.
6. Agents 03 and 04 define product and technical architecture from the approved intake and mockup.
7. Development architecture defaults to the authorized Proxmox environment on pve3/pve4 unless the intake explicitly requires another target.
8. Only one development system design is required by default: the Proxmox development design.
9. Builders implement the project in the Proxmox development environment.
10. Visual implementations must be reviewed against the approved mockup and achieve at least 92% visual similarity before release approval.
11. Agents 25, 26, and 27 independently review function, security, and architecture/code quality.
12. Agent 28 performs the final completion audit.
13. After project completion, ask the user exactly: **DO YOU WANT TO DEPLOY TO PRODUCTION?**
14. Only after a YES is production architecture designed.
15. AWS is the default production architecture target unless the intake or user specifies another target.
16. Linode/Akamai is an alternative production target when selected.

## Visual Source of Truth

The explicitly approved mockup is the visual source of truth for the project.

The 92% visual threshold applies to the rendered implementation compared with the approved mockup. Functional correctness, accessibility, responsive behavior, and security are separate gates and cannot be traded away to increase visual similarity.

## Resource Rule

Do not design production infrastructure during initial development unless the intake explicitly requires it. This avoids unnecessary work and resource use.
