# Candidate v1 Specification — Automated Pre-Bill Chart Compliance Console

## 1. Core Objective
Ship an on-premises automated pre-bill clinical documentation and ICD-10 compliance console within 12 weeks by wrapping Asset A's mature chart parser (96.4% F1, 120 ms/chart) into a daily coder review queue that catches under-coded encounters before claim submission.

## 2. System Architecture
- **Ingestion:** Scheduled nightly batch job reads closed encounter summaries from the local EHR replica inside the hospital VPC and calls the existing Asset A REST service.
- **Confidence-Gated Queue:** Flags encounters where parsed diagnoses diverge from draft billing codes with calibrated probability >= 0.85, writing structured audit records to the existing local PostgreSQL cluster.
- **HIM Coder Review UI:** Lightweight internal React app showing highlighted chart evidence spans, suggested ICD-10 deltas, and 1-click accept/dismiss reason codes (logged to tune thresholds weekly without ever auto-submitting claims).

## 3. Security, Privacy & Operational Guardrails
- Deployed strictly inside the hospital on-prem Kubernetes VPC; zero outbound network calls and zero PHI egress.
- Hospital Active Directory SSO restricts access to credentialed HIM coders and clinical documentation auditors; immutable append-only audit trail logs every coder decision.
- Deterministic fail-safe: if the parser service degrades, claims flow cleanly through standard manual coding with zero billing delay.

## 4. Rollout & Resource Budget
- **Team:** 2 full-time engineers + 1 part-time informatics lead (weeks 1–4 VPC pipeline & calibration audit, weeks 5–7 coder UI & SSO, weeks 8–10 shadow evaluation on 2,000 consecutive closed encounters with blind senior HIM adjudication, weeks 11–12 live production cutover).
- **Non-Payroll Spend:** $4,200 (internal TLS certs, observability storage, coder UX testing) — well under the $18,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 12-Week Window)
- >= 94% precision on flagged pre-bill discrepancies adjudicated blind by two senior HIM auditors on the 2,000-chart shadow sample in weeks 8–10 (lower 95% CI >= 90%), plus documented estimated net capture per audited chart.
- <= 90 seconds median coder review time per flagged encounter and zero PHI egress incidents.

## 6. Explicit Non-Goals for v1
- Real-time bedside shift-change handoff tooling, live HL7 alert ranking, and nurse override feedback loops (Asset B) are deferred to Future Phase 2 once Q1 pre-bill validation completes.
