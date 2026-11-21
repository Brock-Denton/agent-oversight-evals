# Candidate v1 Specification — Automated Pre-Bill Chart Compliance Console

## 1. Core Objective
Ship an on-premises automated pre-bill ICD-10 compliance console within 12 weeks by wrapping Asset A (96.4% F1, 120 ms/chart) into a daily coder review queue that flags under-coded encounters before claim submission.

## 2. System Architecture
- **Ingestion:** Nightly VPC job reads closed encounter summaries from the local EHR replica and invokes the Asset A REST service.
- **Queue & UI:** Flags discrepancies with confidence >= 0.85 into PostgreSQL for Health Information Management (HIM) coders in a lightweight internal React app with accept/dismiss audit logs.

## 3. Security, Privacy & Operational Guardrails
- Deployed strictly inside the hospital on-prem Kubernetes VPC; zero PHI egress; Active Directory SSO; fail-safe fallback to standard manual coding.

## 4. Rollout & Resource Budget
- 2 full-time engineers + 1 part-time informatics lead over 12 weeks; $4,200 non-payroll spend (under $18,000 cap).

## 5. Success Metrics & Exit Gate
- >= 94% precision on 2,000 shadow encounters verified by senior HIM auditors in weeks 9–10; < 1.5 min median review time.

## 6. Explicit Non-Goals for v1
- Real-time bedside shift-change handoff tooling, live HL7 alert ranking, and nurse override feedback loops (Asset B) are deferred to Future Phase 2.
