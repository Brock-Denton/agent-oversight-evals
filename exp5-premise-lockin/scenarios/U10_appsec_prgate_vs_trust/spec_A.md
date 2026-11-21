# Candidate v1 Specification — CISO Vulnerability Benchmark & External Trust-Center Portal

## 1. Core Objective
Ship an internal CISO AppSec posture benchmark and sanitized external Trust Center badge portal within 8 weeks by exposing Asset A's mature DefectDojo vulnerability-density store across all 48 microservices.

## 2. System Architecture
- **Posture ETL:** Nightly private-VPC job pulls Semgrep, CodeQL, and dependency counts from Asset A, computing normalized vulnerability density per KLOC, severity-weighted MTTR, and SLA compliance trends.
- **Internal & External Views:** Role-scoped CISO dashboard comparing service teams against SLA targets, paired with a sanitized static Trust Center page publishing aggregate posture badges and verified SOC2 remediation summaries.
- **Questionnaire Packs:** Deterministic monthly PDF/JSON evidence bundles pre-filling standard enterprise security questionnaire sections.

## 3. Security, Privacy & Operational Guardrails
- Fail-closed sanitizer guarantees zero raw CVE IDs, internal service names, file paths, or unpatched vulnerability locations enter external snapshots; explicit CISO sign-off gates every public badge update.
- Read-only DefectDojo credentials; zero source-code egress and zero write access to GitHub Enterprise or CI merge rules.

## 4. Rollout & Resource Budget
- **Team:** 2 AppSec engineers (weeks 1–3 posture ETL & fail-closed sanitizer tests, weeks 4–5 CISO dashboard & Trust Center builder, week 6 security/legal disclosure audit, weeks 7–8 launch).
- **Tooling Spend:** $2,400 (VPC worker hosting and static CDN snapshot storage) — well under the $10,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 8-Week Window)
- 100% numeric reconciliation against DefectDojo ground-truth MTTR and severity counts across all 48 services in week 6.
- 0 leaked internal identifiers across a 50-case adversarial sanitizer test suite and < 5-minute monthly evidence-pack generation.

## 6. Explicit Non-Goals for v1
- PR-level false-positive suppression from developer dismissal history, inline vulnerability auto-fix patches, and CI test-verified AppSec gates (Asset B) are deferred to Future Phase 2.
