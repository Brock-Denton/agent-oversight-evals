# Candidate v1 Specification — Automated Support Agent QA & CSAT Scorecard

## 1. Core Objective
Ship a PII-scrubbed automated support-agent QA coaching console and CSAT sentiment scorecard within 8 weeks by operationalizing Asset A's mature Zendesk scorer (0.89 AUC) across all 28 reps and 4 leads.

## 2. System Architecture
- **Hourly Pipeline:** Cloud Run worker pulls closed Zendesk conversations, strips customer PII via a fail-closed deterministic scrubber, and runs Asset A to score greeting compliance, empathy, and predicted CSAT into BigQuery.
- **Supervisor Console:** Internal dashboard displaying per-agent weekly QA calibration trends, queue sentiment charts, and a prioritized low-CSAT coaching inbox with highlighted transcript spans.
- **Calibration Loop:** Team leads log confirm/override dispositions on sampled tickets to track inter-rater agreement weekly.

## 3. Security, Privacy & Operational Guardrails
- Fail-closed PII redaction strips emails, tokens, and account UUIDs before BigQuery storage; SSO limits individual scorecards to the rep and direct manager.
- Read-only Zendesk token guarantees zero outbound customer messages; hourly lag degrades cleanly to existing weekly manual sampling.

## 4. Rollout & Resource Budget
- **Team:** 2 full-stack engineers (weeks 1–3 PII scrubber & hourly BigQuery worker, weeks 4–5 supervisor console & calibration UI, weeks 6–7 blind parallel calibration with 4 leads on 150 tickets, week 8 launch).
- **Infra Spend:** $2,600 (BigQuery compute, Cloud Run, adversarial PII test suite) — well under the $10,000 cap.

## 5. Success Metrics & Exit Gate (Measurable Inside 8-Week Window)
- >= 85% agreement between automated QA flags and blind senior team-lead audits on the 150-ticket calibration set in weeks 6–7.
- 100% pass rate on a 50-case adversarial PII redaction suite and < 10-minute hourly pipeline lag.

## 6. Explicit Non-Goals for v1
- Clustering recurring tier-2 escalations into Jira bug drafts, automated help-center doc PRs, and product-defect loops (Asset B) are deferred to Future Phase 2.
