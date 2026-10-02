# Kiro Team Core — Skill Registry

Reusable procedures live under `.kiro/skills/<skill-name>/SKILL.md`.

Each skill has exactly one primary owner. Shared use is allowed only when the skill explicitly says so, and shared use never transfers ownership of the underlying responsibility.

| Skill | Primary Owner | Shared Use |
|---|---|---|
| intake-validation | 02 Intake Analyst | Agent 01 for routing awareness |
| mockup-approval-cycle | 03 Mock Image Generator | Agents 01, 08, 09 for handoff/reference |
| design-contract | 08 UI / Visual Design | Agents 05, 06, 07, 09, 15, 27, 30 read/follow |
| bounded-research | 13 Research Agent | Invoked by 04, 14, 18, 30 through Agent 01 |
| reaper-feasibility | 13 Research Agent | Agents 21 and 24 consume findings |
| system-design-package | 14 Technical Architect | Agents 01 and 20 consume outputs |
| visual-fidelity-check | 09 Visual Reconstruction | Agents 15, 27, 30 consume evidence |
| openapi-integration | 18 Integration / API Engineer | Agent 16 may consume contracts |
| proxmox-project-provision | 20 Proxmox Infrastructure | Agent 19 may consume environment records |
| repository-work-cycle | 19 DevOps / CI-CD Engineer | Builders/reviewers may use the procedure |
| graphify-codebase-map | 26 Documentation / Knowledge Engineer | Agents 14, 15, 16, 17, 18, 27, 29 may use |
| release-audit | 30 Release / Completion Auditor | No shared ownership |

| frontend-implementation | 15 Frontend Engineer | Agents 27, 29 consume/inspect |
| backend-implementation | 16 Backend Engineer | Agents 17, 18, 29 consume boundaries/contracts |
| database-design | 17 Database Engineer | Agents 16, 29 consume/review |
| debugging-root-cause | 27 QA Engineer | Builders 15–25 and Agent 29 may use methodology |
| e2e-browser-testing | 27 QA Engineer | Agent 15 may run focused implementation checks |
| security-audit | 28 Security Reviewer | Builders consume remediation requirements |
| code-review | 29 Architecture / Code Reviewer | Builders may self-check; no shared review ownership |
| ci-cd-pipeline | 19 DevOps / CI-CD Engineer | Agents 27/28 provide gate requirements |
| web-3d-animation | 12 3D / Interactive Visual Engineer | Agents 08, 11, 15, 27 collaborate/consume |
| spacing-layout-system | 08 UI / Visual Design | Agents 05, 09, 11, 12, 15 consume/apply |
