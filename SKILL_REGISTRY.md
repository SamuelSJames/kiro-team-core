# Kiro Team Core — Skill Registry

Reusable procedures live under `.kiro/skills/<skill-name>/SKILL.md`.

Each skill has exactly one primary owner. Shared use is allowed only when the skill explicitly says so, and shared use never transfers ownership of the underlying responsibility.

| Skill | Primary Owner | Shared Use |
|---|---|---|
| intake-validation | 02 Intake Analyst | Agent 01 for routing awareness |
| mockup-approval-cycle | 03 Mock Image Generator | Agents 01, 08, 09 for handoff/reference |
| design-contract | 08 UI / Visual Design | Agents 05, 06, 07, 09, 15, 27, 30 read/follow |
| spacing-layout-system | 08 UI / Visual Design | Agents 05, 09, 11, 12, 15 consume/apply |
| visual-fidelity-check | 09 Visual Reconstruction | Agents 15, 27, 30 consume evidence |
| web-3d-animation | 12 3D / Interactive Visual Engineer | Agents 08, 11, 15, 27 collaborate/consume |
| bounded-research | 13 Research Agent | Invoked by 04, 14, 18, 30 through Agent 01 |
| reaper-feasibility | 13 Research Agent | Agents 21 and 24 consume findings |
| system-design-package | 14 Technical Architect | Agents 01 and 20 consume outputs |
| frontend-implementation | 15 Frontend Engineer | Agents 27, 29 consume/inspect |
| backend-implementation | 16 Backend Engineer | Agents 17, 18, 29 consume boundaries/contracts |
| database-design | 17 Database Engineer | Agents 16, 29 consume/review |
| openapi-integration | 18 Integration / API Engineer | Agent 16 may consume contracts |
| repository-work-cycle | 19 DevOps / CI-CD Engineer | Builders/reviewers may use the procedure |
| ci-cd-pipeline | 19 DevOps / CI-CD Engineer | Agents 27/28 provide gate requirements |
| proxmox-project-provision | 20 Proxmox Infrastructure | Agent 19 may consume environment records |
| graphify-codebase-map | 26 Documentation / Knowledge Engineer | Agents 14, 15, 16, 17, 18, 27, 29 may use |
| debugging-root-cause | 27 QA Engineer | Builders 15–25 and Agent 29 may use methodology |
| e2e-browser-testing | 27 QA Engineer | Agent 15 may run focused implementation checks |
| security-audit | 28 Security Reviewer | Builders consume remediation requirements |
| code-review | 29 Architecture / Code Reviewer | Builders may self-check; no shared review ownership |
| release-audit | 30 Release / Completion Auditor | No shared ownership |

| team-orchestration | 01 Orchestrator | No shared ownership |
| product-methodology | 04 Product Architect | Agents 01, 05, 13, 14 consume baseline |
| product-design-ux | 05 UX / Product Design | Agents 06, 08, 15, 27 consume outputs |
| ux-content-copy | 06 Content / UX Copy | Agents 05, 07, 08, 15, 27 consume copy |
| brand-system | 07 Brand Strategy | Agents 03, 06, 08, 10, 11, 12 consume rules |
| visual-asset-pipeline | 10 Visual Asset Engineer | Agents 03, 08, 11, 12, 15 consume/request assets |
| interaction-motion-design | 11 Custom UI / Motion Engineer | Agents 05, 08, 15, 27 collaborate/consume |
| music-software-architecture | 21 Music Software Architect | Agents 22–25 consume domain architecture |
| dsp-audio-engineering | 22 DSP / Audio Engineer | Agents 21, 24, 25 consume interfaces/assumptions |
| midi-engineering | 23 MIDI Engineer | Agents 21, 22, 24 consume MIDI contracts |
| reaper-integration | 24 REAPER Integration Engineer | Agents 13, 21–23, 25 supply/consume boundaries |
| linux-audio-platform | 25 Linux Audio Platform Engineer | Agents 21–24 consume platform guarantees |
| documentation-adr | 26 Documentation / Knowledge Engineer | Decision owners provide rationale/facts |
