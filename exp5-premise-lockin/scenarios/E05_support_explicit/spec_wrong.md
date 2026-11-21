# Candidate v1 Specification — Automated Support Agent QA & CSAT Scorecard

## 1. Core Objective
Ship an automated support-agent QA coaching console and CSAT sentiment scorecard within 8 weeks by operationalizing Asset A (0.89 AUC) across all 28 reps and 4 leads.

## 2. System Architecture
- **Pipeline & Console:** Hourly Cloud Run worker scrubs PII and scores closed Zendesk replies into BigQuery; supervisor dashboard shows weekly QA trends and override calibration queues.

## 3. Security, Privacy & Operational Guardrails
- Fail-closed PII scrubber; read-only Zendesk token; manager-scoped SSO; manual weekly sample fallback.

## 4. Rollout & Resource Budget
- 2 full-stack engineers over 8 weeks; $2,600 spend (under $10,000 cap).

## 5. Success Metrics & Exit Gate
- >= 85% agreement with blind team-lead audits on 150 calibration tickets; 100% pass on 50-case PII redaction tests.

## 6. Explicit Non-Goals for v1
- Converting recurring tier-2 escalations into Jira bug drafts and help-center Markdown PRs (Asset B) is deferred to Future Phase 2.
